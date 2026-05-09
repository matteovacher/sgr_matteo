import gymnasium as gym
import math
import numpy as np 

from evogym.utils import get_full_connectivity 


class RobotSimulator : 
    def __init__(self, env_name, n_steps) : 
        self.env_name = env_name
        self.n_steps = n_steps 

    def _get_env(self, robot) : 
        connections = get_full_connectivity(robot)
        env = gym.make(self.env_name, body=robot, connections=connections)
        return env.unwrapped  
    
    def get_observation_size(self, robot) : 
        env = self._get_env(robot)
        observation, _ = env.reset()
        env.close()
        del env 
        return len(observation)
    
    def simulate(self, robot, controller) :
        env = self._get_env(robot)
        reward = 0 
        observation, _ = env.reset()

        actuators = env.get_actuator_indices("robot")
        inputs_size = math.ceil(math.sqrt(len(observation)))

        finished = False 

        for _ in range(self.n_steps) : 
            observation.resize(inputs_size**2, refcheck = False)
            all_actions = controller.activate(observation)
            action = np.array([all_actions[i] for i in actuators])
            observation, step_reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated 

            reward += step_reward 

            if done : 
                finished = True 
                break

        env.close()
        del env 
        return reward, finished