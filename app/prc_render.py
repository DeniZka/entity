import time

from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.graphics import OrderedGroup
from pymunk.pyglet_util import DrawOptions
from pyglet.text import Label

from app.cmp_renderable import Renderable
from app.cmp_transform import Transform
from app.cmp_segment import Segment
from app.prc import Processor
from app.prc_camera import CameraProcessor
from app.prc_ui import UIProcessor


class TextureRenderProcessor(Processor):

    def __init__(self, debug_draw = True):
        super().__init__()
        Renderable.batch = pyglet.graphics.Batch()
        Renderable.ui_batch = pyglet.graphics.Batch()
        Renderable.bg = RendOrderGroup(0)
        Renderable.mg = RendOrderGroup(1)
        Renderable.fg = RendOrderGroup(2)
        Renderable.ui = RendOrderGroup(3)
        Renderable.fat_line = FatLineOrderGroup(4)
        Renderable.fat_point = FatPointGroup()

        self.cam = None
        self.width = 800
        self.height = 600
        self.hw = self.width * 0.5
        self.hh = self.height * 0.5

        self.debug_draw = debug_draw
        self.debug_draw = debug_draw
        if debug_draw:
            self.opt = DrawOptions()
            #            self.opt.shape_static_color
            self.fps_display = pyglet.clock.ClockDisplay()

    def on_add(self, proc):
        if proc == self:
            self.sub_id = self.world.win_hnd.subscribe("on_draw", self.on_draw)
            self.sub_id = self.world.win_hnd.subscribe("on_resize", self.on_resize)
        if proc.__class__ is CameraProcessor:
            self.cam = proc

    def on_resize(self, width, height):
        self.width = width
        self.height = height
        self.hw = self.width * 0.5
        self.hh = self.height * 0.5

    def on_remove(self):
        self.world.win_hnd.unsubscribe("on_draw", self.sub_id)

    def process(self, dt):
        for e, (tr, rend) in self.world.get_components(Transform, Renderable):
            if rend.modified:
                for vl in rend.vertex_list:
                    try:
                        vl.colors[:] = rend.colors
                    except:
                        print ("Entity rendering problem:", e)
                        exit()
        for e, (seg, rend) in self.world.get_components(Segment, Renderable):
            if seg.modified:
                rend.vertex_list[0].vertices[:] = seg.vertices
                rend.vertex_list[1].vertices[:] = seg.vertices
                rend.vertex_list[0].colors[:] = rend.colors
                #print(seg.vertices)

            #if tr.modified(self.cam.zoom):
                #for vl in rend.vertex_list:
                #    if rend.atype == GL_POINTS:
                #        vl.vertices[:] = [tr.g_pos.x, tr.g_pos.y]
                #        tr.redrawed()
                #elif rend.atype == GL_LINES:
                #    v1 = tr.g_pos
                #    v2 = tr.g_pos1
                #    rend.vertex_list.vertices[:] = [v1.x, v1.y, v2.x, v2.y]
                    # make tratsform unmodified
                #    tr.redrawed()
                #elif rend.atype == GL_QUADS:
                #    rend.vertex_list.vertices[:] = tr.vertixes(self.cam.zoom)

        #for e, (tr, l) in self.world.get_components(Transform, Label):
        #    if tr.modified:
        #        l.x = int(tr.g_pos.x)
        #        l.y = int(tr.g_pos.y)

    def draw_texture(self, rend, entity):
        texture = rend.texture

        if rend.sub_modif:
            rend.vertex_list.colors[:] = rend.colors

    def on_draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


        self.cam.apply_transform()
        #if self.debug_draw:
        #    Physics.space.debug_draw(self.opt)

        if Renderable.bg_image:
            #TODO: blit HIDING mask on Car texture so if it on hiden segment
            Renderable.bg_image.texture.blit(0, 0)

        #t1 = time.time()
        Renderable.batch.draw()
        #t2 = time.time()
        #print (1/(t2-t1))

        self.cam.restore_transform()

        uip = self.world.get_processor(UIProcessor)
        if uip:
            uip.draw()

        if self.debug_draw:
            self.fps_display.draw()



class RendOrderGroup(OrderedGroup):
    def __init__(self, order, parent=None):
        super().__init__(order, parent)

    def set_state(self):
        return
        #this added grlobaly
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class FatLineOrderGroup(OrderedGroup):
    def __init__(self, order, parent=None):
        super().__init__(order, parent)

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