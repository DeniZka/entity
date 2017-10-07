from app.cmp import Component


class ParticleBehave(Component):

    def __init__(self, kind):
        self.kind = kind  # get from emitter