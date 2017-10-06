import random

from code.cmp import Component


class TempLive(Component):
    TTL_INFINITY = 0

    def __init__(self, ttl, dtt=0):
        if dtt > 0:
            self.ttl = random.triangular(ttl-dtt, ttl+dtt)
        else:
            self.ttl = ttl
        self.tl = 0

    def alive(self, dt):
        if self.ttl != TempLive.TTL_INFINITY:
            self.tl += dt
            if self.tl >= self.ttl:
                return False
            else:
                return True
