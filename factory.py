import esper
import pyglet
from cmp_renderable import Renderable
import pymunk
from cmp_physics import Physics
import math
from pymunk import  Vec2d
from cmp_input import  Input
from cmp_cannon import  Cannon
from cmp_temp_live import TempLive
from cmp_hp import Hp
from cmp_part_emiter import ParticleEmiter
from prc_camera import Camera
import math

class Factory(esper.Processor):
    def __init__(self):
        pyglet.resource.path = ['res']

    def createEnv(self):
        self.environment = self.world.create_entity()  #first of all global entity for environment world
        lines = [
            pymunk.Segment(Physics.space.static_body, Vec2d(0, 0), Vec2d(720, 0), 2),
            pymunk.Segment(Physics.space.static_body, Vec2d(0, 0), Vec2d(0, 480), 2),
            pymunk.Segment(Physics.space.static_body, Vec2d(720, 0), Vec2d(720, 480), 2)
        ]
        for l in lines:
            l.friction = 0.5
            l.collision_type = Physics.coll_types["walls"]
        Physics.space.add(lines)
        return self.environment

    def createPlayer(self, pos):
        player = self.world.create_entity()
        widht = 64
        hw = widht/2
        height = 64
        hh = height/2
        redsquare = Renderable(texture=self.texture_from_image("ship.png"))
        redsquare.colors = [255,0,0,255] * 4
        self.world.add_component(player, redsquare)
        #engine emitter
        emiters = []
        e = ParticleEmiter(Vec2d(0, -34), math.radians(180), 0.03, True)
        emiters.append(e)
        self.world.add_component(player, e)
        #physics
        vs = [(-hw, hh), (hw, hh), (hw, -hh), (-hw, -hh)]
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
        Physics.space.add(s, b)
        self.world.add_component(player, Physics(b, s, redsquare, emiters))
        #Camera update
        #Camera.target = b
        #input
        self.world.add_component(player, Input(0))
        #weapon
        self.world.add_component(player, Cannon(1000))

        return player


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
        Physics.space.add(s, b)
        self.world.add_component(enemy, Physics(b, s, bluesquare, emiters))
        # input
        self.world.add_component(enemy, Input(1))
        #hp
        self.world.add_component(enemy, Hp(5))
        return enemy

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
        Physics.space.add(b,s)
        self.world.add_component(bullet, Physics(b,s, br))
        self.world.add_component(bullet, TempLive(0.5))
        return bullet





    def texture_from_image(self, image_name):
        """Create a pyglet Texture from an image file"""
        return pyglet.resource.image(image_name).get_texture()

    def delete_entity(self, enity):
        if self.world.has_component(enity, Physics):
            phy = self.world.component_for_entity(enity, Physics)
            Physics.space.remove(phy.shape, phy.body)
            self.world.delete_entity(enity)

    def process(self, dt):
        #check died entity by ttl
        #"""
        for ent, tl in self.world.get_component(TempLive):
            if not tl.alive(dt):
                self.world.delete_entity(ent)


        #"""
