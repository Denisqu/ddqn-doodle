import gym
from gym import spaces
import numpy as np

# https://www.gymlibrary.dev/content/environment_creation/
class DoodleEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Box(low=0, high=255, dtype=np.ubyte)
        self.action_space = spaces.Discrete(2)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode