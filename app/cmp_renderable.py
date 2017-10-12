from pyglet.gl import *
from pymunk import Vec2d

from app.cmp import Component


class Renderable(Component):
    # pack of vertixes
    # easy access to batch group from everywhere
    batch = None
    ui_batch = None

    # groups
    bg = None
    mg = None
    fg = None
    ui = None
    bg_image = None
    fat_line = None
    fat_point = None

    def __init__(self, texture=None, group=None, atype=GL_QUADS, verts=[]):
        self.texture = texture
        self.vertex_list = None
        self.atype = atype
        parent = Renderable.mg
        if group:
            parent = group
        if texture:
            self.group = TextureBindGroup(texture, parent)
        elif group:
            self.group = group
        else:
            self.group = Renderable.mg
        self.vertex_list = []
        self._modified = True  # support for smooth coloring in dt

        vertex_format = 'v2f/static'
        if texture:
            if self.group.parent == Renderable.ui:
                self.vertex_list.append(
                    Renderable.ui_batch.add(
                    4, atype,
                    self.group,
                    vertex_format, 'c4B/static',
                    ('t3f/static', texture.tex_coords)
                    )
                )
            else:
                self.vertex_list.append(
                    Renderable.batch.add(
                    4, atype,
                    self.group,
                    vertex_format, 'c4B/static',
                    ('t3f/static', texture.tex_coords)
                    )
                )
        else:  # textureless
            if atype == GL_QUADS:
                self.vertex_list.append (
                    Renderable.batch.add(
                    4, atype,
                    self.group,
                    vertex_format, 'c4B/static'
                    )
                )
            elif atype == GL_LINES:
                self.vertex_list.append(
                    Renderable.batch.add(
                    2, atype,
                    self.group,
                    vertex_format, 'c4B/static'
                    )
                )
            elif atype == GL_POINTS:
                self.vertex_list.append(
                    Renderable.batch.add(
                    1, atype,
                    self.group,
                    vertex_format, 'c4B/static'
                    )
                )
            else:
                assert (False), "WRONG atype"

        # set default colors
        self._colors = [255, 255, 255, 255] * self.vertex_list[0].count
        self.sub_colors = self._colors

        #set default vertex
        if len(verts) < 1:
            return

        self.vertex_list[0].vertices = verts

    def add_line(self, v):
        """
        single verticse list is NOT better then multiple lists  !!!

        size = self.vertex_list[0].get_size()
        self.vertex_list[0].resize(size+2)
        self.vertex_list[0].vertices[size*2:] = v
        #self.vertex_list[0].colors[size*2:] =
        for i in range(2):
            for j in range(4):
                self._colors.append(self._colors[j])
        return
        """
        self.vertex_list.append(
            Renderable.batch.add(
                2, GL_LINES,
                self.group,
                'v2f/static', 'c4B/static'
            )
        )
        self.vertex_list[-1].vertices = v

    def add_quads(self, v):
        self.vertex_list.append(
            Renderable.batch.add(
                4, GL_QUADS,
                self.group,
                'v2f/static', 'c4B/static'
            )
        )
        self.vertex_list[-1].vertices = v


    @property
    def colors(self):
        self._modified = False
        return self._colors

    @colors.setter
    def colors(self, val):
        self._colors = val * self.vertex_list[0].get_size()
        self._modified = True

    @property
    def modified(self):
        return self._modified

    @property
    def size(self):
        if self.texture:
            return Vec2d(self.texture.width, self.texture.height)
        else:
            return None

    def on_remove(self):
        if self.vertex_list:
            self.vertex_list.delete()

    def set_pos_lock(self, lock_st):
        self.pos_locked = lock_st

    def set_sub_colors(self, colors):
        self.sub_colors = colors
        for i in range(16):
            self._colors[i] = int(self.sub_colors[i])
        self._modified = True

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
        glEnable(self.texture.target)  # Fixed disappeared textures
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        glPushAttrib(GL_COLOR_BUFFER_BIT)
        return
        # this added globaly
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