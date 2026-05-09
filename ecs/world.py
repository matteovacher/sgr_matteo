from ecs.entity_manager import EntityManager
from ecs.registry import ComponentRegistry

class World : 

    def __init__(self) :
        self.entities = EntityManager()
        self.registry = ComponentRegistry()
        self._systems = []

    def add_system(self, system) : 
        self.systems.append(system)

    def reset(self) : 
        self.registry.clear_all_except_genome()

    def step(self) : 
        for system in self._systems : 
            pass 
