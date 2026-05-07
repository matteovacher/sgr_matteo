import neat 
import os 
import math 
import errno 
import multiprocess 
import dill 
import numpy as np 

from sgr.substrates import morph_substrate_shape_builder, control_substrate_shape_builder
from sgr.body_speciation import MorphoAwareGenome
from sgr.generate_robot import generate_robot_from_substrate, is_valid_robot
from hyperneat.hyper_neat import create_phenotype_network
from sgr.evogym_sim import get_observation_size, simulate_env


from pathos.multiprocessing import ProcessPool

class SGR : 
    _id_counter = None

    @classmethod
    def _init_id_counter(myclass) : 
        if myclass._id_counter is None : 
            myclass._id_counter = 0

    @classmethod
    def _get_next_id(myclass) :
        if myclass._id_counter is None :
            raise RuntimeError("ID counter not initialized. Please call SGR._init_id_counter() before creating any instance of SGR.")
        current_id = myclass._id_counter
        myclass._id_counter += 1
        return current_id
    

    def __init__(
        self,
        neat_config_path,
        robot_size,
        spec_genotype_weight,
        spec_phenotype_weight,
        pop_size,
        save_to="",
        reporters=True
    ) :
        self.id = self._get_next_id() 

        morphology_coordinates = morph_substrate_shape_builder(robot_size)
        self.input_size_of_cppn = morphology_coordinates.dimensions*2 + 1 # two coordinates plus the bias
        self.pop_size = pop_size
        self.robot_size = robot_size
        self.save_to = save_to

        self.neat_config = self._create_neat_config(neat_config_path)
        MorphoAwareGenome.configure(self.neat_config, morphology_coordinates, robot_size, spec_genotype_weight, spec_phenotype_weight)
        
        self.pop = neat.Population(self.neat_config)

        if reporters : 
            self._add_reporters()

        self.voxel_types = ['empty', 'rigid', 'soft', 'hori', 'vert']

        self.best_fit = -10000
        self.stagnation = 0
        self.generation = 0 
        self.save_gen_interval = None



    def _create_neat_config(self, neat_config_path) : 
        neat_config = neat.Config(MorphoAwareGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, neat_config_path)

        # ovewriting pop_size from the neat config file
        neat_config.pop_size = self.pop_size

        # overwriting the num_inputs and num_outputs from the neat config file to fit the substrate
        neat_config.genome_config.num_inputs = self.input_size_of_cppn
        neat_config.genome_config.input_keys = [-1*i for i in range(1, self.input_size_of_cppn+1)]
        neat_config.genome_config.num_outputs = 2
        neat_config.genome_config.output_keys = [1, 2]

        return neat_config
    
    def _add_reporters(self) : 
        self.pop.add_reporter(neat.StdOutReporter(True))
        if self.save_to != "" :
            parent = os.path.dirname(self.save_to)
            if parent != "" : 
                os.makedirs(parent, exist_ok=True)
            # self.pop.add_reporter(CustomReporter(True , self.save_to + "_out.txt", self.save_to + "_table.csv"))
    
    def single_genome_fitness(self, 
                            genome, 
                            n_steps, 
                            env_name,
                            render = False, 
                            save_gif = None  
                            ) : 
        """Here the function is more like a simulation of un robot ahah and building the controller by the way"""
        cppn = neat.nn.FeedForwardNetwork.create(genome, self.neat_config)

        if hasattr(genome, 'robot') : 
            robot = genome.robot
        else : 
            design_substrate = morph_substrate_shape_builder(self.robot_size)
            design_network = create_phenotype_network(cppn, design_substrate, output_node_idx=0)
            robot = generate_robot_from_substrate(design_network, self.robot_size)
            genome.robot = robot

        if not is_valid_robot(robot) :
            return -10000, False 
        
        observator_size = get_observation_size(robot, env_name) 
        grid_input_size = math.ceil(math.sqrt(observator_size))

        try : 
            controller_substrate = control_substrate_shape_builder(self.robot_size, grid_input_size)
        except IndexError : 
            print("Error in building the controller substrate.")
            return -10000, False 
        
        controller_network = create_phenotype_network(cppn, controller_substrate, output_node_idx=1)

        reward, done = simulate_env(robot, controller_network, env_name, n_steps, save_gif_name=save_gif)

        return reward, done

    def fitness_function_worker(self, genomes, n_steps, env_name) : 
        results_dict = {}
        for genome_key, genome in genomes :
            reward, _ = self.single_genome_fitness(genome, n_steps, env_name)
            results_dict[genome_key] = reward
        return results_dict


    def fitness_function(self, genomes, neat_config, env_name, n_steps, cpus) : 
        self.stagnation += 1
         
        try : 
            pool = ProcessPool(nodes=cpus)
            results_map = pool.amap(
                self.fitness_function_worker, 
                np.array_split(genomes, cpus),
                [n_steps for _ in range (cpus)],
                [env_name for _ in range (cpus)],
            )
            results = results_map.get(timeout=60*10)
        
            fitness_dictionary = {}
            for result_dictionary in results : 
                for key, value in result_dictionary.items() : 
                    fitness_dictionary[key] = value
            
            for genome_id, genome in genomes : 
                genome.fitness = fitness_dictionary[genome_id]
                if genome.fitness > self.best_fit : 
                    self.best_fit = genome.fitness
                    self.stagnation = 0
                    
            
        except IOError as e : 
            if e.errno == errno.EPIPE : 
                print("Problem with broken pipe")
            else : 
                raise(IOError)
        except multiprocess.context.TimeoutError as e:
            print("Deu timeout!!!!!!")
            for genome_id, genome in genomes :
                if genome.fitness is None :
                    genome.fitness = -1000
        
        pool.terminate()
        pool.clear()
        surviving_genomes = {genome_id: genome for genome_id, genome in genomes if genome.fitness is not None and genome.fitness > -1000}
        self.pop.population = surviving_genomes

        self._check_stagnation_and_save()
    
    def _check_stagnation_and_save(self):
    
        if self.max_stagnation is not None and self.stagnation > self.max_stagnation :
            print("Population stagnated.")
            if self.save_to != "" :
                with open(self.save_to + "_pop.pkl", mode='wb') as f:
                    dill.dump(self.pop, f)
            raise RuntimeError("Population stagnated.")
        
        if (
            self.save_to != ""
            and self.save_gen_interval is not None
            and (self.pop.generation + 1) % self.save_gen_interval == 0
        ):
            path = f"{self.save_to}_pop_gen_{self.pop.generation}.pkl"
            with open(path, mode='wb') as f:
                dill.dump(self.pop, f)
            
        

    def _neat_fitness_function(self, genomes, neat_config) : 
        return self.fitness_function(genomes, neat_config, self.env_name, self.n_steps, self.cpus)

        
    def run(self, env_name, n_steps, n_gens, cpus=1, max_stagnation=None, save_gen_interval=None, print_results=True) :
        self.max_stagnation = max_stagnation
        self.save_gen_interval = save_gen_interval

        self.env_name = env_name
        self.n_steps = n_steps  
        self.cpus = cpus    

        winner = self.pop.run(self._neat_fitness_function, n_gens)

        if print_results :
            print("Best genome:\n{!s}".format(winner))
        
        if self.save_to != "" :
            with open(self.save_to + "_pop.pkl", mode='wb') as f:
                dill.dump(self.pop, f)  
        
        return winner
            




    
    


        


