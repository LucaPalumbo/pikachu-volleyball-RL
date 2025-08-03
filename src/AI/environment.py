import numpy as np
import gymnasium as gym
from gymnasium.utils import seeding
from game import pikaVolley
from game import pikaUserInput
from game import constants as c 
import random

class PikaVolleyEnv(gym.Env):
    def __init__(self, render_mode=None, original_algo=False):
        super(PikaVolleyEnv, self).__init__()
        self.render_mode = render_mode
        self.display = render_mode == "human"
        self.original_algo = original_algo

        self.action_space = gym.spaces.MultiDiscrete([3, 3, 2])

        # self.game = pikaVolley.PikachuVolleyball(self.original_algo, False, self.display)
        # self.game.startOfNewGame()
        self.current_step = 0
        self.max_steps = 2000
        self.seed()

        self.observation_space = gym.spaces.Box(
            low=np.array([
                0, 0, -100, 0, -1 , -2,                      # player1
                c.GROUND_HALF_WIDTH, 0, -100, 0, -1 , -2,    # player2
                0, 0, -100, -100,                            # ball
                0.0,                                         # isPowerHit
            ], dtype=np.float32),
            high=np.array([
                c.GROUND_HALF_WIDTH, c.HEIGHT, 100, 6, 1, 3, # player1
                c.GROUND_WIDTH, c.HEIGHT, 100, 6, 1, 3,      # player2
                c.GROUND_WIDTH, c.HEIGHT, 100, 100,          # ball
                1.0,                                         # isPowerHit
            ], dtype=np.float32),
            dtype=np.float32
        )
        self.window = None
        self.clock = None

        self.consecutive_hits = 0

    def render(self):
        if self.render_mode == "human":
            self.game.draw()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _get_obs(self):
        player1 = self.game.physics.player1
        player2 = self.game.physics.player2
        ball = self.game.physics.ball
        return np.array([
            player1.x, player1.y, player1.yVelocity, player1.state, player1.divingDirection, player1.lyingDownDurationLeft,
            player2.x, player2.y, player2.yVelocity, player2.state, player2.divingDirection, player2.lyingDownDurationLeft,
            ball.x, ball.y, ball.xVelocity, ball.yVelocity, float(ball.isPowerHit),
        ], dtype=np.float32)
       

    def reset(self, seed=None, options=None, match=False, isPlayer2Serve=False):
        super().reset(seed=seed)
        if seed is not None:
            self.seed(seed)


        self.game = pikaVolley.PikachuVolleyball(isPlayer1Computer=self.original_algo, isPlayer2Computer=False, display=self.display)
        self.game.physics.player2.isPlayer2Serve = isPlayer2Serve
        self.game.startOfNewGame()

        # Bind ai/opp player
        self.ai_player = self.game.physics.player2 #if self.ai_position == "right" else self.game.physics.player1
        self.opp_player = self.game.physics.player1 #if self.ai_position == "right" else self.game.physics.player2

        self.ball_in_ai_half = (lambda x: x >= c.GROUND_HALF_WIDTH) #if self.ai_position == "right" else (lambda x: x < c.GROUND_HALF_WIDTH)

        # self.game.physics.player2.x = c.GROUND_HALF_WIDTH + c.PLAYER_LENGTH
        # self.game.physics.ball.x = c.GROUND_HALF_WIDTH + c.PLAYER_LENGTH

        # Reset positions
        if not match:
            self.game.physics.ball.x = self.generate_position("any")
            self.game.physics.ball.xVelocity = random.randint(-10, 10)
            self.game.physics.player1.x = self.generate_position("left")
            self.game.physics.player2.x = self.generate_position("right")
        self.current_step = 0
        self.consecutive_hits_delta = 1

        return self._get_obs(), {}

    def step(self, action, opponent_action=None):
        
        pre_ball_x = self.game.physics.ball.x
        pre_dist_ball = abs(self.ai_player.x - self.game.physics.ball.x)
        user_input = self._action_to_userinput(action)
        if opponent_action is None:
            opponent_input = pikaUserInput.PikaUserInput()
        else:
            opponent_input = self._action_to_userinput(opponent_action)

        actions = [opponent_input, user_input] # if self.ai_position == "right" else [user_input, opponent_input]

        isBallTouchingGround = self.game.physics.runEngineForNextFrame(actions)

        reward = self._calculate_reward(pre_ball_x, pre_dist_ball, user_input, isBallTouchingGround)

        self.current_step += 1
        terminated = isBallTouchingGround
        truncated = self.current_step >= self.max_steps

        return self._get_obs(), reward, terminated, truncated, {}

    def _calculate_reward(self, pre_ball_x, pre_dist_ball, input, isBallTouchingGround):
        reward = 0

        # penalty for actions taken
        if input.powerHit == 1:
            reward -= 0.2
            if self.display:
                print("Power hit, penalty applied (-0.2).")

        if input.yDirection == -1:
            reward -= 0.3
            if self.display:
                print("Player is jumping, penalty applied (-0.3).")


        # reward for ball passing the net
        if self.has_ball_passed_net(pre_ball_x):
            reward += 14
            self.consecutive_hits_delta = 1
            if self.display:
                print("Ball passed the net, reward applied (+14).")

        if self.has_ball_passed_net(pre_ball_x) and self.game.physics.ball.isPowerHit:
            reward += 1
            if self.display:
                print("Ball passed the net with power hit, reward applied (+1).")

        # reward for collisions
        if self.ai_player.isCollisionWithBallHappened:
            reward += 5 * self.consecutive_hits_delta
            if self.display:
                print("Player hit the ball, reward applied (+5x{}).".format(self.consecutive_hits_delta))
            self.consecutive_hits_delta *= 0.8
            

        if self.ai_player.isCollisionWithBallHappened and input.powerHit == 1:
            reward += 1
            if self.display:
                print("Player power hit, reward applied (+1).")
            
        if self.ai_player.isCollisionWithBallHappened and input.powerHit == 0 and self.ai_player.y == c.PLAYER_TOUCHING_GROUND_Y_COORD:
            reward += 1
            if self.display:
                print("Player is touching the ball while on ground, reward applied (+1).")

        if self.ai_player.isCollisionWithBallHappened and self.ai_player.state == 2 and self.ai_player.x > c.GROUND_HALF_WIDTH * 5/4 and input.yDirection == 1:
            reward -= 7
            if self.display:
                print("Player is smashing while it's not supposed to, penalty applied (-7).")

        # reward for tactics
        # player state 2 == jumping and power hitting; 
        if self.ai_player.isCollisionWithBallHappened and self.ai_player.state == 2 and self.ai_player.x < c.GROUND_HALF_WIDTH * 5/4  and input.yDirection == 1: 
            reward += 3
            if self.display:
                print("Player is smashing, reward applied (+3).")

        if self.ai_player.isCollisionWithBallHappened and self.ai_player.state == 2 and self.ai_player.x >= c.GROUND_HALF_WIDTH * 7/4 and input.xDirection != 0 and input.yDirection == 0:
            reward += 3
            if self.display:
                print("Player is serving, reward applied (+3).")
        
        # reward for diving
        if self.ai_player.state == 3 and self.ball_in_ai_half(self.game.physics.ball.x):
            signed_distance = self.game.physics.ball.x - self.ai_player.x
            if signed_distance > c.GROUND_HALF_WIDTH / 2 and self.ai_player.divingDirection == -1:
                reward += 2
            if signed_distance < -c.GROUND_HALF_WIDTH / 2 and self.ai_player.divingDirection == 1:
                reward += 2
            if self.display:
                print("Player is diving towards the ball, reward applied (+2).")

        # reward / penalty for point scoring
        if isBallTouchingGround:
            if self.ball_in_ai_half(self.game.physics.ball.x):
                reward -= 70
                if self.display:
                    print("Ball touching ground on ai's side, penalty applied (-70).")
            else:
                reward += 70
                if self.display:
                    print("Ball touching ground on opponent's side, reward applied (+70).")


        # reward for getting closer to the ball
        if abs(self.ai_player.x - self.game.physics.ball.x) < pre_dist_ball and self.ball_in_ai_half(self.game.physics.ball.x):
            reward += 0.1
            if self.display:
                print("Player is getting closer to the ball, reward applied (+0.1).")
        
        # penalty for being above the ball
        # remember that y = 0 is the top of the screen
        if self.ai_player.y < self.game.physics.ball.y and self.ball_in_ai_half(self.game.physics.ball.x):
            reward -= 1
            if self.display:
                print("Player is above the ball, penalty applied (-1).")
        
        # penalty for not being in the middle of the ground
        reward -= abs(self.ai_player.x - c.GROUND_HALF_WIDTH* 3/2) / (c.GROUND_HALF_WIDTH*3/2)

        return reward

    def _action_to_userinput(self, action):
        x_action, y_action, power_action = action
        return pikaUserInput.PikaUserInput(
            xDirection=x_action - 1,
            yDirection=y_action - 1,
            powerHit=power_action
        )

    def has_ball_passed_net(self, pre_ball_x):
        ball_x = self.game.physics.ball.x
        return (
            ball_x < c.GROUND_HALF_WIDTH and pre_ball_x >= c.GROUND_HALF_WIDTH
            #if self.ai_position == "right"
            #else ball_x > c.GROUND_HALF_WIDTH and pre_ball_x <= c.GROUND_HALF_WIDTH
        )

    def generate_position(self, side):
        if side == "right":
            return random.randint(c.GROUND_HALF_WIDTH+c.BALL_RADIUS, c.GROUND_WIDTH-c.BALL_RADIUS)
        elif side == "left":
            return random.randint(c.BALL_RADIUS, c.GROUND_HALF_WIDTH-1-c.BALL_RADIUS)
        elif side == "any":
            return random.randint(c.BALL_RADIUS, c.GROUND_WIDTH-1-c.BALL_RADIUS)

    def close(self):
        self.game.close()
