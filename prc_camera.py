from prc import Processor
from pymunk import Vec2d
from pyglet.gl import *
import math


class CameraProcessor(Processor):
    
    hres = Vec2d(800, 600)

    def __init__(self, resolution, pos=Vec2d(100,100), target=None):
        self.pos = Vec2d(0, 0)
        self.target = None
        self.use_target_angle = False
        self.angle = 0

        self.zoom = 1

        self.pos = pos
        self.target = target
        CameraProcessor.hres = resolution / 2
        self.process(0)


    def process(self, dt):
        if self.target:
            self.pos = self.target.position
            if self.use_target_angle:
                self.angle = self.target.angle
        #TODO: cam can moove when target speed up

    def on_add(self, proc):
        if proc == self and self.world.win_hnd:
            self.sub_id = self.world.win_hnd.subscribe("on_resize", self.on_win_resize)

    def on_remove(self):
        if self.world.win_hnd:
            self.world.win_hnd.unsubscribe("on_resize", self.sub_id)

    def on_win_resize(self, width, height):
        CameraProcessor.hres = Vec2d(width/2, height/2)

    def resize(self, resolition):
        CameraProcessor.hres = resolition/2

    def set_target(self, body):
        self.target = body
        self.pos = self.target.position
        if self.use_target_angle:
            self.angle = self.target.angle

    def to_world(self, screen):
        sub_v = (screen - CameraProcessor.hres) / self.zoom
        sub_v.rotate(self.angle)
        v = self.pos + sub_v
        return v

    def drag(self, dv):
        if self.target:
            return
        sv = dv / self.zoom
        sv.rotate(self.angle)
        self.pos -= sv

    def shift_to_mouse(self, screen, z_mul):
        if self.target:
            return
        wrld = self.to_world(screen)
        v = wrld - self.pos
        self.pos = self.pos + v * z_mul

    def shift_from_mouse(self, screen, z_mul):
        if self.target:
            return
        wrld = self.to_world(screen)
        v = wrld - self.pos
        self.pos = self.pos - v * z_mul

    def zoom_step(self, step):
        self.zoom = self.zoom + self.zoom * step

    def set_target(self, body):
        self.target = body

    def apply_transform(self):
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        glPushMatrix()

        glTranslatef(CameraProcessor.hres[0], CameraProcessor.hres[1], 0) #move to 0 to rotate correctly

        glScalef(self.zoom, self.zoom, 1)

        deg = math.degrees(self.angle)
        glRotatef(-deg, 0, 0, 1)

        gluLookAt(self.pos[0], self.pos[1], 1.0,
                  self.pos[0], self.pos[1], -1.0,
                  0.0, 1.0, 0.0) #move to target

    def restore_transform(self):
        glPopMatrix()
