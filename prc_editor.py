from prc import Processor
from cmp_joint import Joint
from cmp_segment import Segment
from cmp_renderable import Renderable
from prc_camera import CameraProcessor
from pymunk import Vec2d
from factory import Factory


class EditorProcessor(Processor):

    def __init__(self):
        self.subscribed = False
        self.sq_sense_rad = 10
        self.cam = None
        self.picked = None
        return

    def on_add(self):
        self.world.win_hnd.subscribe("on_mouse_press", self.on_mouse_press)
        self.world.win_hnd.subscribe("on_mouse_drag", self.on_mouse_drag)
        self.world.win_hnd.subscribe("on_mouse_release", self.on_mouse_release)

    def in_target(self, tgt, pick):
        r = tgt.pos1 - pick
        if r.get_length_sqrd() < self.sq_sense_rad:
            return tgt.pos1
        r = tgt.pos2 - pick
        if r.get_length_sqrd() < self.sq_sense_rad:
            return tgt.pos2
        return None

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.cam:
            self.cam = self.world.get_processor(CameraProcessor)
        if button == 1:
            v = self.cam.to_world(Vec2d(x, y))
            factory = self.world.get_processor(Factory)
            found = False
            for ent, (seg, rend) in self.world.get_components(Segment, Renderable):
                self.picked =  self.in_target(seg, v)
                if self.picked:
                    found = True
                    break

            if not found:
                factory.create_segment(v)
                self.picked = v

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.picked:
            w = self.cam.to_world(Vec2d(x, y))
            self.picked.x = w.x
            self.picked.y = w.y

    def on_mouse_release(self, x, y, button, modifiers):
        self.picked = None
        #TODO; merge with existing (and IS not self)
        """
        v = self.cam.to_world(Vec2d(x, y))
        for ent, (seg, rend) in self.world.get_components(Segment, Renderable):
            
            tgtv = self.in_target(seg, v)
            if tgtv:
               if tgtv == seg.pos1 and self.picked is not seg.pos1:
                seg
                self
        """

    def process(self, dt):
        return
        #if not self.subscribed:
            #self.world.get

