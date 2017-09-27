import esper
import pyglet
from cmp_renderable import Renderable
from pymunk import Vec2d
import math
from hnd_window import WindowHandler
from factory import Factory
from cmp_physics import Physics
from prc_camera import Camera


class UIProcessor(esper.Processor):
    def __init__(self):
        return

    def load_ui(self):
        pfct = self.world.get_processor(Factory)
        self.pl_phy = self.world.component_for_entity(pfct.player, Physics)
        self.en_phy = self.world.component_for_entity(pfct.enemy, Physics)

        pos = Vec2d(WindowHandler.RESOLUTION[0] - 64,
                    WindowHandler.RESOLUTION[1] - 64)
        compass = self.world.create_entity()
        tex = pyglet.resource.image("compass.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = pos
        self.world.add_component(compass, rend)
        self.com_rend = rend
        #self dir arrow
        arrow = self.world.create_entity()
        tex = pyglet.resource.image("arrow.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = pos
        rend.set_pos_lock(True)
        rend.colors = [255, 0, 0, 255] * 4
        self.world.add_component(arrow, rend)
        self.p_rend = rend
        #enemy pos dir arrow
        arrow = self.world.create_entity()
        tex = pyglet.resource.image("arrow_enemy.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = pos
        rend.set_pos_lock(True)
        rend.colors = [0, 0, 255, 255] * 4
        self.world.add_component(arrow, rend)
        self.e_rend = rend
        #Selv velocity dir
        arrow = self.world.create_entity()
        tex = pyglet.resource.image("arrow.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = pos
        rend.set_pos_lock(True)
        rend.colors = [0, 200, 75, 200] * 4
        rend.w = rend.w * 0.5
        self.world.add_component(arrow, rend)
        self.v_rend = rend

    def process(self, dt):
        if self.pl_phy:
            self.p_rend.angle = self.pl_phy.body.angle - Camera.angle
            l = self.pl_phy.body.velocity.length
            if abs(l) > 0.5:
                a = self.pl_phy.body.velocity.angle - Camera.angle
                a -= math.pi/2
                self.v_rend.angle = a
                self.v_rend.h = 128
            else:
                self.v_rend.h = 0
        if self.en_phy:
            v = self.en_phy.body.position - self.pl_phy.body.position
            v.rotate(math.radians(-90))
            self.e_rend.angle = v.angle - Camera.angle
        self.com_rend.angle = -Camera.angle

        return

    def draw(self):
        return