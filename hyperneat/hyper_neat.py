import neat

"""Hyperneat implementation 
"""

def query_cppn(coordinate1, coordinate2, one_towards_two, cppn, max_weight, output_node_idx, bias=1.0) :
    """This function takes the array of coordinates, a boolean indicating the direction of the connection, 
    the cppn, the max weight that will define the output interval and the index of output that is used to know if we take the first or second output of the cppn 
    we add a bias so that if every inputs is null, we still have one of them that is not null. 
    """
    if one_towards_two : 
        inputs = [*coordinate1, *coordinate2, bias]
    else : 
        inputs = [*coordinate2, *coordinate1, bias]
    outputs = cppn.activate(inputs)
    weight = outputs[output_node_idx] # our cppn has two outputs, so that it is easier for him 
    # to detect the type of substrate, then we identify them with 0 and 1 
    # here we only keep weight greater than 0.2 or smaller than -0.2, then we rescale them between 0, 1 before rescaling them to max_weight
    if weight > 0.2 : 
        weight = (weight - 0.2)/0.8
    elif weight < -0.2 :
        weight = (weight + 0.2)/0.8
    else : 
        weight =0.0
        return weight
    return weight*max_weight

def connect_target_node_to_layer(cppn, target_node_coordinate, source_layer_coordinates, node_dict, one_towards_two, max_weight, output_node_idx) :
    """This function takes the cppn, the coordinate of the target node ie one node on the next layer and the coordinates of the node in the source layer 
    then it returns the list of incoming connections to the target node with the format (index of the source node, weight of the connection)
    It is important to note that the cppn has 2 outputs, it is necessary for him to learn to differentiate the direction of the connextions. """
    incoming_connections = []
    for source_node_coordinate in source_layer_coordinates :
        weight = query_cppn(source_node_coordinate, target_node_coordinate, one_towards_two, cppn, max_weight, output_node_idx)
        if weight != 0.0 : 
            incoming_connections.append((node_dict[tuple(source_node_coordinate)], weight))
    return incoming_connections
    
def create_phenotype_network(cppn, substrate, activation_function="tanh", out_activation_function="identity", max_weight=1, output_node_idx=0) :
    """This function takes the cppn, a substrate defining the substrate structure. Then, it creates the phenotype, 
    its structure must be a dictionary following the format node_dict ={coordinates of the node : index of the node}. 
    then the phenotype ie ann is also defined by node_evaluations, an array of the format [[index of the node, activation function, agregation_function, bias, response, incoming_connections], ...]
    where incoming connections is an array of the format [(index of the source node, weight), ...]"""
    activation_function_set = neat.activations.ActivationFunctionSet()
    activation = activation_function_set.get(activation_function)
    output_activation = activation_function_set.get(out_activation_function)

    all_layers = [substrate.input_coordinates] + substrate.hidden_coordinates + [substrate.output_coordinates]
    node_dict = {}
    idx = 0 
    for layer in all_layers : 
        for node in layer : 
            node_dict[tuple(node)] = idx 
            idx += 1

    node_evaluations = []
    idx_current_source_layer = 0
    for layer in all_layers[1:] : 
        source_layer = all_layers[idx_current_source_layer]
        for hidden_node in layer : 
            one_towards_two = True 
            incoming_connections = connect_target_node_to_layer(cppn, hidden_node, source_layer, node_dict, one_towards_two, max_weight, output_node_idx)
            # eval contains the index of the node stored in the dict, the activation function, the agregation function, the bias, and the response such that : 
            # output = activation(bias + response*sum(inputs))
            act = output_activation if layer is all_layers[-1] else activation
            evaluation = [node_dict[tuple(hidden_node)], act, sum, 0.0, 1.0, incoming_connections]
            node_evaluations.append(evaluation)
        idx_current_source_layer += 1

    input_nodes = [node_dict[tuple(node)] for node in substrate.input_coordinates]
    output_nodes = [node_dict[tuple(node)] for node in substrate.output_coordinates]
    return neat.nn.FeedForwardNetwork(input_nodes, output_nodes, node_evaluations)



