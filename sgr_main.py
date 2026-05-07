import os 
import sys 
from config import SGRConfig
from sgr.sgr import SGR

def main() : 
    local_dir = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) > 1 : 
        config_path = os.path.join(local_dir, sys.argv[1])
    else : 
        config_path = os.path.join(local_dir, "configs/configs.json")

    print(f"config_path : ", config_path) 

    config = SGRConfig(config_path, local_dir)
    SGR._init_id_counter()
    pop = SGR(
        config.neat_config,
        config.robot_size,
        config.spec_genotype_weight,
        config.spec_phenotype_weight,
        config.pop_size,
        config.save_to
    )

    pop.run(config.env, config.steps, config.gens, config.cpus, config.max_stagnation, config.save_gen_interval)

if __name__ == "__main__" :
    main()

