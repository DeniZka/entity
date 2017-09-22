import esper
import pyglet
from cmp_renderable import Renderable
from pymunk import Vec2d



class UIProcessor(esper.Processor):
    def __init__(self):
        return

    def load_ui(self):
        compass = self.world.create_entity()
        tex = pyglet.resource.image("compass.png").get_texture(True)
        rend = Renderable(tex, group=Renderable.ui)
        rend.pos = Vec2d(100, 100)
        self.world.add_component(compass, rend)

    def process(self, dt):
        return

    def draw(self):
        return