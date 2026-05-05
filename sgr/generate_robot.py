import numpy as np 
from evogym.utils import is_connected, has_actuator

N_TYPES = ['empty', 'rigid', 'soft', 'horizontal', 'vertical']

def generate_robot_from_substrate(network, robot_size) : 
    """Here we generate the robot from the substrate with a random input, everything is fine when we format the output of the network, 
    """
    morphology_output = network.activate([1997])
    formated = np.reshape(morphology_output, (robot_size, robot_size, len(N_TYPES)))
    robot = np.argmax(formated, 2)
    return robot 

def is_valid_robot(robot) : 
    """A valid robot is a robot that is connected and has at least one actuator. We use the functions provided by evogym to check these constraints."""
    return is_connected(robot) and has_actuator(robot)