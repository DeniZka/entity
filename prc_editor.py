from prc import Processor
from cmp_joint import Joint
from cmp_renderable import Renderable
from prc_camera import CameraProcessor
from pymunk import Vec2d
from factory import Factory


class EditorProcessor(Processor):

    def __init__(self):
        self.subscribed = False
        self.sq_sense_rad = 10 * 10
        self.cam = None
        return


    def on_add(self):
        self.world.win_hnd.subscribe("on_mouse_press", self.on_mouse_press)
        self.world.win_hnd.subscribe("on_mouse_drag", self.on_mouse_drag)
        self.world.win_hnd.subscribe("on_mouse_release", self.on_mouse_release)

    def in_target(self, tgt, pick):
        r = tgt - pick
        if r.get_length_sqrd() < self.sq_sense_rad:
            return True
        else:
            return False

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.cam:
            self.cam = self.world.get_processor(CameraProcessor)
        if button == 1:
            v = self.cam.to_world(Vec2d(x, y))
            factory = self.world.get_processor(Factory)
            found = False
            for ent, (jnt, rend) in self.world.get_components(Joint, Renderable):
                if self.in_target(rend.pos, v):
                    jnt.on_mouse = True
                    found = True
                    break

            if not found:
                j = factory.create_joint(v)
                j = factory.create_joint(v)
                j.on_mouse = True


        #pick a part
        #if no part add 1: start joint, 2:mid, 3:end, 4:line
        #if part - attach start point
        return

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.cam:
            self.cam = self.world.get_processor(CameraProcessor)
        if button == 1:
            for ent, (jnt, rend) in self.world.get_components(Joint, Renderable):
                if jnt.on_mouse:
                    jnt.on_mouse = False
                    break


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.cam:
            self.cam = self.world.get_processor(CameraProcessor)
#        if (buttons == 4):  # 1-left, 2-mid, 4-right
        if buttons == 1:
            for ent, (jnt, rend) in self.world.get_components(Joint, Renderable):
                if jnt.on_mouse:
                    v = self.cam.to_world(Vec2d(x, y))
                    rend.pos = v

    def process(self, dt):
        return
        #if not self.subscribed:
            #self.world.get

