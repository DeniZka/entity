import esper
"""
esper variation with cleanup component calling
"""


class Ecs(esper.World):
    def delete_entity(self, entity, immediate=False):
        if immediate: #call callbacks
            for component_type in self._entities[entity]:
                self._entities[entity][component_type].on_remove()
        super().delete_entity(entity, immediate)

