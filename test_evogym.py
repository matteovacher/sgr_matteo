import numpy as np 
import gymnasium as gym 
import evogym.envs
from evogym.utils import is_connected, has_actuator
from evogym.utils import get_full_connectivity

body = np.array([[3, 3, 3, 3, 3],
                 [1, 1, 1, 1, 1],
                 [1, 1, 0, 1, 1],
                 [1, 1, 0, 1, 1],
                 [3, 1, 0, 1, 3]], dtype=int)

def test_robot_validity(body) : 
    assert is_connected(body) == True
    assert has_actuator(body) == True
    return get_full_connectivity(body)

connections = test_robot_validity(body)

print(f"body shape is {body.shape}")
print(f"connection shape is {connections.shape}")

# puis on créer l'env 
env = gym.make('Walker-v0', body=body, connections=connections)
env = env.unwrapped

obs, info = env.reset()
actuators = env.get_actuator_indices("robot")
print(f"obs shape is {obs.shape}")
print(f"number of actuators is {len(actuators)}")
print(f"actuator_indices: {actuators}")

# la boucle 
n_steps = 100
total_reward = 0
for step in range(n_steps) :
    action = np.ones(len(actuators)) 
    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward  
    if terminated or truncated:
        break

print(f"Episode finished after and steps : {step}, total reward: {total_reward:.3f}")

env.close()
