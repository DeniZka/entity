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

        self.modified = True # need to redraw
        self.drag_id = 0 #id of default modificable vector

    def other_point(self, val):
        """
        Try to find another end of segment if param is the one of ther side
        :param val: one of the segment point
        :return: other point or nothing
        """
        if val == self._pos[0]:
            return self._pos[1]
        if val == self._pos[1]:
            return self._pos[0]
        return None

    def pick_pt_drag_id(self, val):
        """
        swap default moveable pos vector if it posible
        :param val: vector to set as movable
        """
        for i in range(4):
            if self._pos[i] is val:
                self.drag_id = i
                return True
        return False

    def redrawed(self):
        self.modified = False

    @property
    def pos(self):
        return self._pos[self.drag_id]

    @pos.setter
    def pos(self, val):
        if val != self._pos[self.drag_id]:
            self._pos[self.drag_id] = val
            self.modified = True

    """
    FIRST SELECT BY pick drag id !!!
    @property
    def pos1(self):
        return self._pos[1]

    @pos1.setter
    def pos1(self, val):
        if val != self._pos[1]:
            self._pos[1] = val
            self.modified = True
    """

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        if val != self._angle:
            self._angle = val
            self.modified = True

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        if val != self._scale:
            self._scale = val
            self.modified = True

    @property
    def x(self):
        return self._pos[self.drag_id].x

    @x.setter
    def x(self, val):
        self._pos[self.drag_id].x = val
        self.modified = True

    @property
    def y(self):
        return self._pos[self.drag_id].y

    @y.setter
    def y(self, val):
        self._pos[self.drag_id].y = val
        self.modified = True

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



