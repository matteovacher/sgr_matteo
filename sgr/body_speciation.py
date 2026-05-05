import neat 
from hyperneat.hyper_neat import create_phenotype_network
from sgr.generate_robot import generate_robot_from_substrate, is_valid_robot
import numpy as np


class MorphoAwareGenome(neat.DefaultGenome) : 
    neat_config = None 

    def __init__(self, key) : 
        super().__init__(key)
        if MorphoAwareGenome.neat_config is None :
            raise RuntimeError("Please set the neat_config attribute of MorphoAwareGenome before creating any instance of it.") 

    @classmethod   
    def configure(myclass, neat, substrate, robot_size, spec_genotype_weight, spec_phenotype_weight) : 
        myclass.neat_config = neat
        myclass.substrate = substrate
        myclass.robot_size = robot_size
        myclass.spec_genotype_weight = spec_genotype_weight
        myclass.spec_phenotype_weight = spec_phenotype_weight

    @staticmethod
    def _robot_from_genome(genome, robot_size, substrate) :
        cppn = neat.nn.FeedForwardNetwork.create(genome, MorphoAwareGenome.neat_config)
        design_network = create_phenotype_network(cppn, substrate, output_node_idx=0)
        robot = generate_robot_from_substrate(design_network, robot_size)

        if is_valid_robot(robot) :
            return robot
        else : 
            return np.zeros((robot_size, robot_size))

    def distance(self, other, _) :
        
        genotype_distance = super().distance(other, MorphoAwareGenome.neat_config.genome_config)
        if not hasattr(self, 'robot') :
            self.robot = MorphoAwareGenome._robot_from_genome(self, self.robot_size, self.substrate)
        if not hasattr(other, 'robot') :    
            other.robot = MorphoAwareGenome._robot_from_genome(other, self.robot_size, self.substrate)

        difference = 0
        for i in range(self.robot_size) : 
            for j in range(self.robot_size) : 
                if (self.robot[i][j] == 0 and other.robot[i][j] != 0) or (self.robot[i][j] != 0 and other.robot[i][j] == 0) : 
                    difference += 1
                elif self.robot[i][j] != other.robot[i][j] : 
                    difference += 0.75

        phenotype_distance = difference/(self.robot_size**2) # Normalizing between 0 and 1        
        return self.spec_genotype_weight*genotype_distance + self.spec_phenotype_weight*phenotype_distance

            