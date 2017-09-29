from cmp import Component
from pymunk import Vec2d


class Section(Component):

    def __init__(self):
        self.joints = (None, None) #left and right joints
        self.curved = False
        self.cur_pt = Vec2d(0,0) #mid point for curve

