from cmp import Component
from pymunk import Vec2d


class Transform(Component):
    """
    check pre_ for to check it was updated
    """
    def __init__(self, pos, w=0, h=0, angle=0):
        self._parent = None  # relative posititoning
        self._childs = []
        self._pos = [
            Vec2d(0, 0),    # for sprite anchor
            Vec2d(0, 0),    # for line
            Vec2d(0, 0),    # for futurer modifible quad
            Vec2d(0, 0)     # for futurer modifible quad
        ]
        self._v = [         # final counted vertixes
            Vec2d(0, 0),    # for sprite anchor
            Vec2d(0, 0),    # for line
            Vec2d(0, 0),    # for futurer modifible quad
            Vec2d(0, 0)     # for futurer modifible quad
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
        self.pre_pos = Vec2d(0, 0) # for check.. update something like graphics or not
        self._angle = angle
        self.pre_angle = self._angle

        self._scale = Vec2d(0, 0)
        self.pre_scale = Vec2d(0, 0)

        self._modified = True  # need to redraw

        self.unzoomable = False # camera zoom does not affect renderable sizes
        self.last_cam_zoom = 1  #

    def _set_modified(self):
        """
        internal usage update modified to True for self and childs
        :return:
        """
        self._modified = True
        for c in self._childs:
            c._modified = True

    def redrawed(self):
        """
        not for childs
        :return:
        """
        self._modified = False


    def modified(self, zoom=None):
        """

        :param zoom: for unzumable transformations only
        :return:
        """
        # check unzumable objects
        if self.unzoomable and zoom:
            if zoom != self.last_cam_zoom:
                self.last_cam_zoom = zoom
                self._set_modified()

        return self._modified

    def other_point(self, val):
        """
        Used for lines with two _pos
        Try to find another end of segment if param is the one of their side
        :param val: one of the segment point
        :return: other point or nothing
        """
        if val == self._pos[0]:
            return self._pos[1]
        if val == self._pos[1]:
            return self._pos[0]
        return None

    def replace_pt(self, self_src, self_dest):
        for i in range(4):
            if self._pos[i] == self_src:
                self._pos[i] = self_dest
                return True
        return False

    @property
    def pos(self):
        return self._pos[0]

    @pos.setter
    def pos(self, val):
        if val != self._pos[0]:
            self._pos[0] = val
            self._set_modified()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        if val != self._angle:
            self._angle = val
            self._set_modified()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        if val != self._scale:
            self._scale = val
            self._set_modified()

    @property
    def x(self):
        if self._parent:
            return self._parent.x + self._pos[0].x
        else:
            return self._pos[0].x

    @x.setter
    def x(self, val):
        """
        Warning!!
        calculate relative position prevous if on _parent!
        :param val:
        :return:
        """
        self._pos[0].x = val
        self._set_modified()

    @property
    def y(self):
        if self._parent:
            return self._parent.y + self._pos[0].y
        else:
            return self._pos[0].y

    @y.setter
    def y(self, val):
        """
        Warning!!
        calculate relative position prevous if on _parent!
        :param val:
        :return:
        """
        self._pos[0].y = val
        self._set_modified()


    @property
    def x1(self):
        if self._parent:
            return self._parent.x + self._pos[1].x
        else:
            return self._pos[1].x

    @x1.setter
    def x1(self, val):
        """
        Warning!!
        calculate relative position prevous if on _parent!
        :param val:
        :return:
        """
        self._pos[1].x = val
        self._set_modified()

    @property
    def y1(self):
        if self._parent:
            return self._parent.y + self._pos[1].y
        else:
            return self._pos[1].y

    @y1.setter
    def y1(self, val):
        """
        Warning!!
        calculate relative position prevous if on _parent!
        :param val:
        :return:
        """
        self._pos[1].y = val
        self._set_modified()

    @property
    def anchor(self):
        return self._anchor

    @property
    def w(self):
        if self.unzoomable:
            return self._w / self.last_cam_zoom
        else:
            return self._w

    @property
    def h(self):
        if self.unzoomable:
            return self._h / self.last_cam_zoom
        else:
            return self._h

    @property
    def scale(self):
        return self._scale

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        if val:
            val._childs.append(self)
            self._parent = val
        else:
            if self.parent:
                self.parent._childs.remove(self)

    def vertixes(self, count):
        return v[:count]

    def scale_to(self, des_wh):
        #rescale
        return



