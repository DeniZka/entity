from cmp import Component
from pymunk import Vec2d


class Transform(Component):
    """
    check pre_ for to check it was updated
    """
    def __init__(self, pos, w=0, h=0, angle=0):
        self._pos = [
            Vec2d(0, 0), #for sprite anchor
            Vec2d(0, 0), #for line
            Vec2d(0, 0),    #for futurer modifible quad
            Vec2d(0, 0)     #for futurer modifible quad
        ]
        if pos:
            self._pos[0] = pos
        self._anchor = Vec2d(0.0, 0.0)
        self._w = 0
        if w:
            self._w = w
            self._anchor.x = w/2
        self._h = 0
        if h:
            self._h = h
            self._anchor.y = h/2
        self.pre_pos = Vec2d(0, 0) #for check.. update something like graphics or not
        self._angle = angle
        self.pre_angle = self._angle

        self._scale = Vec2d(0, 0)
        self.pre_scale = Vec2d(0, 0)

    def pos_modified(self):
        if self.pos[0] != self.pre_pos:
            return True
        else:
            return False

    def angle_modified(self):
        if self.angle != self.pre_angle:
            return True
        else:
            return False

    def scale_modified(self):
        if self.scale != self.pre_scale:
            return True
        else:
            return False

    @property
    def pos(self):
        return self._pos[0]

    @pos.setter
    def pos(self, val):
        if val != self._pos[0]:
            self.pre_pos = Vec2d(self._pos[0])
            self._pos[0] = val

    @property
    def pos1(self):
        return self._pos[1]

    @pos1.setter
    def pos1(self, val):
        if val != self._pos[1]:
            self._pos[1] = val

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        if val != self._angle:
            self.pre_angle = self._angle
            self._angle = val

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        if val != self._scale:
            self.pre_scale = self._scale
            self._scale = val

    @property
    def anchor(self):
        return self._anchor

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return  self._h

    def scale_to(self, des_wh):
        #rescale
        return



