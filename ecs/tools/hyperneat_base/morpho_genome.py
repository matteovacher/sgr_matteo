import neat 


class MorphoAwareGenome(neat.DefaultGenome) :
    neat_config = None

    def __init__(self, key) : 
        super().__init__(key)
        self.robot = None # will be written outside 
        if MorphoAwareGenome.neat_config is None :
            raise RuntimeError("Please set the neat_config attribute of MorphoAwareGenome before creating any instance of it.")

    @classmethod
    def configure(myclass, neat, robot_size, spec_genotype_weight, spec_phenotype_weight) : 
        myclass.neat_config = neat
        myclass.robot_size = robot_size
        myclass.spec_genotype_weight = spec_genotype_weight
        myclass.spec_phenotype_weight = spec_phenotype_weight
         

    def distance(self, other, _) : 

        genotype_distance = super().distance(other, MorphoAwareGenome.neat_config.genome_config)
        
        if self.robot is None or other.robot is None : 
            return self.spec_genotype_weight*genotype_distance
    
        difference = 0 
        for i in range(self.robot_size) : 
            for j in range(self.robot_size) : 
                if (self.robot[i][j] == 0 and other.robot[i][j] != 0) or (self.robot[i][j] != 0 and other.robot[i][j] == 0) : 
                    difference += 1
                elif self.robot[i][j] != other.robot[i][j] : 
                    difference += 0.75

        phenotype_distance = difference/(self.robot_size**2) # Normalizing between 0 and 1        
        return self.spec_genotype_weight*genotype_distance + self.spec_phenotype_weight*phenotype_distance

