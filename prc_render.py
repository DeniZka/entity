from prc import Processor
from pyglet.gl import *
from cmp_renderable import Renderable
from cmp_transform import Transform
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

    def on_add(self, proc):
        if proc == self:
            self.sub_id = self.world.win_hnd.subscribe("on_draw", self.on_draw)
        if proc.__class__ is CameraProcessor:
            self.cam = proc

    def on_remove(self):
        self.world.win_hnd.unsubscribe("on_draw", self.sub_id)

    def process(self, dt):
        for e, (tr, rend) in self.world.get_components(Transform, Renderable):
            if rend.modified:
                rend.vertex_list.colors[:] = rend.colors

            if tr.modified(self.cam.zoom):
                if rend.atype == GL_POINTS:
                    rend.vertex_list.vertices[:] = [tr.x, tr.y]
                elif rend.atype == GL_LINES:
                    rend.vertex_list.vertices[:] = [
                        tr.x,
                        tr.y,
                        tr.x1,
                        tr.y1
                    ]
                    # make tratsform unmodified
                    tr.redrawed()
                else:
                    rend.vertex_list.vertices[:] = tr.vertixes(self.cam.zoom)

    def draw_texture(self, rend, entity):
        texture = rend.texture

        if rend.sub_modif:
            rend.vertex_list.colors[:] = rend.colors

    def on_draw(self):
        self.cam.apply_transform()
        if self.debug_draw:
            Physics.space.debug_draw(self.opt)

        if Renderable.bg_image:
            #TODO: blit HIDING mask on Car texture so if it on hiden segment
            Renderable.bg_image.texture.blit(0, 0)

        Renderable.batch.draw()

        self.cam.restore_transform()

        uip = self.world.get_processor(UIProcessor)
        if uip:
            uip.draw()

        if self.debug_draw:
            self.fps_display.draw()

