import gymnasium as gym
from environment import PikaVolleyEnv

class SelfPlayEnv(gym.Env):
    def __init__(self, model_opponent, render_mode=None):
        self.env = PikaVolleyEnv(render_mode)
        self.model_opponent = model_opponent
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)

    def step(self, action):
        obs = self.env._get_obs()

        opponent_action, _ = self.model_opponent.predict(obs, deterministic=True)
        return self.env.step(action, opponent_action)


    def render(self):
        self.env.render()

    def close(self):
        self.env.close()
