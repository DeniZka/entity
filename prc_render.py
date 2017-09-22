from pyglet.gl import *
import esper
from cmp_renderable import Renderable
from pymunk import Vec2d
from cmp_physics import Physics


class TextureRenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        Renderable.batch = pyglet.graphics.Batch()

    def process(self, dt):
        # This will iterate over every Entity that has this Component, and
        # add the texture associated with the Renderable Component instance
        # and its vertice_list to the render batch. The batch will then be
        # drawn by the 'on_draw' event handler of teh main window:
        for entity, renderable in self.world.get_component(Renderable):
            self.draw_texture(renderable, entity)

    def draw_texture(self, rend, entity):
        texture = rend.texture

        if rend.vertex_list is None:

            vertex_format = 'v2f/stream'
            rend.vertex_list = Renderable.batch.add(4, GL_QUADS,
                                                    rend.group,
                                                    vertex_format, 'c4B/stream',
                                                    ('t3f/static', texture.tex_coords))
        if rend.sub_modif:
            rend.vertex_list.colors[:] = rend.colors

        hw = rend.w * 0.5
        hh = rend.h * 0.5
        v1 = Vec2d(-hw, -hh)
        v1.rotate(rend.angle)
        v1 += rend.pos
        v2 = Vec2d( hw, -hh)
        v2.rotate(rend.angle)
        v2 += rend.pos
        v3 = Vec2d(hw, hh)
        v3.rotate(rend.angle)
        v3 += rend.pos
        v4 = Vec2d(-hw, hh)
        v4.rotate(rend.angle)
        v4 += rend.pos
        rend.vertex_list.vertices[:] = [v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, v4.x, v4.y]

