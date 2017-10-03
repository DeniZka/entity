from prc import Processor
from cmp_joint import Joint
from cmp_transform import Transform
from cmp_segment import Segment
from cmp_renderable import Renderable
from cmp_renderables import Renderables
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

    def on_add(self, proc):
        if proc == self:
            self.cam = self.world.get_processor(CameraProcessor)
            self.world.win_hnd.subscribe("on_mouse_press", self.on_mouse_press)
            self.world.win_hnd.subscribe("on_mouse_drag", self.on_mouse_drag)
            self.world.win_hnd.subscribe("on_mouse_release", self.on_mouse_release)
        if proc.__class__ is CameraProcessor:
            self.cam = proc

    def in_target(self, tgt, pick):
        r = tgt.pos - pick
        if r.get_length_sqrd() < self.sq_sense_rad:
            return tgt
        return None

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            v = self.cam.to_world(Vec2d(x, y))
            factory = self.world.get_processor(Factory)
            found = False
            for ent, (tr, jnt) in self.world.get_components(Transform, Joint):
                self.picked = self.in_target(tr.pos[0], v)
                if self.picked:
                    print("FOUND", v)
                    found = True
                    break

            if not found:
                rend = factory.create_segment(v)
                self.picked = rend

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.picked:
            w = self.cam.to_world(Vec2d(x, y))
            print("DRAG", w)
            self.picked.pos = w #update the POS,not the x y. This will update vertex

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

