from prc import Processor
from pymunk import Vec2d
from pyglet.gl import *
import math


class Camera(Processor):

    pos = Vec2d(0,0)
    target = None
    use_target_angle = False
    angle = 0
    hres = Vec2d(800, 600)
    scale = 1

    def __init__(self, resolution, pos=(100,100), target=None):
        Camera.pos = pos
        Camera.target = target
        Camera.hres = resolution / 2
        self.process(0)

    def process(self, dt):
        if Camera.target:
            Camera.pos = Camera.target.position
            if Camera.use_target_angle:
                Camera.angle = Camera.target.angle
        #TODO: cam can moove when target speed up



    @staticmethod
    def on_resize(width, height):
        Camera.hres = Vec2d(width/2, height/2)

    @staticmethod
    def resize(resolition):
        Camera.hres = resolition/2

    @staticmethod
    def set_target(body):
        Camera.target = body
        Camera.pos = Camera.target.position
        if Camera.use_target_angle:
            Camera.angle = Camera.target.angle

    @staticmethod
    def to_world(screen):
        sub_v = (screen - Camera.hres) / Camera.scale
        sub_v.rotate(Camera.angle)
        v = Camera.pos + sub_v
        return v

    @staticmethod
    def drag(dv):
        if Camera.target:
            return
        sv = dv / Camera.scale
        sv.rotate(Camera.angle)
        Camera.pos -= sv

    @staticmethod
    def shift_to_mouse(screen, z_mul):
        if Camera.target:
            return
        wrld = Camera.to_world(screen)
        v = wrld - Camera.pos
        Camera.pos = Camera.pos + v * z_mul

    @staticmethod
    def shift_from_mouse(screen, z_mul):
        if Camera.target:
            return
        wrld = Camera.to_world(screen)
        v = wrld - Camera.pos
        Camera.pos = Camera.pos - v * z_mul

    @staticmethod
    def zoom_step(step):
        Camera.scale = Camera.scale + Camera.scale * step

    @staticmethod
    def set_target(body):
        Camera.target = body

    @staticmethod
    def apply_transform():
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        glPushMatrix()

        glTranslated(Camera.hres[0], Camera.hres[1], 0) #move to 0 to rotate correctly
        glScalef(Camera.scale, Camera.scale, 1)

        deg = math.degrees(Camera.angle)
        glRotatef(-deg, 0, 0, 1)

        gluLookAt(Camera.pos[0], Camera.pos[1], 1.0,
                  Camera.pos[0], Camera.pos[1], -1.0,
                  0.0, 1.0, 0.0) #move to targer


    @staticmethod
    def restore_transform():
        glPopMatrix()
