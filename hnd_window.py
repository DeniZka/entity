import pyglet
from pymunk import Vec2d
from pyglet.gl import *
from pyglet.window import key
from cmp_renderable import Renderable
from cmp_input import Input
from prc_camera import Camera
import time
import math
from cmp_physics import Physics
from pymunk.pyglet_util import DrawOptions

class WindowHandler(pyglet.window.Window):
    RESOLUTION = 720, 480
    FPS = 60
    dt_cnt = 0
    dt_lim = 1.0 / FPS
    ZOOM_MUL = 0.1

    def __init__(self,  debug_draw=True):
        super().__init__(width=WindowHandler.RESOLUTION[0], height=WindowHandler.RESOLUTION[1])
        BGCOLOR = (0.2, 0.2, 0.2, 1.0)
        pyglet.gl.glClearColor(*BGCOLOR)
        self.set_caption("Esper pyglet Example")

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

        for k in Input.inps:
            for i in range(Input.inp_grps):
                Input.inps[k][i] = False

        self.fps_display = pyglet.clock.ClockDisplay()
        self.alive = True
        self.last_time = time.time()

        self.target_backup = None
        self.debug_draw = debug_draw
        if debug_draw:
            self.opt = DrawOptions()
#            self.opt.shape_static_color

    def add_ui_processor(self, uip):
        self.uip = uip

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        if symbol == key.DELETE:
            Camera.angle = Camera.angle + math.radians(10)
            return
        if symbol == key.PAGEDOWN:
            Camera.angle = Camera.angle + math.radians(-10)
            return
        if symbol == key.NUM_0:
            if Camera.target:
                self.target_backup = Camera.target
                Camera.target = None
            return
        if symbol == key.NUM_1:
            if self.target_backup:
                Camera.target = self.target_backup
        if symbol == key.END:
            Camera.angle = 0
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
            Camera.to_world(Vec2d(x,y))

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y > 0: #zoom in
            Camera.zoom_step(WindowHandler.ZOOM_MUL)
            Camera.shift_to_mouse(Vec2d(x,y), WindowHandler.ZOOM_MUL) #not in center
        if scroll_y < 0: #zoom out
            Camera.zoom_step(-WindowHandler.ZOOM_MUL)
            Camera.shift_from_mouse(Vec2d(x, y), WindowHandler.ZOOM_MUL) #not in center

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if (buttons == 4):  # 1-left, 2-mid, 4-right
            Camera.drag(Vec2d(dx,dy))

    def on_draw(self):
        self.clear()
        Camera.apply_transform()
        if self.debug_draw:
            Physics.space.debug_draw(self.opt)
        Renderable.batch.draw()

        Camera.restore_transform()
        #ui
        if self.uip:
            Renderable.ui_batch.draw()
        self.fps_display.draw()



