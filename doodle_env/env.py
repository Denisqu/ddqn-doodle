import gym
from gym import spaces
import torch
import numpy as np
from networking.mlclient import MLClient

# https://www.gymlibrary.dev/content/environment_creation/
class DoodleEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Box(low=0, high=255, shape=[84,84,3], dtype=np.uint8)
        self.action_space = spaces.Discrete(2)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.ml_client = MLClient()
        self.ml_client.make_send_receive()

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        
        obs_tensor = self.ml_client.reset_send_receive()
        print(f"obs_tensor = {obs_tensor}, it's shape = {obs_tensor.shape}")

        return obs_tensor
    
    def step(self, action):
        action_map = {0: "L", 1: "R"}
        next_state_tensor, reward, done = self.ml_client.step_send_receive(action_map[action])
        return next_state_tensor, reward, done, {"test":123}
    
    def render(self):
        pass

    def close(self):
        self.ml_client.close()


from gym.envs.registration import register

register(
    id='doodle-env',
    entry_point='doodle_env.env:DoodleEnv',
    max_episode_steps=100000,
)