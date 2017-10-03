import pyglet
from pyglet.gl import *

window = pyglet.window.Window()

image = pyglet.image.load('circle.png')
mask = pyglet.image.load('mask.png')
texture = pyglet.image.Texture.create(200, 200)

done = False

@window.event
def on_draw():
    window.clear()
    
    global done
    if not done:
        id = GLuint(0)
        glGenFramebuffersEXT(1, byref(id))
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, id)
        glFramebufferTexture2DEXT(
            GL_FRAMEBUFFER_EXT,
            GL_COLOR_ATTACHMENT0_EXT,
            texture.target,
            texture.id,
            texture.level)

        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        image.blit(100, 100)
        glBlendFunc(GL_ZERO, GL_SRC_ALPHA)
        mask.blit(0, 0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0)
        done = True
    
    glClearColor(0.8, 0.8, 0.8, 1)
    texture.blit(40, 30)
    texture.blit(0, 0)

pyglet.app.run()