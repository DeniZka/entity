from app.cmp import Component


class Cannon(Component):
    def __init__(self, max_timeout):
        self.max_timeout = max_timeout
        self.time = 0
        self.fired = False
