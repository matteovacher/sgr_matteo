from ecs.components import *

class ComponentRegistry : 

    def __init__(self) : 
        self.genome_registry = {}
        self.body_registry = {}
        self.controller_registry = {}
        self.fitness_registry = {}
        self.morphology_network_registry = {}
        self.cppn_registry = {}


    # ADDER METHODS
    def add_genome(self, entity_id, genome) : 
        self.genome_registry[entity_id] = GenomeComponent(genome)
    
    def add_body(self, entity_id, body) : 
        self.body_registry[entity_id] = BodyComponent(body)
    
    def add_controller(self, entity_id, controller) : 
        self.controller_registry[entity_id] = ControllerNetworkComponent(controller)

    def add_fitness(self, entity_id, fitness) : 
        self.fitness_registry[entity_id] = FitnessComponent(fitness)
    def add_morphology_network(self, entity_id, morphology_network) : 
        self.morphology_network_registry[entity_id] = MorphologyNetworkComponent(morphology_network) 
    
    def add_cppn(self, entity_id, cppn) : 
        self.cppn_registry[entity_id] = CPPNComponent(cppn)

    
    # GETTER METHODS
    def get_genome(self, entity_id) : 
        return self.genome_registry[entity_id]
    
    def get_body(self, entity_id) : 
        return self.body_registry[entity_id]
    
    def get_controller(self, entity_id) : 
        return self.controller_registry[entity_id]
    
    def get_fitness(self, entity_id) : 
        return self.fitness_registry[entity_id]
    
    def get_morphology_network(self, entity_id) : 
        return self.morphology_network_registry[entity_id]
    
    def get_cppn(self, entity_id) : 
        return self.cppn_registry[entity_id]


    # CHECKER METHODS
    def has_genome(self, entity_id) : 
        return entity_id in self.genome_registry
    
    def has_body(self, entity_id) : 
        return entity_id in self.body_registry
    
    def has_controller(self, entity_id) : 
        return entity_id in self.controller_registry
    
    def has_fitness(self, entity_id) : 
        return entity_id in self.fitness_registry
    
    def has_morphology_network(self, entity_id) : 
        return entity_id in self.morphology_network_registry
    
    def has_cppn(self, entity_id) : 
        return entity_id in self.cppn_registry
    
    
    # ADVANCED GETTER METHODS 
    def get_all_id_with_genome(self) : 
        return self.genome_registry.keys()
    
    def get_all_id_with_body(self) : 
        return self.body_registry.keys()
    
    def get_all_id_with_controller(self) : 
        return self.controller_registry.keys()
    
    def get_all_id_with_fitness(self) : 
        return self.fitness_registry.keys()
    
    def get_all_id_with_morphology_network(self) : 
        return self.morphology_network_registry.keys()
    
    def get_all_id_with_cppn(self) : 
        return self.cppn_registry.keys()
    
    
    # CLEARER METHODS 
    def  clear_all_except_genome(self) : 
        self.body_registry.clear()
        self.controller_registry.clear()
        self.fitness_registry.clear()   
        self.morphology_network_registry.clear()
        self.cppn_registry.clear()

    def clear_genome(self) : 
        self.genome_registry.clear()
    
    def clear_body(self) : 
        self.body_registry.clear()
    
    def clear_controller(self) : 
        self.controller_registry.clear()
    
    def clear_fitness(self) : 
        self.fitness_registry.clear()

    def clear_morphology_network(self) : 
        self.morphology_network_registry.clear()
    
    def clear_cppn(self) : 
        self.cppn_registry.clear()
    


