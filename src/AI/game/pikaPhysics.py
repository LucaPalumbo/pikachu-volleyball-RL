from .player import Player
from .ball import Ball
from .physicsEngine import physicsEngine

class PickaPhysics:
    def __init__(self, isPlayer1Computer, isPlayer2Computer):
        self.player1 = Player(isPlayer2=False, isComputer=isPlayer1Computer)
        self.player2 = Player(isPlayer2=True,  isComputer=isPlayer2Computer)
        self.ball = Ball(isPlayer2Serve = False)

    def runEngineForNextFrame(self, userInputArray):
        isBallTouchingGround = physicsEngine(
            self.player1, 
            self.player2,
            self.ball,
            userInputArray
        )

        # print("Player 1:", self.player1.x, self.player1.y, "State:", self.player1.state)
        # print("Player 2:", self.player2.x, self.player2.y, "State:", self.player2.state)
        # print("Ball:", self.ball.x, self.ball.y, "Velocity:", self.ball.xVelocity, self.ball.yVelocity)


        return isBallTouchingGround