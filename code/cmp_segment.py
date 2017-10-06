from code.cmp import Component


class Segment(Component):
    next_id = 0

    def __init__(self, id, begin, end, tag="TrackSegment"):
        """

        :param id:   self id (entity)
        :param begin: begin joint entity id
        :param end:   end joint entity id
        :param tag:   type of segment
        """
        self.tag = tag
        self.id = id
        self.begin = begin
        self.end = end

