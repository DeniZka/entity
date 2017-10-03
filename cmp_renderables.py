from cmp_renderable import Renderable

"""
For those entity, who have more then one sprite
"""

class Renderables():

    def __init__(self, renderable):
        self.renderable = [renderable]

    def add_renderable(self, renderable):
        self.renderable.append(renderable)

    def del_renderable(self, renderable):
        self.renderable.remove(renderable)