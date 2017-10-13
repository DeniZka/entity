from pymunk import Vec2d
import pyglet

from app.cmp_instance import Instance
from app.cmp_joint import Joint
from app.cmp_renderable import Renderable
from app.cmp_transform import Transform
from app.cmp_pin import Pin
from app.cmp_segment import Segment
from app.factory import Factory
from app.prc import Processor
from app.prc_camera import CameraProcessor

SQ_SNAP_DISTANCE = 200  # snapping distance when drag a joint (in screen pixels)
SQ_SENSE_RAD = 10       # additional radius when joint dropped near
JOINT_WAYS_LIMIT = 4    # maximuum of connected segments (NEED TO BE CORRECTED IN JOINT TOO)


class EditorProcessor(Processor):

    def __init__(self):
        self.subscribed = False
        self.cam = None
        self.picked = None
        self.picked_id = -1
        self.picked_jnt = None
        self.picked_shift_v = Vec2d(0, 0)
        self.cam_rotating = False
        self.cam_rot_angle = 0
        self.en_snap = True       #instance items do not need in snapping

    def on_add(self, proc):
        if proc == self:
            self.cam = self.world.get_processor(CameraProcessor)
            self.world.win_hnd.subscribe("on_mouse_press", self.on_mouse_press)
            self.world.win_hnd.subscribe("on_mouse_drag", self.on_mouse_drag)
            self.world.win_hnd.subscribe("on_mouse_release", self.on_mouse_release)
        if proc.__class__ is CameraProcessor:
            self.cam = proc

    def contact_dist(self, pt1, pt2):
        """
        Those points are one the taking/connecting distance
        :param pt1:
        :param pt2:
        :return: boolean
        """
        r = pt1 - pt2
        if r.get_length_sqrd() < SQ_SENSE_RAD:
            return True
        else:
            return False

    def can_merge(self, src_trs, dst_tr, src_pos):
        # check joints transfromrations are the same
        if src_trs[0] == dst_tr:
            return False
        if self.contact_dist(src_trs[0].pos, dst_tr.pos):
            #check is not a tail of one of self segments
            for tr in src_trs:
                if tr.other_point(src_pos) == dst_tr.pos:
                    return False
            return dst_tr

    def get_seg_tr(self, tr, jnt):
        """
        Get all segments that joined to this joint transform
        :param tr: transform for joint
        :param jnt: joint
        :return: pack of transforms for pos updating
        """
        ret = [tr]
        for sg_ent in jnt.ios:
            sg = self.world.component_for_entity(sg_ent, Segment)
            # if not sg_tr.pick_pt_drag_id(tr.pos):
            #    print("Problem")
            ret.append(sg)
        return ret

    def nearest(self, pos):
        min_dist = 1000000
        near_tr = None
        for ent, tr in self.world.get_component(Transform):
            has_jnt = self.world.has_component(ent, Joint)
            has_pin = self.world.has_component(ent, Pin)
            if not has_jnt and not has_pin:
                continue
            # except calc if tr is picked
            if self.picked and tr == self.picked[0]:
                continue
            # except unpickable Transform child node
            if self.picked is None and tr.parent and tr.parent.__class__ == Transform:
                continue
            sq_d = pos.get_dist_sqrd(tr.g_pos)
            if sq_d < min_dist:
                min_dist = sq_d
                near_tr = tr
        return near_tr

    def nearest_joint(self, pos):
        min_dist = 1000000
        near_tr = None
        near_jnt = None
        for ent, (tr, jnt) in self.world.get_components(Transform, Joint):
            # except calc if tr is picked
            if self.picked and tr == self.picked[0]:
                continue
            # except unpickable Transform child node
            if self.picked is None and tr.parent and tr.parent.__class__ == Transform:
                continue
            sq_d = pos.get_dist_sqrd(tr.g_pos)
            if sq_d < min_dist:
                min_dist = sq_d
                near_tr = tr
                near_jnt = jnt

        return near_tr, near_jnt

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            scr_v = Vec2d(x, y)
            w = self.cam.to_world(Vec2d(x, y))
            # find an pickable instance
            for ent, (tr, inst, r) in self.world.get_components(Transform, Instance, Renderable):
                if self.world.has_component(ent, Joint):
                    continue
                if tr.parent:
                    continue
                sv = tr.get_in_bb(w)
                if sv:
                    self.picked = [tr]
                    self.picked_shift_v = sv
                    self.en_snap = False
                    return

            # nothing to pick -> find a join
            found = False
            near = self.nearest_joint(w)
            if near[0]:
                scr_tr_v = self.cam.to_screen(near[0].g_pos)
                if (scr_tr_v - scr_v).get_length_sqrd() < SQ_SNAP_DISTANCE:
                    self.picked_jnt = near[1]
                    self.picked_id = near[1].id
                    self.picked = self.get_seg_tr(near[0], near[1])
                    found = True

            if not found:
                # no joint -> create segment and pick it
                factory = self.world.get_processor(Factory)
                seg = factory.create_segment(w)
                self.picked_id = seg[0]
                self.picked_jnt = seg[1]
                self.picked = seg[2]

        if button == 2:
            v = Vec2d(x - self.world.win_hnd.res[0]*0.5, y - self.world.win_hnd.res[1]*0.5)
            self.cam_rot_angle = v.angle

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.picked:
            scr_v = Vec2d(x, y)
            w = self.cam.to_world(scr_v)
            if self.en_snap:
                #on move snap feature
                near = self.nearest(w)
                if near:
                    scr_tr_v = self.cam.to_screen(near.g_pos)
                    if (scr_tr_v - scr_v).get_length_sqrd() < SQ_SNAP_DISTANCE:
                        w = near.g_pos

            self.picked[0].x = w.x - self.picked_shift_v.x
            self.picked[0].y = w.y - self.picked_shift_v.y
            for v in self.picked:
                v._set_modified()

        if buttons == 2:
            v = Vec2d(x - self.world.win_hnd.res[0]/2, y - self.world.win_hnd.res[1]/2)
            a = v.angle
            self.cam.angle += (self.cam_rot_angle - a)
            self.cam_rot_angle = a

    def on_mouse_release(self, x, y, button, modifiers):
        self.picked_shift_v.x = 0
        self.picked_shift_v.y = 0
        if button == 1 and self.picked and self.picked_jnt:
            # merge jointes if it able
            w = self.cam.to_world(Vec2d(x, y))
            cnt = len(self.picked) - 1
            for ent, (tr, jnt) in self.world.get_components(Transform, Joint):
                # check ways total count
                if jnt.ways + cnt > JOINT_WAYS_LIMIT:
                    continue
                if self.can_merge(self.picked, tr, self.picked[0].pos):
                    # attach to joint
                    for seg_id in self.picked_jnt.ios:
                        jnt.attach(seg_id)
                    # attach to segment
                    for i in range(1, cnt+1):
                        assert (self.picked[i].replace_pt(self.picked[0].pos, tr.pos) == True), "Some problem"
                        self.picked[i]._set_modified()
                    self.world.delete_entity(self.picked_id)
                    break
        self.en_snap = True
        self.picked_jnt = None
        self.picked = None
        self.picked_id = -1

    def process(self, dt):
        return


