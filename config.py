import json
import os 



class SGRConfig : 

    def __init__(self, json_path, project_root) : 
        with open(json_path, 'r') as f : 
            data = json.load(f)
        
        self.neat_config = os.path.join(project_root, data["neat_config"])
        self.robot_size = data["robot_size"]
        self.spec_genotype_weight = data["spec_genotype_weight"]
        self.spec_phenotype_weight = data["spec_phenotype_weight"]
        self.pop_size = data["pop_size"]
        self.save_to = data["save_to"]

        self.env = data["env"]
        self.steps = data["steps"]
        self.gens = data["gens"]
        self.cpus = data["cpus"]
        self.max_stagnation = data["max_stagnation"]
        self.save_gen_interval = data["save_gen_interval"]

