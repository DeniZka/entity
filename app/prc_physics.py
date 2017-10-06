import pymunk
from pymunk import Vec2d

from app.cmp_hp import Hp
from app.cmp_physics import Physics
from app.prc import Processor
from app.prc_partciles import ParticleProcessor


class PhysicsProcessor(Processor):

    def __init__(self):
        Physics.space = pymunk.Space()
        Physics.space.iterations = 5
        Physics.space.gravity = Vec2d(0.0, 0.0)
        Physics.space.sleep_time_threshold = 0.3
        Physics.space.damping = 0.5
        #collision handle
        ch = Physics.space.add_collision_handler(
            Physics.coll_types["p_bullet"],
            Physics.coll_types["walls"]
        )
        ch.post_solve = self.bullet_in_wall

        ch1 = Physics.space.add_collision_handler(
            Physics.coll_types["p_bullet"],
            Physics.coll_types["enemy"]
        )
        ch1.post_solve = self.bullet_in_enemy

    def process(self, dt):
        Physics.space.step(dt)
        for ent, phy in self.world.get_component(Physics):
            phy.update_renderable()
            phy.update_emiters()

    def bullet_in_wall(self, arbiter, space, data):
        #create splat
        pp = self.world.get_processor(ParticleProcessor)
        pp.addSparks(arbiter.shapes[0].body.position)
        #remove entity
        self.world.delete_entity(arbiter.shapes[0].entity)

    def bullet_in_enemy(self, arbiter, space, data):
        self.world.delete_entity(arbiter.shapes[0].entity)
        for ent, (hp, phy) in self.world.get_components(Hp, Physics):
            if phy.shape == arbiter.shapes[1]:
                hp.hp -= 1
                if hp.hp == 0:
                    self.world.delete_entity(ent)
