from ecs.registry import ComponentRegistry
from ecs.components import CPPNComponent, GenomeComponent, MorphologyNetworkComponent, BodyComponent, ControllerNetworkComponent
from ecs.tools.hyperneat_base.substrate import Substrate 
from ecs.tools.hyperneat_base.robot_generator import RobotGenerator
from ecs.tools.hyperneat_base.robot_simulator import RobotSimulator
from ecs.tools.hyperneat_base.hyperneat import PhenotypeBuilder

import neat 
import math 

class BuildSystem : 
    def __init__(self, neat_config, robot_size, env_name, n_steps) :
        self.neat_config = neat_config
        self.robot_size = robot_size
        self.env_name = env_name
        self.n_steps = n_steps

        # initializing the tools i will be using 
        self.robot_generator = RobotGenerator(robot_size)
        self.robot_simulator = RobotSimulator(env_name, n_steps)
        

         

    def process(self, registry) : 
        
        # first get the id of all entities with genome to use the genome to create everything 
        for entity_id in list(registry.get_all_id_with_genome()) : 
            genome = registry.get_genome(entity_id).genome 

            # then create cppn and stock it to use it 
            cppn = neat.nn.FeedForwardNetwork.create(genome, self.neat_config)
            registry.add_cppn(entity_id, cppn)

            # then proceed to create substrate, first morpho 
            morphology_substrate = Substrate.morph_substrate_shape_builder(self.robot_size)

            # then create the network associated to the substrate 
            phenotype_builder = PhenotypeBuilder(cppn)
            morphology_network = phenotype_builder.create_phenotype_network(morphology_substrate, output_node_idx=0)
            registry.add_morphology_network(entity_id, morphology_network)

            # then create the body 
            robot_grid = self.robot_generator.generate_robot_body_from_substrate(morphology_network)
            
            # evaluate its validity 
            if not self.robot_generator.is_valid_robot(robot_grid) : 
                continue

            # ig good add to bodycomponenent 
            connections = self.robot_generator.get_full_connectivity(robot_grid)
            registry.add_body(entity_id, robot_grid, connections)

            # then create the controller but for that we need the input grid size 
            obervation_size = self.robot_simulator.get_observation_size(robot_grid)
            grid_input_size = math.ceil(math.sqrt(obervation_size))
            control_substrate = Substrate.control_substrate_shape_builder(self.robot_size, grid_input_size)

            # then create the network associated to the substrate 
            controller_network = phenotype_builder.create_phenotype_network(control_substrate, output_node_idx=1)
            registry.add_controller_network(entity_id, controller_network)


