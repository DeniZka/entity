from cmp import Component

class Input(Component):
    inp_grps = 2

    inps = {  # active keys
        'throttle': {},
        'prop_brk': {},
        'prop_lft': {},
        'prop_rgh': {},
        'fire': {}
    }
    def __init__(self, group):
        self.group = group #for example two players on pc
