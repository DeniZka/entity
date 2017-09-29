from prc import Processor
import pyglet
from cmp_renderable import Renderable
from pymunk import Vec2d
import math
from hnd_window import WindowHandler
from factory import Factory
from cmp_physics import Physics
from prc_camera import CameraProcessor


class UIProcessor(Processor):
    def __init__(self):
        return

    def on_add(self):
        if self.world.win_hnd:
            self.sub_id = self.world.win_hnd.subscribe("on_resize", self.on_win_resize)

    def on_remove(self):
        if self.world.win_hnd:
            self.world.win_hnd.unsubscribe("on_resize", self.sub_id)

    def on_win_resize(self, width, height):
        self.compass_pos.x = width - 64
        self.compass_pos.y = height - 64

        self.vel.x = width - 64
        self.vel.y = height - 150

    def load_ui(self):
        pfct = self.world.get_processor(Factory)
        self.pl_phy = self.world.component_for_entity(pfct.player, Physics)
        self.en_phy = self.world.component_for_entity(pfct.enemy, Physics)

        self.compass_pos = Vec2d(WindowHandler.RESOLUTION[0] - 64,
                    WindowHandler.RESOLUTION[1] - 64)
        compass = self.world.create_entity()
        tex = pyglet.resource.image("compass.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = self.compass_pos
        self.world.add_component(compass, rend)
        self.com_rend = rend
        #self dir arrow
        arrow = self.world.create_entity()
        tex = pyglet.resource.image("arrow.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = self.compass_pos
        rend.set_pos_lock(True)
        rend.colors = [255, 0, 0, 255] * 4
        self.world.add_component(arrow, rend)
        self.p_rend = rend
        #enemy pos dir arrow
        arrow = self.world.create_entity()
        tex = pyglet.resource.image("arrow_enemy.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = self.compass_pos
        rend.set_pos_lock(True)
        rend.colors = [0, 0, 255, 255] * 4
        self.world.add_component(arrow, rend)
        self.e_rend = rend
        #Selv velocity dir
        arrow = self.world.create_entity()
        tex = pyglet.resource.image("arrow.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = self.compass_pos
        rend.set_pos_lock(True)
        rend.colors = [0, 200, 75, 200] * 4
        rend.w = rend.w * 0.5
        self.world.add_component(arrow, rend)
        self.v_rend = rend
        #velocity
        self.vel = pyglet.text.Label(
            str(self.pl_phy.body.velocity.length),
            x = WindowHandler.RESOLUTION[0] - 40,
            y = WindowHandler.RESOLUTION[1] - 150
        )


    def process(self, dt):
        cam = self.world.get_processor(CameraProcessor)
        if self.pl_phy:
            self.p_rend.angle = self.pl_phy.body.angle - cam.angle
            l = self.pl_phy.body.velocity.length
            if abs(l) > 0.5:
                a = self.pl_phy.body.velocity.angle - cam.angle
                a -= math.pi/2
                self.v_rend.angle = a
                self.v_rend.h = 128
                # velocity text update
                self.vel.text = str(int(self.pl_phy.body.velocity.length))
            else:
                self.v_rend.h = 0
        if self.en_phy:
            v = self.en_phy.body.position - self.pl_phy.body.position
            v.rotate(math.radians(-90))
            self.e_rend.angle = v.angle - cam.angle
        self.com_rend.angle = -cam.angle
        return

    def draw(self):
        Renderable.ui_batch.draw()
        self.vel.draw()
