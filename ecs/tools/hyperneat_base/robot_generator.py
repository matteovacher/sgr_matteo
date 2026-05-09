import numpy as np 
from evogym import is_connected, has_actuator, get_full_connectivity



class RobotGenerator :
    TYPES_OF_VOXELS = ['empty', 'rigid', 'soft', 'horizontal', 'vertical']

    def __init__(self, robot_size) :
        self.robot_size = robot_size 

    def generate_robot_body_from_substrate(self, morphology_ann): 
        """Here we generate the robot from the substrate with a random input, everything is fine when we format the output of the network, 
        """
        morphology_output = morphology_ann.activate([1997])
        formated = np.reshape(morphology_output, (self.robot_size, self.robot_size, len(self.TYPES_OF_VOXELS)))
        robot = np.argmax(formated, 2)
        return robot 

    def is_valid_robot(self, robot) : 
        """A valid robot is a robot that is connected and has at least one actuator. We use the functions provided by evogym to check these constraints."""
        return is_connected(robot) and has_actuator(robot)
    
    def get_full_connectivity(self, robot) : 
        return get_full_connectivity(robot)
            
    