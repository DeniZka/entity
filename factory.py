from prc import Processor
import pyglet
from cmp_transform import Transform
from cmp_renderable import Renderable
from cmp_renderables import Renderables
import pymunk
from cmp_physics import Physics
import math
from pymunk import  Vec2d
from cmp_input import  Input
from cmp_cannon import  Cannon
from cmp_temp_live import TempLive
from cmp_hp import Hp
from cmp_part_emiter import ParticleEmiter
import math
from cmp_joint import Joint
import xml.etree.ElementTree as ET
from cmp_segment import Segment
from pyglet.gl import *

class Factory(Processor):
    def __init__(self):
        pyglet.resource.path = ['res']

    def joint_mod_colors(self, rend):
        #became two way
        if rend.colors[0] == 255:
            rend.colors = [0, 255, 0, 255] * 4
            return
        #became threeway
        if rend.colors[1] == 255:
            rend.colors = [0, 0, 255, 255] * 4
            return
        #became four way
        if rend.colors[2] == 255:
            rend.colors = [254, 0, 255, 255] * 4
            return

    def createEnv(self):
        self.environment = self.world.create_entity()  #first of all global entity for environment world
        lines = [
            pymunk.Segment(Physics.space.static_body, Vec2d(0, 0), Vec2d(7200, 0), 10),
            pymunk.Segment(Physics.space.static_body, Vec2d(0, 0), Vec2d(0, 480), 2),
            pymunk.Segment(Physics.space.static_body, Vec2d(720, 0), Vec2d(720, 480), 6)
        ]

        self.world.add_component(self.environment, Transform(Vec2d(7200/2, 0), 7200, 20))
        base = Renderable()
        base.colors = [0, 200, 0, 255] * 4
        self.world.add_component(self.environment, base)

        for l in lines:
            l.friction = 0.5
            l.collision_type = Physics.coll_types["walls"]
        Physics.space.add(lines)

        #load tracks
        self.tree = ET.parse("res/Plymouth.rwm")
        self.root = self.tree.getroot()
        self.meta = self.root[0]
        fn = "res/" + self.meta[1].attrib["File"]
        Renderable.bg_image = pyglet.image.load(fn)
        Renderable.bg_image.anchor_y = Renderable.bg_image.height
        self.segs = self.root[1]
        for seg in self.segs:
            if seg.tag == "TrackSegment" or seg.tag == "HiddenSegment" or seg.tag == "Crossing"\
                    or seg.tag == "LUSegment" or seg.tag == "EESegment":

                ent = self.world.create_entity()
                v1 = v2 = Vec2d(0, 0)

                begin = int(seg.attrib["Begin"])
                end = int(seg.attrib["End"])
                id = ent #int(seg.attrib["ID"])
                v1 = Vec2d(float(seg.attrib["X1"]), -float(seg.attrib["Y1"]))
                v2 = Vec2d(float(seg.attrib["X2"]), -float(seg.attrib["Y2"]))

                #replace with existing nodes
                fnd_begin = False
                fnd_end = False
                for e, (j, rends) in self.world.get_components(Joint, Renderables):
                    if not fnd_begin:
                        if v1.get_dist_sqrd(j.pos) < 1:
                            v1 = j.pos
                            ways = j.attach(id)
#                            if ways == 3:
#                                self.switch_rend(j,)
                            self.joint_mod_colors(rends.renderable[0])
                            fnd_begin = True
                    if not fnd_end:
                        if v2.get_dist_sqrd(j.pos) < 1:
                            v2 = j.pos
                            ways = j.attach(id)
                            self.joint_mod_colors(rends.renderable[0])
                            fnd_end = True

                    #both found
                    if fnd_begin and fnd_end:
                        break

                s = Segment(id, v1, v2,  begin,  end, seg.tag)
                self.world.add_component(ent, s)

                # create node circle
                if not fnd_begin:
                    jent = self.world.create_entity()
                    j = Joint(jent, v1, id)
                    self.world.add_component(jent, j)
                    #transform
                    self.world.add_component(jent, Transform(v1, 5, 5))
                    #switch circle
                    r = Renderable(self.texture_from_image("joint.png"))
                    r.colors = [255, 0, 0, 255] * 4
                    rs = Renderables(r)
                    self.world.add_component(jent, rs)
                if not fnd_end:
                    jent = self.world.create_entity()
                    j = Joint(jent, v2, id)
                    self.world.add_component(jent, j)
                    self.world.add_component(jent, Transform(v2, 5, 5))
                    r = Renderable(self.texture_from_image("joint.png"))
                    r.colors = [255, 0, 0, 255] * 4
                    rs = Renderables(r)
                    self.world.add_component(jent, rs)

                #create segment line
                tr = Transform(v1)
                tr._pos[1] = v2
                self.world.add_component(ent, tr)
                br = Renderable(atype=GL_LINES)
                if seg.tag == "TrackSegment":
                    br.colors = [000, 200, 0, 255] * 2
                elif seg.tag == "HiddenSegment":
                    br.colors = [100, 100, 100, 255] * 2
                elif seg.tag == "Crossing":
                    br.colors = [200, 0, 0, 255] * 2
                elif seg.tag == "LUSegment":
                    br.colors = [200, 100, 0, 255] * 2
                elif seg.tag == "EESegment":
                    br.colors = [200, 0, 200, 255] * 2
                self.world.add_component(ent, br)

            #elif seg.tag == "Switch":
        return self.environment

    def testing(self):
        #ent = self.world.create_entity()
        #rends = Renderables();
        #self.world.add_component(ent, rends)
        return

    def createPlayer(self, pos):
        player = self.world.create_entity()
        widht = 64
        hw = widht/2
        height = 64
        hh = height/2
        redsquare = Renderable(texture=self.texture_from_image("ship.png"))
        redsquare.colors = [255,0,0,255] * 4
        redsquare.colors[1] = 255
        redsquare.colors[3] = 100
        self.world.add_component(player, redsquare)
        #engine emitter
        emiters = []
        e = ParticleEmiter(Vec2d(0, -34), math.radians(180), 0.03, True)
        emiters.append(e)
        self.world.add_component(player, e)
        #physics
        vs = [(0, hh), (hw, -hh), (-hw, -hh)]
        poly_mass = 10
        m = pymunk.moment_for_poly(poly_mass,vs,(0,0),0)
        b = pymunk.Body(poly_mass, m)
        b.center_of_gravity = (0, -hh/2)
        s = pymunk.Poly(b, vs)
        s.collision_type = Physics.coll_types["player"]
        s.friction = 0.9
        s.entity = player
        s.filter = pymunk.ShapeFilter(0, Physics.cats["player"], Physics.masks["player"])
        b.position = pos
        self.world.add_component(player, Physics(b, s, redsquare, emiters))
        #input
        self.world.add_component(player, Input(0))
        #weapon
        self.world.add_component(player, Cannon(1000))
        self.player = player

        return player, b


    def createEnemy(self, pos):
        enemy = self.world.create_entity()
        #graphics
        widht = 64
        hw = widht/2
        height = 64
        hh = height/2
        bluesquare = Renderable(self.texture_from_image("ship.png"))
        bluesquare.colors = [0,0,255,255] * 4
        self.world.add_component(enemy, bluesquare)
        #engine emitter
        emiters = []
        e = ParticleEmiter(Vec2d(0, -30), math.radians(180), 0.1, True)
        emiters.append(e)
        self.world.add_component(enemy, e)
        #physics
        vs = [(-hw,hh), (hw,hh), (hw,-hh), (-hw,-hh)]
        poly_mass = 1
        m = pymunk.moment_for_poly(poly_mass,vs,(0,0),0)
        b = pymunk.Body(poly_mass, m) #, pymunk.Body.KINEMATIC)
        s = pymunk.Poly(b, vs)
        s.collision_type = Physics.coll_types["enemy"]
        s.friction = 0.9
        s.entity = enemy
        s.filter = pymunk.ShapeFilter(0,Physics.cats["enemy"], Physics.masks["enemy"])
        b.position = pos
        b.angle=math.radians(30)
        self.world.add_component(enemy, Physics(b, s, bluesquare, emiters))
        # input
        self.world.add_component(enemy, Input(1))
        #hp
        self.world.add_component(enemy, Hp(1))
        self.enemy = enemy
        return enemy, b

    def createBullet(self, pos, emitter):
        bullet = self.world.create_entity()
        #render comp
        br = Renderable(self.texture_from_image("bullet.png"), 15, 15)
        br.colors = [255, 0, 0, 255] * 4
        self.world.add_component(bullet, br)
        #physics
        mass = 0.2
        r = 4
        m = pymunk.moment_for_circle(mass, 0, r, (0,0))
        b = pymunk.Body(mass, m)
        b.position = pos

        force = Vec2d(0, 1.0) * 100
        force.rotate(emitter.angle)
        b.velocity = emitter.velocity

        b.apply_impulse_at_world_point(force, pos)

        b.torque = 2000000


        s = pymunk.Circle(b, r)
        s.friction = 0.3
        s.collision_type = Physics.coll_types["p_bullet"]
        s.entity = bullet
        s.filter = pymunk.ShapeFilter(0,Physics.cats["p_bullet"], Physics.masks["p_bullet"])
        self.world.add_component(bullet, Physics(b,s, br))
        self.world.add_component(bullet, TempLive(0.5))
        return bullet


    def create_joint(self, pos):
        ent = self.world.create_entity()
        # render comp
        br = Renderable(self.texture_from_image("joint.png"), 10, 10)
        br.colors = [255, 0, 0, 255] * 4
        br.pos = pos
        self.world.add_component(ent, br)
        # joint
        j = Joint()
        self.world.add_component(ent, j)
        return j

    def create_segment(self, pos):
        ent = self.world.create_entity()

        v1 = Vec2d(pos)
        s = Segment(
            Segment.next_id,
            v1,
            pos,
            -1,
            -1
        )
        Segment.next_id += 1
        self.world.add_component(ent, s)

        br = Renderable(atype=GL_LINES, pos=v1, pos2=pos)
        br.colors = [200, 100, 0, 255] * 2
        self.world.add_component(ent, br)
        return br







    def texture_from_image(self, image_name):
        """Create a pyglet Texture from an image file"""
        return pyglet.resource.image(image_name).get_texture()

    """

    def delete_entity(self, enity):
        if self.world.has_component(enity, Physics):
            phy = self.world.component_for_entity(enity, Physics)
            Physics.space.remove(phy.shape, phy.body)
            self.world.delete_entity(enity)
    """

    def process(self, dt):         #check died entity by ttl
        #"""
        for ent, tl in self.world.get_component(TempLive):
            if not tl.alive(dt):
#                if self.world.has_component(ent, Physics):
#                    phy = self.world.component_for_entity(ent, Physics)
#                    phy.remove(False)
                self.world.delete_entity(ent)


        #"""
        return
