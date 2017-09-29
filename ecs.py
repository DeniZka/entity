import esper
"""
esper variation with cleanup component calling
"""


class Ecs(esper.World):
    """
    callback for components for cleanup
    """
    def delete_entity(self, entity, immediate=False):
        if immediate: #call callbacks
            for component_type in self._entities[entity]:
                self._entities[entity][component_type].on_remove()
        super().delete_entity(entity, immediate)

    """
    callback for Processors for subscription actions
    """
    def add_processor(self, processor_instance, priority=0):
        super().add_processor(processor_instance, priority)
        processor_instance.on_add()

