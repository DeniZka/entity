from cmp_renderable import Renderable
from cmp import Component

"""
For those entity, who have more then one sprite
"""

class Renderables(Component):

    def __init__(self, renderable):
        self.renderable = [renderable]

    def add_renderable(self, renderable):
        self.renderable.append(renderable)

    def del_renderable(self, renderable):
        self.renderable.remove(renderable)

    def __del__(self):
        for r in self.renderable:
            r.on_remove()
            del r