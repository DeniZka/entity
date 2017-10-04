from prc import Processor
from cmp_joint import Joint
from cmp_transform import Transform
from cmp_segment import Segment
from prc_camera import CameraProcessor
from pymunk import Vec2d
from factory import Factory


class EditorProcessor(Processor):

    def __init__(self):
        self.subscribed = False
        self.sq_sense_rad = 10
        self.cam = None
        self.picked = None
        self.picked_id = -1
        self.picked_jnt = None
        return

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
        if r.get_length_sqrd() < self.sq_sense_rad:
            return True
        else:
            return False

    def can_merge(self, src_trs, dst_tr):
        # check joints transfromrations are the same
        if src_trs[0] == dst_tr:
            return False
        if self.contact_dist(src_trs[0].pos, dst_tr.pos):
            #check is not a tail of one of self segments
            for tr in src_trs:
                if tr.other_point(tr.pos) == dst_tr.pos:
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
            sg_tr = self.world.component_for_entity(sg_ent, Transform)
            if not sg_tr.pick_pt_drag_id(tr.pos):
                print("Problem")
            ret.append(sg_tr)
        return ret


    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            w = self.cam.to_world(Vec2d(x, y))
            factory = self.world.get_processor(Factory)
            found = False
            for ent, (tr, jnt) in self.world.get_components(Transform, Joint):
                if self.contact_dist(tr.pos, w):
                    self.picked_jnt = jnt
                    self.picked_id = ent
                    self.picked = self.get_seg_tr(tr, jnt)
                    if self.picked:
                        found = True
                        break

            if not found:
                rend = factory.create_segment(w)
                self.picked = [rend]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.picked:
            w = self.cam.to_world(Vec2d(x, y))
            for v in self.picked:
                v.x = w.x #update the X and Y cause of pos uses by multiple entity
                v.y = w.y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1 and self.picked:
            w = self.cam.to_world(Vec2d(x, y))
            cnt = len(self.picked) - 1
            for ent, (tr, jnt) in self.world.get_components(Transform, Joint):
                #check ways total count
                if jnt.ways + cnt > 4:
                    continue
                if self.can_merge(self.picked, tr):
                    #attach to joint
                    for seg_id in self.picked_jnt.ios:
                        jnt.attach(seg_id)
                    #attach to segment
                    for t in self.picked:
                        t.pos = jnt.pos

                    self.world.delete_entity(self.picked_id)
                    self.picked_jnt = None
                    self.picked = None
                    self.picked_id = -1
                    return
        self.picked_jnt = None
        self.picked = None
        self.picked_id = -1



        #TODO; merge with existing (and IS not self)
        """
        v = self.cam.to_world(Vec2d(x, y))
        for ent, (seg, rend) in self.world.get_components(Segment, Renderable):
            
            tgtv = self.in_target(seg, v)
            if tgtv:
               if tgtv == seg.pos1 and self.picked is not seg.pos1:
                seg
                self
        """

    def process(self, dt):
        return
        #if not self.subscribed:
            #self.world.get

