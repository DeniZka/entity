from prc import Processor
from pyglet.gl import *
from cmp_renderable import Renderable
from pymunk import Vec2d
from prc_camera import CameraProcessor
from cmp_physics import Physics
from prc_ui import UIProcessor
from pymunk.pyglet_util import DrawOptions


class TextureRenderProcessor(Processor):

    def __init__(self, debug_draw = True):
        super().__init__()
        Renderable.batch = pyglet.graphics.Batch()
        Renderable.ui_batch = pyglet.graphics.Batch()
        Renderable.bg = pyglet.graphics.OrderedGroup(0)
        Renderable.mg = pyglet.graphics.OrderedGroup(1)
        Renderable.fg = pyglet.graphics.OrderedGroup(2)
        Renderable.ui = pyglet.graphics.OrderedGroup(3)

        self.cam = None

        self.debug_draw = debug_draw
        self.debug_draw = debug_draw
        if debug_draw:
            self.opt = DrawOptions()
            #            self.opt.shape_static_color
            self.fps_display = pyglet.clock.ClockDisplay()

    def on_add(self):
        self.sub_id = self.world.win_hnd.subscribe("on_draw", self.on_draw)

    def on_remove(self):
        self.world.win_hnd.unsubscribe("on_draw", self.sub_id)

    def process(self, dt):
        # This will iterate over every Entity that has this Component, and
        # add the texture associated with the Renderable Component instance
        # and its vertice_list to the render batch. The batch will then be
        # drawn by the 'on_draw' event handler of teh main window:
        for entity, renderable in self.world.get_component(Renderable):
            self.draw_texture(renderable, entity)

    def draw_texture(self, rend, entity):
        texture = rend.texture

        if rend.sub_modif:
            rend.vertex_list.colors[:] = rend.colors

        if rend.pos2: #lines
            v1 = rend.pos
            v2 = rend.pos2
            rend.vertex_list.vertices[:] = [v1.x, v1.y, v2.x, v2.y]
        else: #quads and with textures
            hw = rend.w * 0.5
            hh = rend.h * 0.5
            v1 = Vec2d(-hw, -hh)
            v1.rotate(rend.angle)
            v1 += rend.pos
            v2 = Vec2d( hw, -hh)
            v2.rotate(rend.angle)
            v2 += rend.pos
            v3 = Vec2d(hw, hh)
            v3.rotate(rend.angle)
            v3 += rend.pos
            v4 = Vec2d(-hw, hh)
            v4.rotate(rend.angle)
            v4 += rend.pos
            rend.vertex_list.vertices[:] = [v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, v4.x, v4.y]

    def on_draw(self):
        if not self.cam:
            self.cam = self.world.get_processor(CameraProcessor)

        self.cam.apply_transform()
        if self.debug_draw:
            Physics.space.debug_draw(self.opt)
        if Renderable.bg_image:
            Renderable.bg_image.blit(0, 0, 0)
        Renderable.batch.draw()

        self.cam.restore_transform()

        uip = self.world.get_processor(UIProcessor)
        if uip:
            uip.draw()

        if self.debug_draw:
            self.fps_display.draw()

