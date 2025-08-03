from .constants import *
import pygame
from .sound import Sound


class Ball:
    def __init__(self, isPlayer2Serve: bool ):
        self.isPlayer2Serve = isPlayer2Serve
        self.expectedLandingPointX = 0
        self.rotation = 0 # ball rotation frame number selector (0..5)
        self.fineRotation = 0
        self.punchEffectX = 0 
        self.punchEffectY = 0
        self.previousX = 0
        self.previousPreviousX = 0
        self.previousY = 0
        self.previousPreviousY = 0

        self.x = 0
        self.y = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.punchEffectRadius = 0
        self.isPowerHit = False
        self.sound = Sound()

    def initializeForNewRound(self, isPlayer2Serve: bool):
        self.x = 56
        if isPlayer2Serve:
            self.x = GROUND_WIDTH - 56
        
        self.y = 0
        self.xVelocity = 0
        self.yVelocity = 1
        self.punchEffectRadius = 0
        self.isPowerHit = False

    def draw(self, screen):
        # draw the ball as a circle
        color = WHITE
        if self.isPowerHit:
            color = RED
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), BALL_RADIUS)