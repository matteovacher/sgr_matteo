from ecs.registry import ComponentRegistry
from ecs.components import CPPNComponent, GenomeComponent, MorphologyNetworkComponent, BodyComponent, ControllerNetworkComponent
from ecs.tools.hyperneat_base.substrate import Substrate 
from ecs.tools.hyperneat_base.robot_generator import RobotGenerator
from ecs.tools.hyperneat_base.robot_simulator import RobotSimulator

class BuildSystem : 
    def __init__(self, neat_config, robot_size, env_name, n_steps) :
        self.neat_config = neat_config
        self.robot_size = robot_size
        self.env_name = env_name
        self.n_steps = n_steps

        # initializing the tools i will be using 
        self.substrate = Substrate(robot_size) 
        self.robot_generator = RobotGenerator(robot_size)
        self.robot_simulator = RobotSimulator(env_name, n_steps)
        

         

    def process(self, registry) : 
        morphology_substrate = self.substrate.morph_substrate_shape_builder(self.robot_size)

