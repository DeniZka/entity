from prc import Processor
from cmp_physics import Physics
from cmp_input import Input
from pymunk import Vec2d
from cmp_cannon import Cannon


class InputProcessor(Processor):
    def __init__(self, factory):
        self.factory = factory
        return

    def process(self, dt):
        for ent, (inp, phy) in self.world.get_components(Input, Physics):
            if Input.inps['throttle'][inp.group]:
                fv = Vec2d(0, 2100)
                fv.rotate(phy.body.angle)
                phy.body.force = fv

            if Input.inps['prop_brk'][inp.group]:
                fv = Vec2d(0, -2000)
                fv.rotate(phy.body.angle)
                phy.body.force = fv

            if Input.inps['prop_lft'][inp.group]:
                phy.body.torque = 10000
            else:
                phy.body.torque = 0

            if Input.inps['prop_rgh'][inp.group]:
                phy.body.torque = -10000

            if Input.inps['fire'][inp.group] and self.world.has_component(ent, Cannon):
                can = self.world.component_for_entity(ent, Cannon)
                if not can.fired:
                    can.fired = True
                    bp = Vec2d(0, 32+3)
                    bp.rotate(phy.body.angle)
                    pos = phy.body.position + bp
                    self.factory.createBullet(pos, phy.body)

            if not Input.inps['fire'][inp.group] and self.world.has_component(ent, Cannon):
                can = self.world.component_for_entity(ent, Cannon)
                can.fired = False