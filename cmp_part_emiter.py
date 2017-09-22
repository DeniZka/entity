from pymunk import Vec2d


"""Pos and angle updates by body if emitter on it
"""

class ParticleEmiter:
    p_limit = 0 #TODO: remove FIRST added over limit(FIFO). If not Destroyed
    p_list = []

    def __init__(self, pos, angle, timeout, work=True):
        self.work = work
        self.pos_rel = Vec2d(pos) #relative pos, if on some body
        self.pos = pos
        self.angle_rel = angle
        self.angle = angle
        self.timeout = timeout #timeout between emit new entity TODO: some randomize
        self.time = 0
        self.kind = "Engine"
        #self.algo = "TEST"  #algorithm that solves particle behavor -moved to particles

    def off(self):
        self.work = False

    def on(self):
        self.work = True

    def can_emit(self, dt):  #resolve to emit new or not
        if self.work:
            self.time += dt
            if self.time >= self.timeout:
                self.time = 0
                return True

        return False
