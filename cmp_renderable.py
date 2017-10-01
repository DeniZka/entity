from pyglet.gl import *
from pyglet.sprite import Sprite
from pymunk import Vec2d
from cmp import Component


class Renderable(Component):
    batch = None #easy access to batch group from everywhere
    ui_batch = None
    bg = None
    mg = None
    fg = None
    ui = None
    bg_image = None

    def __init__(self, texture=None, width=0, height=0, group=None, atype=GL_QUADS):
        #self.sprite = Sprite(texture, 0,0,)
        #TODO: REFACTORE THIS ADD LINES
        self.pos = Vec2d(0, 0)
        self.pos2 = None  # for lines that has two points
        self.pos_locked = False  #for UI which update noly angles
        self.angle = 0
        self.texture = texture
        parent = Renderable.mg

        if group:
            parent = group
        if width:
            self.w = width
        elif texture:
            self.w = texture.width
        if height:
            self.h = height
        elif texture:
            self.h = texture.height
        if texture:
            self.group = TextureBindGroup(texture, parent)
        else:
            self.group = Renderable.mg
        self.vertex_list = None
        self._dirty = True
        self.colors = [255, 255, 255, 255] * 4
        self.sub_colors = self.colors
        self.sub_modif = True #support for smooth coloring in dt
        vertex_format = 'v2f/stream'
        if texture:
            if self.group.parent == Renderable.ui:
                self.vertex_list = Renderable.ui_batch.add(
                    4, atype,
                    self.group,
                    vertex_format, 'c4B/stream',
                    ('t3f/static', texture.tex_coords)
                )
            else:
                self.vertex_list = Renderable.batch.add(
                    4, atype,
                    self.group,
                    vertex_format, 'c4B/stream',
                    ('t3f/static', texture.tex_coords)
                )
        else:  # textureless
            if atype == GL_QUADS:
                self.vertex_list = Renderable.batch.add(
                    4, atype,
                    self.group,
                    vertex_format, 'c4B/stream'
                )
            else:
                self.vertex_list = Renderable.batch.add(
                    2, atype,
                    self.group,
                    vertex_format, 'c4B/static'
                )

    def on_remove(self):
        if self.vertex_list:
            self.vertex_list.delete()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        if val != self._x:
            self._x = val
            self._dirty = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        if val != self._y:
            self._y = val
            self._dirty = True


    def scale(self, vec):
        #TODO: SCALE
        return

    def set_pos_lock(self, lock_st):
        self.pos_locked = lock_st

    def set_sub_colors(self, colors):
        self.sub_colors = colors
        for i in range(16):
            self.colors[i] = int(self.sub_colors[i])
        self.sub_modif = True

    def set_pos(self, vec):
        if not self.pos_locked:
            self.pos = vec

    def set_angle(self, angle):
        self.angle = angle



# Code below cobbled together from
# https://pyglet.readthedocs.org/en/latest/programming_guide/graphics.html#hierarchical-state
# and pyglet.sprite.SpriteGroup


class TextureEnableGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(GL_TEXTURE_2D)

    def unset_state(self):
        glDisable(GL_TEXTURE_2D)


texture_enable_group = TextureEnableGroup()


class TextureBindGroup(pyglet.graphics.Group):
    def __init__(self, texture, parent):
        super().__init__(parent=texture_enable_group)
        assert texture.target == GL_TEXTURE_2D
        self.texture = texture
        self.parent = parent
        self.blend_src = GL_SRC_ALPHA
        self.blend_dest = GL_ONE_MINUS_SRC_ALPHA

    def set_state(self):
        glEnable(self.texture.target) #Fied disappeared textures
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        glPushAttrib(GL_COLOR_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)

    def unset_state(self):
        glPopAttrib()
        glDisable(self.texture.target)

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.parent is other.parent and
                self.texture.target == other.texture.target and
                self.texture.id == other.texture.id and
                self.blend_src == other.blend_src and
                self.blend_dest == other.blend_dest)

    def __hash__(self):
        return hash((id(self.parent),
                     self.texture.id, self.texture.target,
                     self.blend_src, self.blend_dest))