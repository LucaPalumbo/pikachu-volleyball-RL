

from stable_baselines3 import PPO
import numpy as np
from game import constants as c


class RLModel(PPO):
    def __init__(self, policy, env, is_on_right=True, **kwargs):
        super().__init__(policy, env, **kwargs)
        self.is_on_right = is_on_right

    def predict(self, observation, deterministic=True):
        if not isinstance(observation, np.ndarray):
            observation = np.array(observation, dtype=np.float32)

        if not self.is_on_right:
            # Invert relevant observation components
            observation = np.array([
                c.GROUND_WIDTH - observation[6], observation[7], observation[8], observation[9], 1-observation[10], observation[11],
                c.GROUND_WIDTH - observation[0], observation[1], observation[2], observation[3], 1-observation[4], observation[5],
                c.GROUND_WIDTH - observation[12], observation[13], -observation[14], observation[15], observation[16]
            ], dtype=np.float32)
            # observation[0] = c.GROUND_WIDTH - observation[0]
            # observation[3] = c.GROUND_WIDTH - observation[3]
            # observation[6] = c.GROUND_WIDTH - observation[6]
            # observation[8] = -observation[8]
        # print(observation)

        action, _ = super().predict(observation, deterministic=deterministic)

        if not self.is_on_right:
            action[0] = 2 - action[0]  # Flip left/right action (0: left, 1: stay, 2: right)

        return action, _