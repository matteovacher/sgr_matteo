import math 
from evogym.utils import get_full_connectivity 
import evogym.envs 
import imageio 
import numpy as np 
import gymnasium as gym 

def get_env(robot, connections, env_name, render_mode=None) :
    env = gym.make(env_name, body=robot, connections=connections, render_mode=render_mode)
    return env.unwrapped 

def get_observation_size(robot, env_name) : 
    connections = get_full_connectivity(robot)
    env = get_env(robot, connections, env_name)
    # here reset return (obs, info_dict) but we dont want this dict 
    observation, _ = env.reset()
    env.close()
    del env 
    return len(observation)

def simulate_env(robot, network, env_name, n_steps, save_gif_name=None) :
    connections = get_full_connectivity(robot)
    render_mode = "rgb_array" if save_gif_name is not None else None
    env = get_env(robot, connections, env_name, render_mode=render_mode)
    reward = 0 
    observation, _ = env.reset()
    actuators = env.get_actuator_indices("robot")
    inputs_size = math.ceil(math.sqrt(len(observation)))

    finished = False
    images = []
    
    for step in range (n_steps) : 
        if render_mode == "rgb_array" : 
            frame = env.render()
            images.append(frame)
        
        observation.resize(inputs_size**2, refcheck = False )
        action_by_actuator = network.activate(observation)
        action = np.array([action_by_actuator[i] for i in actuators])

        observation, step_reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated 

        reward += step_reward 

        if done : 
            finished = True 
            break 

    env.close()
    del env 
    if render_mode == "rgb_array" : 
        imageio.mimsave(save_gif_name + ".gif", images, duration=(1/60))

    return reward, finished 
        

