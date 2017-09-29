from prc import Processor


class EditorProcessor(Processor):

    def __init__(self):
        self.subscribed = False
        return

    def process(self, dt):
        if not self.subscribed:
            self.world.get

