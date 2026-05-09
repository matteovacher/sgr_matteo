

class GenomeComponent : 
    
    def __init__(self, genome) : 
        self.genome = genome 

class CPPNComponent : 

    def __init__(self, cppn) : 
        self.cppn = cppn

class MorphologyNetworkComponent : 

    def __init__(self, morphology_network) : 
        self.morphology_network = morphology_network

class BodyComponent : 

    def __init__(self, grid, connections) : 
        self.grid = grid
        self.connections = connections

class ControllerNetworkComponent : 

    def __init__(self, controller_network) : 
        self.controller_network = controller_network

class FitnessComponent : 

    def __init__(self, fitness, finished) : 
        self.fitness = fitness
        self.finished = finished



