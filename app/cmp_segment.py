from app.cmp import Component


class Segment(Component):
    next_id = 0

    def __init__(self, id, pos_b, pos_e, begin, end, tag="TrackSegment"):
        """

        :param id:   self id (entity)
        :param begin: begin joint entity id
        :param end:   end joint entity id
        :param tag:   type of segment
        """
        self._pos = [pos_b, pos_e]
        self.tag = tag
        self.id = id
        self.begin = begin
        self.end = end
        self._modified = True  #means need to correct sprite line

    def _set_modified(self):
        self._modified = True

    @property
    def pos(self):
        return self._pos[0]

    @property
    def modified(self):
        res = self._modified
        self._modified = False
        return res

    @property
    def vertices(self):
        return [self._pos[0].x, self._pos[0].y, self._pos[1].x, self._pos[1].y]


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