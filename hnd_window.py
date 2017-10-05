import pyglet
from pymunk import Vec2d
from pyglet.gl import *
from pyglet.window import key
from cmp_renderable import Renderable
from cmp_input import Input
import time
import math
from cmp_physics import Physics

class WindowHandler(pyglet.window.Window):
    RESOLUTION = 720, 480
    FPS = 60
    dt_cnt = 0
    dt_lim = 1.0 / FPS

    def __init__(self,  debug_draw=True):
        super().__init__(width=WindowHandler.RESOLUTION[0], height=WindowHandler.RESOLUTION[1],
                         resizable=True)
        self.win_subs = {}
        self.sub_id = 0 #subscribers identifier
        BGCOLOR = (0.2, 0.2, 0.2, 1.0)
        pyglet.gl.glClearColor(*BGCOLOR)
        self.set_caption("Esper pyglet Example")


        for k in Input.inps:
            for i in range(Input.inp_grps):
                Input.inps[k][i] = False

        self.alive = True
        self.last_time = time.time()

        self.target_backup = None

    def subscribe(self, method, cb_func):
        self.sub_id += 1
        if method in self.win_subs:
            self.win_subs[method].append((self.sub_id, cb_func))
        else:
            self.win_subs[method] = [(self.sub_id, cb_func)]
        return self.sub_id

    def unsubscribe(self, method, id):
        if method not in self.win_subs:
            return

        for i in range(len(self.win_subs[method])):
            if self.win_subs[method][i][0] == id:
                del self.win_subs[method][i]
                return


    def on_resize(self, width, height):
        super().on_resize(width, height)
        for sub in self.win_subs["on_resize"]:
            sub[1](width, height)

    def add_ui_processor(self, uip):
        self.uip = uip

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
            return

        for sub in self.win_subs["on_key_press"]:
            sub[1](symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for sub in self.win_subs["on_key_release"]:
            sub[1](symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for sub in self.win_subs["on_mouse_motion"]:
            sub[1](x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for sub in self.win_subs["on_mouse_press"]:
            sub[1](x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for sub in self.win_subs["on_mouse_release"]:
            sub[1](x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for sub in self.win_subs["on_mouse_scroll"]:
            sub[1](x, y, scroll_x, scroll_y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for sub in self.win_subs["on_mouse_drag"]:
            sub[1](x, y, dx, dy, buttons, modifiers)

    def on_draw(self):
        self.clear()
        for sub in self.win_subs["on_draw"]:
            sub[1]()
