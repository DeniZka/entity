from cmp import Component

"""
Segments terminal
"""

class Joint(Component):

    def __init__(self, id, pos, seg_id):
        self.id = id
        self.ins = [seg_id, -1]
        self.outs = [-1, -1]
        self.ways = 1
        self.pos = pos
        self.sw_out = -1 #index of output
        self.sw_in = -1  #index of input in cross

    def attach(self, seg_id):
        """
        try to attach another joint
        :return: number of ways
        """
        if self.ways == 1:
            self.ways = 2
            self.outs[0] = seg_id
            self.sw_out = 0
            return self.ways
        if self.ways == 2:
            self.ways = 3
            self.outs[1] = seg_id
            return self.ways
        if self.ways == 3:
            self.ins[1] = seg_id
            self.ways = 4
            return self.ways

    def flip(self):
        """
        for threeway is one of output
        for fourway is one of output for first input
            another one for second input (fipable only in editor)
        :return:
        """
        if self.ways == 3:
            if self.sw_out == 0:
                self.sw_out = 1
            else:
                self.sw_out = 0

    def next(self, src):
        """
        :param src:
        :return: next available segment
        """
        if self.ways == 1:
            return None
        if self.ways == 2:
            if src == self.ins[0]:
                return self.outs[0]
            else:
                return self.ins[0]
        if self.ways == 3:
            if src == self.ins[0]:
                return self.outs[self.sw_out]
            else:
                return self.ins[0]
        if self.ways == 4:
            if src == self.ins[0]:
                return self.outs[self.sw_out]
            if src == self.ins[1]:
                return self.outs[self.sw_out-1]
            if src == self.outs[0]:
                return self.ins[self.sw_out]
            if src == self.outs[1]:
                return self.outs[self.sw_out - 1]


