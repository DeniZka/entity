from pymunk import Vec2d
from cmp import Component
"""
    IF Physics component will destroyed the renderable and emitter could be alive
"""


class Physics(Component):

    coll_types = { #to handle collision from types
        "player":   0,
        "enemy":    1,
        "p_bullet": 2,
        "e_bullet": 3,
        "walls":    4
    }
    cats = { #physical categories
        "player":    0x00000001,
        "enemy":     0x00000002,
        "p_bullet":  0x00000004,
        "e_bullet":  0x00000008,
        "walls":     0x00000010,
        "particles": 0x00000020,
        "all":       0xffffffff
    }
    masks = { #collision masks
        "player":  cats["player"] + cats["enemy"] + cats["walls"] + cats["e_bullet"],
        "enemy": cats["player"] + cats["enemy"] + cats["walls"] + cats["p_bullet"],
        "p_bullet": cats["enemy"] + cats["walls"] + cats["e_bullet"],
        "e_bullet": cats["player"], # + cats["walls"] + cats["p_bullet"],
        "particles": cats["walls"], # + cats["enemy"] + cats["player"],
        "walls": cats["all"]


    }
    coll_grp = {
        "no": 0, #default
        "bullet": 1,
        "clouds": 2
    }

    space = None #easy access to pymunk space from everywhere

    def __init__(self, body, shape, renderable=None, emiters=[]):
        self.body = body
        self.shape = shape
        self.renderable = []
        if renderable:
            self.renderable.append(renderable) #for update them
            self.renderable[-1].pos = body.position
        self.emiters = emiters #for update them
        Physics.space.add(self.body, self.shape)

    def on_remove (self, with_sprites=True):
        Physics.space.remove(self.body, self.shape)  # remove self from world

    def add_renderable(self, rend):
        self.renderable.append(rend)

    def update_renderable(self):
        for r in self.renderable:
            if r:
                r.pos = self.body.position
                r.angle = self.body.angle

    def add_emiter(self, emiter):
        self.emiters.append(emiter)

    def update_emiters(self):
        for e in self.emiters:
            if e:
                rel_rot = Vec2d(e.pos_rel)
                rel_rot.rotate(self.body.angle)
                e.pos = self.body.position + rel_rot
                e.angle = self.body.angle + e.angle_rel
