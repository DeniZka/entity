import esper
import pymunk
from pymunk import Vec2d
import random
import pyglet
from cmp_part_emiter import ParticleEmiter
from cmp_part_behave import ParticleBehave
from cmp_renderable import Renderable
from cmp_temp_live import TempLive
from cmp_physics import Physics
from cmp_input import Input

"""
ParticleProcessor works with particles: Emit, Move, Destroy

emitters are on some body

particle that has
    part_behave
    ttl           --controled by emitter?
    renderable
    may be (or not) physics
"""

class ParticleProcessor(esper.Processor):
    def __init__(self):
        #self.particles = self.world.create_entity()
        return

    def process(self, dt):
        #check emiters componets to emit more or something
        for ent, emit in self.world.get_component(ParticleEmiter):
            if emit.can_emit(dt):
                if emit.kind == "Engine" and self.world.has_component(ent, Input):
                    inp = self.world.component_for_entity(ent, Input)
                    if Input.inps['throttle'][inp.group]:
                        self.addEngineParticle(emit, emit.kind)

        #iterate particles
        for ent, (bhv, rend, ttl) in self.world.get_components(ParticleBehave, Renderable, TempLive):
            if bhv.kind == "Engine":
                self.iterateEngineParticle(dt, ent, rend, ttl)


    def addEngineParticle(self, emtr, kind):
        prt = self.world.create_entity()
        self.world.add_component(prt, ParticleBehave(kind))
        self.world.add_component(prt, TempLive(2, 0.7))
        tex = pyglet.resource.image("cloud.png").get_texture()
        rend = Renderable(tex, 60, 60)
        rend.sub_colors = [255, 100, 0, 255] * 4
        self.world.add_component(prt, rend)

        m = 0.01
        r = 1.0
        i = pymunk.moment_for_circle(m, 0, r, (0, 0))
        b = pymunk.Body(m, i)
        b.position = emtr.pos
        b.torque = random.triangular(-10, 10)

        force = Vec2d(0.0, 1.0) * 2
        force.rotate(emtr.angle + random.triangular(-0.40, 0.40))
        b.apply_impulse_at_world_point(force, emtr.pos)

        s = pymunk.Circle(b, r)
        s.friction = 0.1
        s.elasticity = 0.0 #no bounce
        s.entity = prt
        s.filter = pymunk.ShapeFilter(0, Physics.cats["particles"], Physics.masks["particles"])
        Physics.space.add(b, s)
        self.world.add_component(prt, Physics(b, s, rend))

    def iterateEngineParticle(self, dt, ent, rend, ttl):
        rend.w = rend.w + rend.w * 0.7 * dt
        rend.h = rend.h + rend.h * 0.7 * dt
        rnd = random.randint(70, 150)
        g = rend.sub_colors[1] + rnd * dt
        if g > 255:
            g = 255
        b = rend.sub_colors[2] + rnd * dt
        if b > 255:
            b = 255
        rnd = random.randint(110, 170)
        a = rend.sub_colors[3] - rnd * dt
        if a < 0:
            a = 0
        rend.set_sub_colors([255, g, b, a] * 4)

    def addSparks(self, pos):
        cnt = random.randint(10, 20) - 1
        for i in range(cnt):
            sprk = self.world.create_entity()



