import math
import xml.etree.ElementTree as ET
from random import randint

import pyglet
from pyglet.gl import *
from pyglet.graphics import Group
import pymunk
from pymunk import Vec2d

from app.cmp_cannon import Cannon
from app.cmp_hp import Hp
from app.cmp_input import Input
from app.cmp_instance import Instance
from app.cmp_joint import Joint
from app.cmp_part_emiter import ParticleEmiter
from app.cmp_physics import Physics
from app.cmp_renderable import Renderable
from app.cmp_segment import Segment
from app.cmp_temp_live import TempLive
from app.cmp_transform import Transform
from app.cmp_pin import Pin
from app.prc import Processor


class Factory(Processor):
    def __init__(self):
        pyglet.resource.path = ['res']

    def joint_mod_colors(self, rend):
        #became two way
        if rend.colors[0] == 255:
            rend.colors = [0, 255, 0, 255]
            return
        #became threeway
        if rend.colors[1] == 255:
            rend.colors = [0, 0, 255, 255]
            return
        #became four way
        if rend.colors[2] == 255:
            rend.colors = [254, 0, 255, 255]
            return

    def createEnv(self):
        self.environment = self.world.create_entity()  #first of all global entity for environment world
        t = Transform(Vec2d(0, -20), Vec2d(7200, 20))
        t.angle = 0
        base = Renderable(group=t, verts=t.q_verts())
        base.colors = [0, 200, 0, 255]
        self.world.add_component(self.environment, base)
        self.world.add_component(self.environment, t)

        lines = [
            pymunk.Segment(Physics.space.static_body, Vec2d(0, 0), Vec2d(7200, 0), 10),
            pymunk.Segment(Physics.space.static_body, Vec2d(0, 0), Vec2d(0, 480), 2),
            pymunk.Segment(Physics.space.static_body, Vec2d(720, 0), Vec2d(720, 480), 6)
        ]

        for l in lines:
            l.friction = 0.5
            l.collision_type = Physics.coll_types["walls"]
        Physics.space.add(lines)

        #load tracks
        f = open("res/Plymouth.rwm")
        self.tree = ET.parse(f)
        self.root = self.tree.getroot()
        self.meta = self.root[0]
        fn = "res/" + self.meta[1].attrib["File"]
        Renderable.bg_image = pyglet.image.load(fn)
        Renderable.bg_image.anchor_y = Renderable.bg_image.height
        self.segs = self.root[1]
        for seg in self.segs:
            if seg.tag == "TrackSegment" or seg.tag == "HiddenSegment" or seg.tag == "Crossing"\
                    or seg.tag == "LUSegment" or seg.tag == "EESegment":

                v1 = v2 = Vec2d(0, 0)
                begin = None #int(seg.attrib["Begin"])
                end = None  #int(seg.attrib["End"])
                #id = int(seg.attrib["ID"])
                v1 = Vec2d(float(seg.attrib["X1"]), -float(seg.attrib["Y1"]))
                v2 = Vec2d(float(seg.attrib["X2"]), -float(seg.attrib["Y2"]))

                #replace with existing nodes
                fnd_begin = False
                fnd_end = False
                for e, (j, rend, tr) in self.world.get_components(Joint, Renderable, Transform):
                    if not fnd_begin:
                        if v1.get_dist_sqrd(tr.pos) < 1:
                            v1 = tr.pos
                            self.joint_mod_colors(rend)
                            begin = j
                    if not fnd_end:
                        if v2.get_dist_sqrd(tr.pos) < 1:
                            v2 = tr.pos
                            self.joint_mod_colors(rend)
                            end = j
                    #both found
                    if begin != None and end != None:
                        break

                self.create_segment(v1, v2, seg.tag, begin, end)


            elif seg.tag == "Switch" or seg.tag == "FourWay" :
                v1 = Vec2d(float(seg.attrib["X"]), -float(seg.attrib["Y"]))
                for e, (j, tr) in self.world.get_components(Joint, Transform):
                    #make switch
                    if tr.pos.get_dist_sqrd(v1) < 1:
                        self.create_switch(j, tr)
                        break
                continue
        return self.environment

    def testing(self):
        #alone green point
        e = self.world.create_entity()
        r = Renderable(atype=GL_POINTS)
        r.colors = [20, 255, 0, 255 ]
        t = Transform(Vec2d(400, 100))
        self.world.add_component(e, r)
        self.world.add_component(e, t)

        #5 circles scaled from anchor point
        for i in range(1, 6):
            e = self.world.create_entity()
            r = Renderable(self.texture_from_image("joint.png"))
            r.colors = [randint(0, 255), randint(0,255), randint(0,255), 255] * 4
            t = Transform(Vec2d(300, 300), Vec2d(10, 10))
            t.anchor = Vec2d(2, 2)
            t.scale = Vec2d(1*i, i*1)
            self.world.add_component(e, r)
            self.world.add_component(e, t)

        #Unzumable test
        e = self.world.create_entity()
        r = Renderable(self.texture_from_image("joint.png"))
        r.colors = [255, 0, 0, 255] * 4
        t = Transform(Vec2d(150, 150), Vec2d(10, 10))
        t.unzoomable = True
        self.world.add_component(e, r)
        self.world.add_component(e, t)
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


    def create_switch(self, j, tr):
        ent = self.world.create_entity()
        # render comp
        im = pyglet.resource.image("joint.png")
        tex = im.get_texture()

        t = Transform(Vec2d(0, 0), Vec2d(10, 20))
        t.anchor = Vec2d(5, 10)
        t.parent = tr
        t.angle = 10
        #t._set_modified()
        r = Renderable(tex,group=t, verts=t.q_verts())
        r.colors = [255, 0, 0, 255]
        self.world.add_component(ent, r)
        self.world.add_component(ent, t)


    def create_segment(self, v1, v2=None, tag="TrackSegment", begin=None, end=None ):
        """

        :param v1: segment start point vector
        :param v2: segment end point vector
        :param tag: type of track
        :param begin: begin joint if found
        :param end: end joint if found
        :return: vector for second joint
        """
        #reseve entity for Segment
        ent = self.world.create_entity()

        if not v2:
            v2 = Vec2d(v1)

        #joint entity for head
        b_j = begin
        if b_j == None:
            b_ent = self.world.create_entity()
            b_j = Joint(b_ent)
            # transform
            t = Transform(v1, Vec2d(5, 5))
            self.world.add_component(b_ent, t)
            self.world.add_component(b_ent, b_j)


        tr2 = None #will return last added for editor
        #joint entity for tail
        e_j = end
        e_ent = 0
        if e_j == None:
            e_ent = self.world.create_entity()
            e_j = Joint(e_ent)
            tr2 = Transform(v2, Vec2d(5, 5))
            self.world.add_component(e_ent, tr2)
            self.world.add_component(e_ent, e_j)

        s = Segment(ent, v1, v2, b_j.id, e_j.id, tag)
        self.world.add_component(ent, s)

        #add segment ID in joints
        b_j.attach(ent)
        e_j.attach(ent)

        # create segment line
        tr = Transform(v1)  # TODO REMOVE
        verts = [v1.x, v1.y, v2.x, v2.y]
        br = Renderable(atype=GL_LINES, verts=verts)
        br.add_points(verts, color=[255, 70, 70, 255], group=Renderable.fat_point)
        if tag == "TrackSegment":
            br.colors = [000, 200, 0, 255]
        elif tag == "HiddenSegment":
            br.colors = [100, 100, 100, 255]
        elif tag == "Crossing":
            br.colors = [200, 0, 0, 255]
        elif tag == "LUSegment":
            br.colors = [200, 100, 0, 255]
        elif tag == "EESegment":
            br.colors = [200, 0, 200, 255]
        self.world.add_component(ent, br)
        return (e_ent, e_j, [tr2, s])

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

    def create_instance(self, pos):
        width = 250
        height = 400
        # main body
        e = self.world.create_entity()
        i = Instance()
        T = Transform(pos, Vec2d(width, height))  #main bounding sizes
        T._anchor = Vec2d(0, 0)
        T.angle = 0
        r = Renderable(group=T, verts=T.q_verts())
        r.colors = [0, 0, 255, 100]
        #for i in range(0, 1000):
        #    r.add_quads([0+i*2, 0, width+i*2, 0, width+i*2, height+i, 0+i*3, height-3  ])
        self.world.add_component(e, i)
        self.world.add_component(e, r)
        self.world.add_component(e, T)

        #around lines
        e = self.world.create_entity()
        t = Transform(Vec2d(0,0))
        t.pos1 = Vec2d(width, 0)
        t.parent = T
        r = Renderable(group=t, atype=GL_LINES, verts=t.l_verts())
        r.colors = [255, 0, 0, 255]
        r.add_line([0,0,0,height])
        r.add_line([width,0,width,height])
        r.add_line([0,height,width,height])
        #for i in range(0, 1000):
        #    r.add_line([width+i*2, 0, width+i*2, height ])
        self.world.add_component(e, r)
        self.world.add_component(e, t)

        #instance name
        t = Transform(Vec2d(100,5))
        t.parent = T
        t.angle = 90
        l = pyglet.text.Label(
            "INSTANCE_NAME",
            font_size=8,
            batch=Renderable.batch,  # will be batched by batch.draw()
            group=t,
            anchor_y="center"
        )

        #instance type
        t = Transform(Vec2d(115, 5))
        t.parent = T
        t.angle = 90
        l = pyglet.text.Label(
            "instance_type",
            font_size=8,
            batch=Renderable.batch,  # will be batched by batch.draw()
            group=t,
            anchor_y="center"
        )

        #left pins
        for i in range(15):
            #a pin joint
            pin_pos = Vec2d(-10, 13+i*27)
            e_ent = self.world.create_entity()
            #e_j = Joint(e_ent)
            e_j = Pin()
            self.world.add_component(e_ent, e_j)
            tr2 = Transform(pin_pos, Vec2d(10, 0))
            tr2.parent = T
            self.world.add_component(e_ent, tr2)
            fat_line_g = FatLineGroup(parent=tr2)
            r = Renderable(
                #group=Renderable.fat_line,  #todo subgroup
                group=fat_line_g,
                #group=tr2,
                atype=GL_LINES,
                verts=tr2.l_verts()
            )
            r.colors = [0, 255, 0, 255]
            self.world.add_component(e_ent, r)

            #joint label
            e = self.world.create_entity()
            #this a bit faster
            #t = Transform (Vec2d(pin_pos.x+20, pin_pos.y))
            #t.parent = T
            # this a bit comfortable
            t = Transform(Vec2d(20, 0))
            t.parent = tr2
            l = pyglet.text.Label(
                "InputPin_"+str(i),
                font_size=8,
                batch=Renderable.batch, # will be batched by batch.draw()
                group=t,
                anchor_y="center"
            )
            self.world.add_component(e, t)
            self.world.add_component(e, l)

        #right pins
        for i in range(15):
            #a pin joint
            pin_pos = Vec2d(width+10, 13+i*27)
            e_ent = self.world.create_entity()
            #e_j = Joint(e_ent) move to Pin entity
            e_j = Pin()
            self.world.add_component(e_ent, e_j)
            tr2 = Transform(pin_pos, Vec2d(-10, 0))
            tr2.parent = T
            self.world.add_component(e_ent, tr2)
            fat_line_g = FatLineGroup(parent=tr2)
            r = Renderable(
                #group=Renderable.fat_line,  #todo subgroup
                group=fat_line_g,
                #group=tr2,
                atype=GL_LINES,
                verts=tr2.l_verts()
            )
            r.colors = [0, 255, 0, 255]
            self.world.add_component(e_ent, r)

            #joint label
            e = self.world.create_entity()
            #this a bit faster
            #t = Transform (Vec2d(pin_pos.x-20, pin_pos.y))
            #t.parent = T
            #this a bit comfortable
            t = Transform(Vec2d(-20, 0))
            t.parent = tr2
            l = pyglet.text.Label(
                "OutPin_"+str(i),
                font_size=8,
                batch=Renderable.batch, # will be batched by batch.draw()
                group=t,
                anchor_y="center",
                anchor_x="right"
            )
            self.world.add_component(e, t)
            self.world.add_component(e, l)

        return T


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



class FatLineGroup(Group):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_state(self):
        glLineWidth(4)

    def unset_state(self):
        glLineWidth(1)


class FatPointGroup(Group):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_state(self):
        glPointSize(3)

    def unset_state(self):
        glPointSize(1)