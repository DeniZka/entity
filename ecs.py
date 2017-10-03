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
        #every on must know about new one
        for prc in self._processors:
            prc.on_add(processor_instance)
        #add new one
        super().add_processor(processor_instance, priority)
        #tell new one tahat he added
        processor_instance.on_add(processor_instance)

