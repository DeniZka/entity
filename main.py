import pyglet
from pyglet.gl import *
import ecs
from prc_render import TextureRenderProcessor
from factory import Factory
from hnd_window import WindowHandler
from prc_input import InputProcessor

from pymunk import Vec2d
from prc_physics import PhysicsProcessor
from prc_partciles import ParticleProcessor
from prc_camera import CameraProcessor
from prc_ui import UIProcessor
from prc_editor import EditorProcessor

def run(args=None):
    # pyglet graphics batch for efficient rendering
    # Initialize the main window stuff
    win_handler = WindowHandler()

    phys_processor = PhysicsProcessor()

    # Initialize Esper world, and create a "player" Entity with a few Components.
    #world = esper.World()
    world = ecs.Ecs()
    world.win_hnd = win_handler


    factory = Factory()
    inp_processor = InputProcessor(factory)
    pos = Vec2d(win_handler.RESOLUTION[0], win_handler.RESOLUTION[1])
    camera = CameraProcessor(pos)

    # Create some Processor instances, and asign them to be processed.
    render_processor = TextureRenderProcessor()
    part_processor = ParticleProcessor()
    ui_processor = UIProcessor()
    edit_proc = EditorProcessor()


    world.add_processor(factory)
    world.add_processor(inp_processor) #input first
    world.add_processor(part_processor)
    world.add_processor(phys_processor)
    world.add_processor(render_processor) #after physiscs !
    world.add_processor(camera) #after physiscs !
    world.add_processor(edit_proc)

    world.add_processor(ui_processor)
    win_handler.add_ui_processor(ui_processor)

    #world.add_processor(camera) funny effect



    #factory was added to processor so we can add come things into
    factory.testing()
    factory.createEnv()
    #player = factory.createPlayer(Vec2d(100,100))
    #camera.target = player[1]
    #enemy = factory.createEnemy(Vec2d(100,250))

    ui_processor.load_ui() #last, cause of ui attaches to player and so on


    def update(dt):
        world.process(dt)

    pyglet.clock.schedule_interval(update, 1.0 / (WindowHandler.FPS*2))
    pyglet.app.run()

if __name__ == "__main__":
    import sys
    sys.exit(run(sys.argv[1:]) or 0)
