from pymunk import Vec2d

from app.cmp import Component
from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.graphics import OrderedGroup


class Transform(Group):
    """
    Hierarchical pyglet group to make object on object
    """
    def on_remove(self): #dummy from Component
        pass

    def __init__(self, pos, size=Vec2d(0, 0), angle=0, anchor=None):
        super().__init__(parent=None)
        """

        :param pos: anchor point position
        :param size: initial size of transformable entity (can be grabed from renderable.size() )
        :param angle: angle in radians
        :param anchor: center of rotation and scaling
        """

        self._bb = [
            Vec2d(0, 0),  # min
            Vec2d(0, 0)   # max
        ]
        self._parent = None  # relative posititoning
        self._ppos = Vec2d(0, 0)  # parent positioning
        self._childs = []
        self._pos = [       # local pos
            Vec2d(0, 0),    # for sprite anchor
            Vec2d(0, 0),    # for line
            Vec2d(0, 0),    # for futurer modifible quad
            Vec2d(0, 0)     # for futurer modifible quad
        ]
        self._v = [       # final counted vertixes
            Vec2d(0, 0),  # for sprite anchor
            Vec2d(0, 0),  # for line
            Vec2d(0, 0),  # for futurer modifible quad
            Vec2d(0, 0)   # for futurer modifible quad
        ]
        self._anchor = Vec2d(0.0, 0.0)
        self._size = size
        self._pos[1] = pos + size
        if anchor:
            self._anchor = anchor
        if pos:
            self._pos[0] = pos



        self.pre_pos = Vec2d(0, 0) # for check.. update something like graphics or not
        self._angle = angle
        self.pre_angle = self._angle

        self._scale = Vec2d(1, 1)
        self.pre_scale = Vec2d(0, 0)

        self._modified = True  #check if need to redraw

        self.unzoomable = False  # camera zoom does not affect renderable sizes
        self.last_cam_zoom = 1   #
        self.update_vertix()
        self.calc_bb()

    def _set_modified(self):
        """
        internal usage update modified to True for self and childs
        :return:
        """
        self._modified = True
        for c in self._childs:
            c._set_modified()
        self.calc_bb()


    def redrawed(self):
        """
        not for childs
        :return:
        """
        self._modified = False

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

    def modified(self, zoom=None):
        if not self.unzoomable:
            return self._modified
        else:
            if zoom and zoom != self.last_cam_zoom:
                self._modified = True
                return self._modified

    @property
    def pos(self):
        """
        :return: local position
        """
        return self._pos[0]

    @pos.setter
    def pos(self, val):
        """
        Sets a local position
        :param val:
        :return:
        """
        if val != self._pos[0]:
            self._pos[0] = val
            self._set_modified()

    @staticmethod
    def recur_pos(tr):
        if tr.parent is None:
            # nothin upper
            if tr.__class__ == Transform:
                return tr.pos
            else:
                return Vec2d(0, 0)
        else:
            #return same parent transformation
            #TODO calc angle and scale
            return Transform.recur_pos(tr.parent) + tr.pos




    @property
    def g_pos(self):
        """
        :return: global position calculated from the parents
        """
        return Transform.recur_pos(self)

        if self.parent and self.parent.__class__ == Transform:
                return self.parent.g_pos + self._pos[0]
        else:
            return self._pos[0]

    @property
    def pos1(self):
        """
        :return: local position
        """
        return self._pos[1]

    @pos1.setter
    def pos1(self, val):
        """
        Sets a local position
        :param val:
        :return:
        """
        if val != self._pos[1]:
            self._pos[1] = val
            self._set_modified()

    @property
    def g_pos1(self):
        """
        :return: global position calculated from the parents
        """
        if self._parent and self.parent is Transform:
            return self._parent.g_pos + self._pos[1]
        else:
            return self._pos[1]

    @property
    def angle(self):
        if self._parent and self.parent is Transform:
            return self._parent.angle + self._angle
        else:
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
        if self._parent and self.parent is Transform:
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
        if self._parent and self.parent is Transform:
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
        if self._parent and self.parent is Transform:
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
        if self._parent and self.parent is Transform:
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

    @anchor.setter
    def anchor(self, val):
        self._anchor = val

    @property
    def w(self):
        if self.unzoomable:
            return self._size.x
        else:
            return self._size.x

    @property
    def h(self):
        if self.unzoomable:
            return self._size.y
        else:
            return self._size.y

    """
    @property
    def parent(self):
        return self._parent
    """

    """
    @parent.setter
    def parent(self, val):
        if val:
            val._childs.append(self)
            self._parent = val
        else:
            if self._parent:
                self._parent._childs.remove(self)
    """

    def scale_to(self, des_wh):
        #TODO rescale
        return

    def calc_bb(self):
        self._bb[0].x = self._v[0].x
        self._bb[0].y = self._v[0].y
        self._bb[1].x = self._v[0].x
        self._bb[1].y = self._v[0].y
        for i in range(1, 4):
            # minimal point
            if self._v[i].x < self._bb[0].x:
                self._bb[0].x = self._v[i].x
            if self._v[i].y < self._bb[0].y:
                self._bb[0].y = self._v[i].y
            # maximal point
            if self._v[i].x > self._bb[1].x:
                self._bb[1].x = self._v[i].x
            if self._v[i].y > self._bb[1].y:
                self._bb[1].y = self._v[i].y

    def get_in_bb(self, pos):
        v = pos - self._pos[0]
        if self._bb[0].x < v.x < self._bb[1].x and \
           self._bb[0].y < v.y < self._bb[1].y:
            return v
        else:
            return None


    def update_vertix(self):
        if self._parent:
            self._ppos.x = self._parent.x
            self._ppos.y = self._parent.y
        self._v[0] = Vec2d(-self._anchor.x * self._scale.x,
                           -self._anchor.y * self._scale.y)
        self._v[0].rotate(self._angle)
        self._v[0] = self._v[0] + self._ppos

        self._v[1] = Vec2d((self._size.x - self._anchor.x) * self._scale.x,
                           -self._anchor.y * self._scale.y)
        self._v[1].rotate(self._angle)
        self._v[1] = self._v[1] + self._ppos

        self._v[2] = Vec2d((self._size.x - self._anchor.x) * self._scale.x,
                           (self._size.y - self._anchor.y) * self._scale.y)
        self._v[2].rotate(self._angle)
        self._v[2] = self._v[2] + self._ppos

        self._v[3] = Vec2d(-self._anchor.x * self._scale.x,
                           (self._size.y - self._anchor.y) * self._scale.y)
        self._v[3].rotate(self._angle)
        self._v[3] = self._v[3] + self._ppos

    def update_vertix_uz(self, zoom):  # FIXME: unzoomable sprites does not show at begin
        if self._parent:
            self._ppos.x = self._parent.x
            self._ppos.y = self._parent.y
        self._v[0] = Vec2d(-self._anchor.x / self.last_cam_zoom,
                           -self._anchor.y / self.last_cam_zoom)
        self._v[0].rotate(self._angle)
        self._v[0] = self._v[0] + self._ppos

        self._v[1] = Vec2d((self._size.x - self._anchor.x) / self.last_cam_zoom,
                           -self._anchor.y / self.last_cam_zoom)
        self._v[1].rotate(self._angle)
        self._v[1] = self._v[1] + self._ppos

        self._v[2] = Vec2d((self._size.x - self._anchor.x) / self.last_cam_zoom,
                           (self._size.y - self._anchor.y) / self.last_cam_zoom)
        self._v[2].rotate(self._angle)
        self._v[2] = self._v[2] + self._ppos

        self._v[3] = Vec2d(-self._anchor.x / self.last_cam_zoom,
                           (self._size.y - self._anchor.y) / self.last_cam_zoom)
        self._v[3].rotate(self._angle)
        self._v[3] = self._v[3] + self._ppos

    def q_verts(self):
        return [0, 0,
                self._pos[1].x-self._pos[0].x, 0,
                self._pos[1].x-self._pos[0].x, self._pos[1].y-self._pos[0].y,
                0, self._pos[1].y-self._pos[0].y]

    def l_verts(self):
        return [0, 0,
                self._pos[1].x-self._pos[0].x, self._pos[1].y-self._pos[0].y]

    def vertixes(self, zoom=None):
        if self.unzoomable:
            if self.last_cam_zoom != zoom or self._modified:
                self.last_cam_zoom = zoom
                self.update_vertix_uz(zoom)
        else:
            if self._modified:
                self.update_vertix()

        self._modified = False
        self.calc_bb()

        return [
            self._v[0].x + self._pos[0].x, self._v[0].y + self._pos[0].y,
            self._v[1].x + self._pos[0].x, self._v[1].y + self._pos[0].y,
            self._v[2].x + self._pos[0].x, self._v[2].y + self._pos[0].y,
            self._v[3].x + self._pos[0].x, self._v[3].y + self._pos[0].y
        ]

    def set_state(self):
        # callback apply local transforamtions
        glPushMatrix()
        glTranslatef(self._pos[0].x, self._pos[0].y, 0.0)
        glRotatef(self._angle, 0.0, 0.0, 1.0)
        glTranslatef(-self._anchor.x, -self._anchor.y, 0.0)
        glScalef(self._scale.x, self._scale.y, 0.0)

    def unset_state(self):
        # callback restore from local transformation
        glPopMatrix()
