from cmp import Component


class Segment(Component):
    next_id = 0

    def __init__(self, id, pos1, pos2, begin, end, tag="TrackSegment", label=""):
        self.tag = tag
        self.id = id
        self.begin = begin
        self.end = end
        self.pos1 = pos1 #begin is pos
        self.pos2 = pos2 #end id pos
        self.label = label


