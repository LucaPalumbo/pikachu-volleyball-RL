import gymnasium as gym
import pygame
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from environment import PikaVolleyEnv  
from SelfPlayEnv import SelfPlayEnv  
from stable_baselines3.common.vec_env import DummyVecEnv
import pygame
import sys
from rl_model import RLModel


# -----------------------------
# Funzione per visualizzare una partita
# -----------------------------
def play_episode(agent_model, opponent_model):
    env = PikaVolleyEnv(render_mode="human")
    # load model from file
    # agent_model = PPO.load("ppo_pikavolley_iter")
    # opponent_model = PPO.load("ppo_pikavolley_iter")

    obs, _ = env.reset()
    terminated = False
    truncated = False

    while not (terminated or truncated):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    


        agent_action, _ = agent_model.predict(obs, deterministic=True)
        opponent_action, _ = opponent_model.predict(obs, deterministic=True)

        obs, reward, terminated, truncated, info = env.step(agent_action, opponent_action)
        
        env.render()
        pygame.time.delay(100)

    env.close()

# -----------------------------
# TRAINING MAIN
# -----------------------------
if __name__ == "__main__":
    policy_kwargs = {
        "net_arch": {
            "pi": [64, 128, 64, 32],      # Policy network
            "vf": [64, 64, 64]     # Value network
        }
    }

    # 1. Create the opponent model
    dummy_env = PikaVolleyEnv()
    dummy_env = Monitor(dummy_env)
    dummy_env = DummyVecEnv([lambda: dummy_env])
    opponent_model = RLModel("MlpPolicy", dummy_env, is_on_right=False, policy_kwargs=policy_kwargs)
    # opponent_model = RLModel.load("ppo_pikavolley_iter", dummy_env, is_on_right=False) 

    # 2. create environment for self-play
    env = SelfPlayEnv(opponent_model)
    env = Monitor(env)
    vec_env = DummyVecEnv([lambda: env]) 

    # 3. Create the agent model to train
    model = RLModel("MlpPolicy", vec_env, verbose=1, is_on_right=True, policy_kwargs=policy_kwargs)  #PPO("MlpPolicy", vec_env, verbose=1)
    # model = RLModel.load("ppo_pikavolley_iter", vec_env, is_on_right=True)  

    # 4. Training loop
    for i in range(100):
        print(f"\n🎯 Start training block {i}")
        model.learn(total_timesteps=30_000, reset_num_timesteps=False)

        if i % 5 == 0 and i != 0:
            print("♻️  Updating opponent model with latest weights")
            opponent_model.set_parameters(model.get_parameters())

        if i % 1 == 0:
            print("👁️  Visualizing test match")
            play_episode(agent_model=model, opponent_model=opponent_model)

        # Salva il modello ogni 20 blocchi
        if i % 1 == 0:
            print(f"💾 Saving model at block {i}")
            model.save(f"ppo_pikavolley_iter")
