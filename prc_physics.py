import esper
import pymunk
from pymunk import Vec2d
from cmp_physics import Physics
from factory import Factory
from cmp_hp import Hp
from prc_partciles import ParticleProcessor

class PhysicsProcessor(esper.Processor):
    def __init__(self):
        Physics.space = pymunk.Space()
        Physics.space.gravity = Vec2d(0.0, -9.78)
        Physics.space.sleep_time_threshold = 0.3
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
                if hp.hp > 1:
                    hp.hp -= 1
                else:
                    self.world.delete_entity(arbiter.shapes[1].entity)
