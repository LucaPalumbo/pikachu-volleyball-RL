import pygame
from .constants import *
import sys
from .player import Player
from .physicsEngine import physicsEngine
from .pikaPhysics import PickaPhysics
from .pikaUserInput import PikaUserInput



# Window dimensions
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


# Calculate offsets to center the field
FIELD_OFFSET_X = (GROUND_WIDTH - GROUND_WIDTH) // 2
FIELD_OFFSET_Y = (HEIGHT - PLAYER_TOUCHING_GROUND_Y_COORD - PLAYER_LENGTH) // 2



class PikachuVolleyball:
    def __init__(self, isPlayer1Computer: bool, isPlayer2Computer: bool, display=False):
        pygame.init()

        self.physics = PickaPhysics(isPlayer1Computer, isPlayer2Computer)
        self.scores = [0, 0]  # Player 1 and Player 2 scores
        self.display = display
        if self.display:
            self.screen = pygame.display.set_mode((GROUND_WIDTH, HEIGHT))
            pygame.display.set_caption("Volleyball 2D")
            self.clock = pygame.time.Clock()

    def run(self, userInputArray):
        isBallTouchingGround = self.physics.runEngineForNextFrame(userInputArray)
        return isBallTouchingGround

    def startOfNewGame(self):
        self.scores = [0, 0]
        self.physics.player1.initializeForNewRound()
        self.physics.player2.initializeForNewRound()
        self.physics.ball.initializeForNewRound(self.physics.player2.isPlayer2Serve)

    def round(self):
        # Handle events
        power_hit_left = False
        power_hit_right = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    power_hit_right = True
                # if shift is pressed, trigger power hit for right player
                if event.key == pygame.K_LSHIFT:
                    power_hit_left = True
        # Continuous input reading
        keys_pressed = pygame.key.get_pressed()
        
        # Left player movement (WASD)
        dx_left, dy_left = 0, 0
        if keys_pressed[pygame.K_a]:  # Left
            dx_left = -1
        if keys_pressed[pygame.K_d]:  # Right
            dx_left = 1
        if keys_pressed[pygame.K_w]:  # Up
            dy_left = -1
        if keys_pressed[pygame.K_s]:  # Down
            dy_left = 1
        
        # Right player movement (Arrow keys)
        dx_right, dy_right = 0, 0
        if keys_pressed[pygame.K_LEFT]:   # Left
            dx_right = -1
        if keys_pressed[pygame.K_RIGHT]:  # Right
            dx_right = 1
        if keys_pressed[pygame.K_UP]:     # Up
            dy_right = -1
        if keys_pressed[pygame.K_DOWN]:   # Down
            dy_right = 1

        userInputArray = [ PikaUserInput(xDirection=dx_left, yDirection=dy_left, powerHit=1 if power_hit_left else 0),
                           PikaUserInput(xDirection=dx_right, yDirection=dy_right, powerHit=1 if power_hit_right else 0) ]
        ifBallTouchingGround = self.physics.runEngineForNextFrame(userInputArray)

        if self.display:
            self.draw()

        if ifBallTouchingGround:
            print("Ball touching ground!")
            self.physics.ball.initializeForNewRound(self.physics.player2.isPlayer2Serve)
        
        # wait for a short time to control the frame rate
        # pygame.time.delay(100)


    def draw(self):
        draw_field(self.screen)
        self.physics.player1.draw(self.screen)
        self.physics.player2.draw(self.screen)
        self.physics.ball.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(FPS)


    def close(self):
        if self.display:
            pygame.quit()



def draw_field(screen):
    # Background
    screen.fill(GREEN)
    
    # Ground area
    ground_rect = pygame.Rect(FIELD_OFFSET_X, FIELD_OFFSET_Y, GROUND_WIDTH, PLAYER_TOUCHING_GROUND_Y_COORD + PLAYER_LENGTH)
    pygame.draw.rect(screen, GREEN, ground_rect)
    
    # Center line
    center_x = FIELD_OFFSET_X + GROUND_HALF_WIDTH
    pygame.draw.line(screen, WHITE, (center_x, FIELD_OFFSET_Y), (center_x, FIELD_OFFSET_Y + PLAYER_TOUCHING_GROUND_Y_COORD + PLAYER_LENGTH), 3)
    
    # Net pillar
    net_x = center_x - NET_PILLAR_HALF_WIDTH
    net_y = FIELD_OFFSET_Y + NET_PILLAR_TOP_TOP_Y_COORD
    net_width = NET_PILLAR_HALF_WIDTH * 2
    net_height = PLAYER_TOUCHING_GROUND_Y_COORD + PLAYER_LENGTH - NET_PILLAR_TOP_TOP_Y_COORD
    pygame.draw.rect(screen, BROWN, (net_x, net_y, net_width, net_height))
    
    # Net top (darker brown)
    net_top_height = NET_PILLAR_TOP_BOTTOM_Y_COORD - NET_PILLAR_TOP_TOP_Y_COORD
    pygame.draw.rect(screen, (100, 50, 0), (net_x, net_y, net_width, net_top_height))
    
    # Field boundaries
    pygame.draw.rect(screen, WHITE, ground_rect, 3)


