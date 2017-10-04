from prc import Processor
from pyglet.gl import *
from cmp_renderable import Renderable
from cmp_renderables import Renderables
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
            if tr.modified:
                self.update_verts(tr, rend)

        for e, (tr, rends) in self.world.get_components(Transform, Renderables):
            if tr.modified:
                for r in rends.renderable:
                    self.update_verts(tr, r)

    def update_verts(self, tr, rend):
        if rend.sub_modif:
            rend.vertex_list.colors[:] = rend.colors

        if rend.atype == GL_LINES:
            rend.vertex_list.vertices[:] = [tr._pos[0].x, tr._pos[0].y, tr._pos[1].x, tr._pos[1].y]
            #make tratsform unmodified
            tr.redrawed()
        else:
            #quads
            v1 = -tr.anchor
            v1.rotate(tr.angle)
            v1 = v1 + tr.pos

            v2 = Vec2d((tr.w - tr.anchor.x), -tr.anchor.y)
            v2.rotate(tr.angle)
            v2 = v2 + tr.pos

            v3 = Vec2d((tr.w - tr.anchor.x), (tr.h - tr.anchor.y))
            v3.rotate(tr.angle)
            v3 = v3 + tr.pos

            v4 = Vec2d(-tr.anchor.x, (tr.h - tr.anchor.y))
            v4.rotate(tr.angle)
            v4 = v4 + tr.pos
            rend.vertex_list.vertices[:] = [v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, v4.x, v4.y]
            #made unmodified
            tr.redrawed()

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

