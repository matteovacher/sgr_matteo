from hyperneat.substrate import Substrate


def morph_substrate_shape_builder(robot_size) : 
    """This function take the robot size and based on it, creates the shape that will be passe to the substrate class to create the substrate for the morpho"""
    # this here will be the number of neurons on 1 dimensions of the layer 
    intermediate_layer = (1 + robot_size)//2
    shape = [
        [1, 1, 1, 1],
        [intermediate_layer, intermediate_layer, 3, 2],
        [robot_size, robot_size, 5, 3],
    ]
    return Substrate(shape)

def control_substrate_shape_builder(robot_size, grid_input_size) :
    """This function take the robot size and the grid input size and based on it, 
    creates the shape that will be passed to the bustrate class to create the substrate for the control."""
    intermediate_layer = (grid_input_size + robot_size)//2
    shape = [
        [grid_input_size, grid_input_size, 1, -1],
        [intermediate_layer, intermediate_layer, 1, -2],
        [robot_size, robot_size, 1, -3]
    ]
    return Substrate(shape)