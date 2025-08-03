from .constants import *
import random
import pygame
from .sound import Sound



class Player:
    def __init__(self, isPlayer2: bool, isComputer: bool):
        self.isPlayer2 = isPlayer2 # Is this player on the right side? 
        self.isComputer = isComputer # Is controlled by computer?
        self.divingDirection = 0 # -1: left, 0: no diving, 1: right 
        self.lyingDownDurationLeft = 0 
        self.isWinner = False
        self.gameEnded = False
        self.computerWhereToStandBy = 0 #  0: middle, 1: by net


        self.x = 0
        self.y = 0
        self.computerBoldness = 0 # 0, 1, 2, 3 or 4
        self.state = 0 # 0: normal, 1: jumping, 2: jumping_and_power_hitting, 3: diving, 4: lying_down_after_diving, 5: win!, 6: lost..
        self.yVelocity = 0
        self.delayBeforeNextFrame = 0
        self.isCollisionWithBallHappened = False
        self.isPlayer2Serve = False
        self.sound = Sound()  # Sound effects for the player


    def initializeForNewRound(self):
        self.x = 36
        if self.isPlayer2:
            self.x = GROUND_WIDTH - 36
        
        self.y = PLAYER_TOUCHING_GROUND_Y_COORD
        self.yVelocity = 0
        self.isCollisionWithBallHappened = False

        # /**
        # * Player's state
        # * 0: normal, 1: jumping, 2: jumping_and_power_hitting, 3: diving
        # * 4: lying_down_after_diving
        # * 5: win!, 6: lost..
        # * 0, 1, 2, 3, 4, 5 or 6
        # */
        self.state = 0 
        self.frameNumber = 0
        self.normalStatusArmSwingDirection = 1
        self.delayBeforeNextFrame = 0


        # /**
        # * This value is initialized to (_rand() % 5) before the start of every round.
        # * The greater the number, the bolder the computer player.
        # *
        # * If computer has higher boldness,
        # * judges more the ball is hanging around the other player's side,
        # * has greater distance to the expected landing point of the ball,
        # * jumps more,
        # * and dives less.
        # * 0, 1, 2, 3 or 4
        # */
        self.computerBoldness = random.randint(0, 4)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x - PLAYER_HALF_LENGTH, self.y, PLAYER_LENGTH, PLAYER_LENGTH))