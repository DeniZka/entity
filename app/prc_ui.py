import math

import pyglet
from pyglet.gl import *
from pymunk import Vec2d

from app.cmp_physics import Physics
from app.cmp_renderable import Renderable
from app.cmp_transform import Transform
from app.factory import Factory
from app.hnd_window import WindowHandler
from app.prc import Processor
from app.prc_camera import CameraProcessor


class UIProcessor(Processor):
    def __init__(self):
        self.cam = None
        self.win_coord = None
        self.scene_coord = None
        self.screen = None
        self.w_width = 800
        self.w_height = 600
        self.com_t = Vec2d(0, 0)
        return

    def on_add(self, proc):
        if proc == self and self.world.win_hnd:
            self.cam = self.world.get_processor(CameraProcessor)
            self.sub_id = self.world.win_hnd.subscribe("on_resize", self.on_win_resize)
            self.sub_id = self.world.win_hnd.subscribe("on_mouse_motion", self.on_mouse_motion)
            self.world.win_hnd.subscribe("on_mouse_drag", self.on_mouse_drag)
        if proc.__class__ is CameraProcessor:
            self.cam = proc

    def on_remove(self):
        if self.world.win_hnd:
            self.world.win_hnd.unsubscribe("on_resize", self.sub_id)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x, y, dx, dy)


    def on_mouse_motion(self, x, y, dx, dy):
        return
        self.win_coord.text = "Actual\tX:" + str(x) + "\tY:" + str(y)
        v = self.cam.to_world(Vec2d(x, y))
        self.scene_coord.text = "World\tX:" + str(int(v.x)) + "\tY:" + str(int(v.y))
        v = self.cam.to_screen(v)
        self.screen.text = "Back\tX:" + str(int(v.x)) + "\tY:" + str(int(v.y))
        return

    def on_win_resize(self, width, height):
        return
        self.com_t.x = width - 64
        self.com_t.y = height - 64
        self.com_t._set_modified()
        self.win_coord.y = height - 15
        self.scene_coord.y = height - 30
        self.screen.y = height - 45
        return
        self.vel.x = width - 64
        self.vel.y = height - 150

    def load_ui(self):
        self.win_coord = pyglet.text.Label("", x=0, y=WindowHandler.res[1] - 15, batch=Renderable.ui_batch)
        self.scene_coord = pyglet.text.Label("", x=0, y=WindowHandler.res[1] - 30, batch=Renderable.ui_batch)
        self.screen = pyglet.text.Label("", x=0, y=WindowHandler.res[1] - 45, batch=Renderable.ui_batch)

        pfct = self.world.get_processor(Factory)
        v = Vec2d(WindowHandler.res[0] - 64,
                  WindowHandler.res[1] - 64)
        compass = self.world.create_entity()
        tex = pyglet.resource.image("compass.png").get_texture(True)
        t = Transform(v, Vec2d(tex.width, tex.height))

        rend = Renderable(tex, group=Renderable.ui, verts=t.q_verts())
        rend.colors = [255, 255, 255, 150]

        self.world.add_component(compass, t)
        self.world.add_component(compass, rend)
        self.com_t = t
        return

        self.pl_phy = self.world.component_for_entity(pfct.player, Physics)
        self.en_phy = self.world.component_for_entity(pfct.enemy, Physics)

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
            x =WindowHandler.res[0] - 40,
            y =WindowHandler.res[1] - 150
        )


    def process(self, dt):
        self.com_t.angle = -self.cam.angle

        return
        if self.pl_phy:
            self.p_rend.angle = self.pl_phy.body.angle - self.cam.angle
            l = self.pl_phy.body.velocity.length
            if abs(l) > 0.5:
                a = self.pl_phy.body.velocity.angle - self.cam.angle
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
            self.e_rend.angle = v.angle - self.cam.angle

        return

    def draw(self):
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.w_width, 0, self.w_height, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)
        Renderable.ui_batch.draw()
        return
        self.vel.draw()
