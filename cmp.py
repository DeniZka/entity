"""
Use those components with ecs world for cleanup callback instead of __del__ which can be ... so far
"""


class Component:

    def on_remove(self):
        #empty callback function
        pass
