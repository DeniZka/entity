import math

from pyglet.gl import *
from pymunk import Vec2d

from app.prc import Processor


class CameraProcessor(Processor):
    hres = Vec2d(800, 600)

    def __init__(self, resolution, pos=Vec2d(0, 0), target=None):
        self.pos = Vec2d(0, 0)
        self.target = None
        self.use_target_angle = False
        self._angle = 0
        self._dangle = 0
        self.zoom = 1

        self.pos = pos
        self.target = target
        CameraProcessor.hres = resolution / 2
        self.process(0)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        self._angle = val
        self._dangle = math.degrees(val)

    def process(self, dt):
        if self.target:
            self.pos = self.target.position
            if self.use_target_angle:
                self._angle = self.target.angle
                # TODO: cam can moove when target speed up

    def on_add(self, proc):
        if proc == self and self.world.win_hnd:
            self.sub_id = self.world.win_hnd.subscribe("on_resize", self.on_win_resize)

    def on_remove(self):
        if self.world.win_hnd:
            self.world.win_hnd.unsubscribe("on_resize", self.sub_id)

    def on_win_resize(self, width, height):
        CameraProcessor.hres = Vec2d(width / 2, height / 2)
        glViewport(0, 0, width, height)

    def resize(self, resolition):
        CameraProcessor.hres = resolition / 2

    def set_target(self, body):
        self.target = body
        self.pos = self.target.position
        if self.use_target_angle:
            self._angle = self.target.angle

    def to_world(self, screen):
        """
        Translate screen position to world
        :param screen: Vec2d on screen
        :return: Vec2d of world
        """
        sub_v = (screen - CameraProcessor.hres) / self.zoom
        sub_v.rotate(self._angle)
        v = self.pos + sub_v
        return v

    def to_screen(self, world):
        """
        Translate world vector to screen
        :param world:
        :return:
        """
        sub_v = world - self.pos
        sub_v.rotate(-self._angle)
        sub_v = sub_v * self.zoom + CameraProcessor.hres
        return sub_v

    def drag(self, dv):
        if self.target:
            return
        sv = dv / self.zoom
        sv.rotate(self._angle)
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
        glPushMatrix()
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(- self.hres[0] / self.zoom,
                + self.hres[0] / self.zoom,
                - self.hres[1] / self.zoom,
                + self.hres[1] / self.zoom,
                -1, 1)

        glMatrixMode(gl.GL_MODELVIEW)

        gluLookAt(self.pos[0], self.pos[1], 1.0,
                  self.pos[0], self.pos[1], -1.0,
                  math.sin(-self.angle),
                  math.cos(-self.angle),
                  0.0
                  ) #move to target
        return
        # rotate camera
        glRotatef(-self._dangle, 0.0, 0.0, 1.0)
        # move camera to position
        glTranslatef(-self.pos[0], -self.pos[1], 0)

    def restore_transform(self):
        glPopMatrix()
