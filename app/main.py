import pyglet
from app.prc_camera import CameraProcessor
from app.prc_editor import EditorProcessor
from app.prc_input import InputProcessor
from app.prc_partciles import ParticleProcessor
from app.prc_render import TextureRenderProcessor
from app.prc_ui import UIProcessor
from pyglet.gl import *
from pymunk import Vec2d

from app.ecs import Ecs
from app.factory import Factory
from app.hnd_window import WindowHandler
from app.prc_physics import PhysicsProcessor

from random import randint

pyglet.options['debug_gl'] = False


def run(args=None):
    # pyglet graphics batch for efficient rendering
    # Initialize the main window stuff
    win_handler = WindowHandler()


    phys_processor = PhysicsProcessor()

    # Initialize Esper world, and create a "player" Entity with a few Components.
    #world = esper.World()
    world = Ecs(True)
    world.win_hnd = win_handler


    factory = Factory()
    inp_processor = InputProcessor(factory)
    pos = Vec2d(win_handler.res[0], win_handler.res[1])
    camera = CameraProcessor(pos)

    # Create some Processor instances, and asign them to be processed.
    render_processor = TextureRenderProcessor()
    part_processor = ParticleProcessor()
    ui_processor = UIProcessor()
    edit_proc = EditorProcessor()


    world.add_processor(factory)
    world.add_processor(inp_processor) #input first
    #world.add_processor(part_processor)
    #world.add_processor(phys_processor)
    world.add_processor(render_processor) #after physiscs !
    world.add_processor(camera) #after physiscs !
    world.add_processor(edit_proc)

    world.add_processor(ui_processor)
    win_handler.add_ui_processor(ui_processor)

    #world.add_processor(camera) funny effect



    #factory was added to processor so we can add come things into
    #factory.testing()
    #factory.createEnv()
    for i in range(10):
        factory.create_instance(Vec2d(randint(0,10000), randint(0, 10000)))
    factory.create_instance(Vec2d(0, 0))
    #player = factory.createPlayer(Vec2d(100,100))
    #camera.target = player[1]
    #enemy = factory.createEnemy(Vec2d(100,250))

    #ui_processor.load_ui() #last, cause of ui attaches to player and so on


    def update(dt):
        world.process(dt)

    pyglet.clock.schedule_interval(update, 1.0 / (WindowHandler.FPS*5))
    pyglet.app.run()

