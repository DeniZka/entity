from cmp import Component

"""
Segments terminal
"""

class Joint(Component):

    def __init__(self, pos, seg_id, ways=1):
        self.seg_ids = [seg_id]
        self.ways = ways
        self.pos = pos

    """
    try to attach another joint
    """
    def attach(self, pos, seg_id):
        if self.ways < 4:
            self.segs.append(seg_id)
            return self.pos
        else:
            return pos