import pygame
from environment import PikaVolleyEnv  
from stable_baselines3.common.vec_env import DummyVecEnv
import pygame
import sys
from rl_model import RLModel
from game import constants as c
import numpy as np

# -----------------------------
# Funzione per visualizzare una partita
# -----------------------------
def play_episode():
    env = PikaVolleyEnv(render_mode="human")
    # load model from file
    # agent_model = RLModel(env, is_on_right=True)
    # opponent_model = RLModel(env, is_on_right=False)
    # agent_model.load("ppo_pikavolley_iter")
    # opponent_model.load("ppo_pikavolley_iter")
    agent_model = RLModel.load("ppo_pikavolley_iter")
    opponent_model = RLModel.load("ppo_pikavolley_iter")
    opponent_model.is_on_right = False

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


def play_match(max_score=15):
    scores = [0, 0]

    env = PikaVolleyEnv(render_mode="human")
    agent_model = RLModel.load("ppo_pikavolley_iter")
    opponent_model = RLModel.load("ppo_pikavolley_iter")
    opponent_model.is_on_right = False
    isPlayer2Serve = False

    while all(score < max_score for score in scores):
        obs, _ = env.reset(match=True, isPlayer2Serve=isPlayer2Serve)
        terminated = False
        truncated = False
        agent_action = np.array([1, 1, 0]) # Default action (stay)
        opponent_action = np.array([1, 1, 0]) # Default action (stay)

        while not (terminated or truncated):

            with open("obs.txt", "a") as f:
                f.write(str(obs.tolist())+"\n")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            agent_action, _ = agent_model.predict(obs, deterministic=False)
            opponent_action, _ = opponent_model.predict(obs, deterministic=False)

            obs, reward, terminated, truncated, info = env.step(agent_action, opponent_action)
            # obs, reward, terminated, truncated, info = env.step(agent_action, opponent_action)
            
            env.render()
            pygame.time.delay(40)

            
        if terminated and env.game.physics.ball.x < c.GROUND_HALF_WIDTH:
            scores[1] += 1
            isPlayer2Serve = True
            print("🏆 Player 2 wins the set! Score:", scores)
        elif terminated and env.game.physics.ball.x >= c.GROUND_HALF_WIDTH:
            scores[0] += 1
            isPlayer2Serve = False
            print("🏆 Player 1 wins the set! Score:", scores)

    env.close()


def play_against_algo():
    env = PikaVolleyEnv(render_mode="human", original_algo=True)
    # load model from file
    # agent_model = RLModel(env, is_on_right=True)
    # agent_model.load("ppo_pikavolley_iter")
    agent_model = RLModel.load("ppo_pikavolley_iter", env=env)
    agent_model.is_on_right = True

    obs, _ = env.reset()
    terminated = False
    truncated = False

    while not (terminated or truncated):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    

        agent_action, _ = agent_model.predict(obs, deterministic=False)

        obs, reward, terminated, truncated, info = env.step(agent_action)
        
        env.render()
        pygame.time.delay(100)

    env.close()



if __name__ == "__main__":
    play_match(max_score=5)
    # play_episode()
    # play_against_algo()