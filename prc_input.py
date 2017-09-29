from prc import Processor
from cmp_physics import Physics
from cmp_input import Input
from pymunk import Vec2d
from cmp_cannon import Cannon
from prc_camera import CameraProcessor
from pyglet.window import key
import math


class InputProcessor(Processor):
    def __init__(self, factory):
        self.map = { #map keys for actions and groups
                      #action     group
            key.UP:    ('throttle', 0),
            key.DOWN:  ('prop_brk', 0),
            key.LEFT:  ('prop_lft', 0),
            key.RIGHT: ('prop_rgh', 0),
            key.RETURN: ('fire', 0),
            key.W: ('throttle', 1),
            key.A: ('prop_lft', 1),
            key.S: ('prop_brk', 1),
            key.D: ('prop_rgh', 1),
            key.SPACE: ('fire', 1)
        }

        self.factory = factory
        self.cam = None
        self.zoom_mul = 0.1
        return

    def on_add(self):
        if self.world.win_hnd:
            self.sub_id = self.world.win_hnd.subscribe("on_key_press", self.on_key_press)
            self.world.win_hnd.subscribe("on_key_release", self.on_key_release)
            self.world.win_hnd.subscribe("on_mouse_press", self.on_mouse_press)
            self.world.win_hnd.subscribe("on_mouse_scroll", self.on_mouse_scroll)
            self.world.win_hnd.subscribe("on_mouse_drag", self.on_mouse_drag)

    def on_remove(self):
        if self.world.win_hnd:
            self.world.win_hnd.unsubscribe("on_key_press", self.sub_id)
        #TODO: UNSUBSCRIBE

    def get_cam(self):
        self.cam = self.world.get_processor(CameraProcessor)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.DELETE:
            self.cam.angle = self.cam.angle + math.radians(10)
            return
        if symbol == key.PAGEDOWN:
            self.cam.angle = self.cam.angle + math.radians(-10)
            return
        if symbol == key.NUM_0:
            if self.cam.target:
                self.target_backup = self.cam.target
                self.cam.target = None
            return
        if symbol == key.NUM_1:
            if self.target_backup:
                self.cam.target = self.target_backup
        if symbol == key.END:
            self.cam.angle = 0
            return
        if symbol in self.map:
            (k, g) = self.map[symbol]
            Input.inps[k][g] = True

    def on_key_release(self, symbol, modifiers):
        if symbol in self.map:
            (k, g) = self.map[symbol]
            Input.inps[k][g] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.cam.to_world(Vec2d(x,y))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0: #zoom in
            self.cam.zoom_step(self.zoom_mul)
            self.cam.shift_to_mouse(Vec2d(x,y), self.zoom_mul) #not in center
        if scroll_y < 0: #zoom out
            self.cam.zoom_step(-self.zoom_mul)
            self.cam.shift_from_mouse(Vec2d(x, y), self.zoom_mul) #not in center

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if (buttons == 4):  # 1-left, 2-mid, 4-right
            self.cam.drag(Vec2d(dx,dy))

    def process(self, dt):
        if not self.cam:
            self.get_cam()

        for ent, (inp, phy) in self.world.get_components(Input, Physics):
            if Input.inps['throttle'][inp.group]:
                fv = Vec2d(0, 2100)
                fv.rotate(phy.body.angle)
                phy.body.force = fv

            if Input.inps['prop_brk'][inp.group]:
                fv = Vec2d(0, -2000)
                fv.rotate(phy.body.angle)
                phy.body.force = fv

            if Input.inps['prop_lft'][inp.group]:
                phy.body.torque = 10000
            else:
                phy.body.torque = 0

            if Input.inps['prop_rgh'][inp.group]:
                phy.body.torque = -10000

            if Input.inps['fire'][inp.group] and self.world.has_component(ent, Cannon):
                can = self.world.component_for_entity(ent, Cannon)
                if not can.fired:
                    can.fired = True
                    bp = Vec2d(0, 32+3)
                    bp.rotate(phy.body.angle)
                    pos = phy.body.position + bp
                    self.factory.createBullet(pos, phy.body)

            if not Input.inps['fire'][inp.group] and self.world.has_component(ent, Cannon):
                can = self.world.component_for_entity(ent, Cannon)
                can.fired = False