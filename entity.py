import pyglet
from pyglet.gl import *

import esper

from cmp_renderable import Renderable
from prc_render import TextureRenderProcessor
from factory import Factory
from cmp_physics import Physics
from hnd_window import WindowHandler
from prc_input import InputProcessor

from pymunk import Vec2d
from prc_physics import PhysicsProcessor
from prc_partciles import ParticleProcessor
from prc_camera import Camera

from threading import *
import time


def run(args=None):
    # pyglet graphics batch for efficient rendering
    # Initialize the main window stuff
    win_handler = WindowHandler()


    phys_processor = PhysicsProcessor()


    # Initialize Esper world, and create a "player" Entity with a few Components.
    world = esper.World()


    factory = Factory()
    inp_processor = InputProcessor(factory)
    pos = Vec2d(win_handler.RESOLUTION[0], win_handler.RESOLUTION[1])
    camera = Camera(pos)

    # Create some Processor instances, and asign them to be processed.
    render_processor = TextureRenderProcessor()
    part_processor = ParticleProcessor()

    world.add_processor(factory)
    world.add_processor(camera)
    world.add_processor(inp_processor) #input first
    world.add_processor(render_processor)
    world.add_processor(part_processor)
    world.add_processor(phys_processor) #phisics count last of all
    #world.add_processor(camera) funny effect



    #factory was added to processor so we can add come things into
    factory.createEnv()
    player = factory.createPlayer(Vec2d(100,100))
    enemy = factory.createEnemy(Vec2d(400,250))

    def update(dt):
        world.process(dt)

    pyglet.clock.schedule_interval(update, 1.0 / (WindowHandler.FPS))
    pyglet.app.run()

if __name__ == "__main__":
    import sys
    sys.exit(run(sys.argv[1:]) or 0)
