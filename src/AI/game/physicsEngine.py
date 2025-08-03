from .player import Player
from .ball import Ball
import math
from .constants import *
import random

def physicsEngine(player1, player2, ball, userInputArray):
    isBallTouchingGround = processCollisionBetweenBallAndWorldAndSetBallPosition(ball)

    for i in range(2):
        if i==0:
            player = player1
            theOtherPlayer = player2
        else:
            player = player2
            theOtherPlayer = player1

        calculateExpectedLandingPointXFor(ball)

        processPlayerMovementAndSetPlayerPosition(
            player,
            userInputArray[i],
            theOtherPlayer,
            ball
        )
    
    for i in range(2):
        if i==0:
            player = player1
        else:
            player = player2

        isHappened = isCollisionBetweenBallAndPlayerHappened(
            ball,
            player.x,
            player.y
        )
        if isHappened:
            if player.isCollisionWithBallHappened == False:
                processCollisionBetweenBallAndPlayer(
                    ball,
                    player.x,
                    userInputArray[i],
                    player.state
                )
                player.isCollisionWithBallHappened = True
        else:
            player.isCollisionWithBallHappened = False

    return isBallTouchingGround


def isCollisionBetweenBallAndPlayerHappened(ball, playerX, playerY):
    diff = ball.x - playerX
    if abs(diff) <= PLAYER_HALF_LENGTH:
        diff = ball.y - playerY
        if abs(diff) <= PLAYER_HALF_LENGTH:
            return True
    return False



"""
Processes the collision between the ball and the world (ground) and sets the ball's position accordingly.
Returns True if the ball is touching the ground, otherwise returns False."""
def processCollisionBetweenBallAndWorldAndSetBallPosition(ball):
    ball.previousPreviousX = ball.previousX
    ball.previousPreviousY = ball.previousY
    ball.previousX = ball.x
    ball.previousY = ball.y

    futureFineRotation = ball.fineRotation + ((int(ball.xVelocity) // 2) | 0)

    # // If futureFineRotation === 50, it skips next if statement finely.
    # // Then ball.fineRotation = 50, and then ball.rotation = 5 (which designates hyper ball sprite!).
    # // In this way, hyper ball glitch occur!
    # // If this happen at the end of round,
    # // since ball.xVelocity is 0-initialized at each start of round,
    # // hyper ball sprite is rendered continuously until a collision happens.
    if futureFineRotation < 0:
        futureFineRotation += 50
    elif futureFineRotation > 50:
        futureFineRotation -= 50

    ball.fineRotation = futureFineRotation
    ball.rotation = futureFineRotation // 10 | 0

    futureBallX = ball.x + ball.xVelocity
    #     /*
    # If the center of ball would get out of left world bound or right world bound, bounce back.

    # In this if statement, when considering left-right symmetry,
    # "futureBallX > GROUND_WIDTH" should be changed to "futureBallX > (GROUND_WIDTH - BALL_RADIUS)",
    # or "futureBallX < BALL_RADIUS" should be changed to "futureBallX < 0".
    # Maybe the former one is more proper when seeing Pikachu player's x-direction boundary.
    # Is this a mistake of the author of the original game?
    # Or, was it set to this value to resolve infinite loop problem? (See comments on the constant INFINITE_LOOP_LIMIT.)
    # If apply (futureBallX > (GROUND_WIDTH - BALL_RADIUS)), and if the maximum number of loop is not limited,
    # it is observed that infinite loop in the function expectedLandingPointXWhenPowerHit does not terminate.
    # */
    if futureBallX < BALL_RADIUS or futureBallX > GROUND_WIDTH:
        ball.xVelocity = -ball.xVelocity

    futureBallY = ball.y + ball.yVelocity
    # // if the center of ball would get out of upper world bound
    if futureBallY < 0:
        ball.yVelocity = 1

    # if ball touches the net
    if abs(ball.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and ball.y > NET_PILLAR_TOP_TOP_Y_COORD:
        if ball.y <= NET_PILLAR_TOP_BOTTOM_Y_COORD:
            if ball.yVelocity > 0:
                ball.yVelocity = -ball.yVelocity
        else:
            if ball.x < GROUND_HALF_WIDTH:
                ball.xVelocity = -abs(ball.xVelocity)
            else:
                ball.xVelocity = abs(ball.xVelocity)

    futureBallY = ball.y + ball.yVelocity

    # if ball would touch ground
    if futureBallY > BALL_TOUCHING_GROUND_Y_COORD:
        # ball.sound.ballTouchesGround = True

        ball.yVelocity = -ball.yVelocity
        ball.punchEffectX = ball.x
        ball.y = BALL_TOUCHING_GROUND_Y_COORD
        ball.punchEffectRadius = BALL_RADIUS
        ball.punchEffectY = BALL_TOUCHING_GROUND_Y_COORD + BALL_RADIUS
        return True
    ball.y = futureBallY
    ball.x = ball.x + ball.xVelocity
    ball.yVelocity += 1

    return False


def calculateExpectedLandingPointXFor(ball):
    copyBall_x = ball.x
    copyBall_y = ball.y
    copyBall_xVelocity = ball.xVelocity
    copyBall_yVelocity = ball.yVelocity
    loopCounter = 0
    while True:
        loopCounter += 1

        futureCopyBallX = copyBall_xVelocity + copyBall_x
        if futureCopyBallX < BALL_RADIUS or futureCopyBallX > GROUND_WIDTH:
            copyBall_xVelocity = -copyBall_xVelocity
        if copyBall_y + copyBall_yVelocity < 0:
            copyBall_yVelocity = 1

        if abs(copyBall_x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and copyBall_y > NET_PILLAR_TOP_TOP_Y_COORD:
            if copyBall_y < NET_PILLAR_TOP_BOTTOM_Y_COORD:
                if copyBall_yVelocity > 0:
                    copyBall_yVelocity = -copyBall_yVelocity
            else:
                if copyBall_x < GROUND_HALF_WIDTH:
                    copyBall_xVelocity = -abs(copyBall_xVelocity)
                else:
                    copyBall_xVelocity = abs(copyBall_xVelocity)

        copyBall_y = copyBall_y + copyBall_yVelocity
        if copyBall_y > BALL_TOUCHING_GROUND_Y_COORD or loopCounter > INFINITE_LOOP_LIMIT:
            break
        copyBall_x = copyBall_x + copyBall_xVelocity
        copyBall_yVelocity += 1
    ball.expectedLandingPointX = copyBall_x



def processPlayerMovementAndSetPlayerPosition(player, userInput, theOtherPlayer, ball):
    if player.isComputer:
        
        letComputerDecideUserInput(player, ball, theOtherPlayer, userInput)

    # Se il player è sdraiato, non si muove
    if player.state == 4:
        player.lyingDownDurationLeft -= 1
        if player.lyingDownDurationLeft < -1:
            player.state = 0
        return

    # Movimento sull'asse X
    playerVelocityX = 0
    if player.state < 5:
        if player.state < 3:
            playerVelocityX = userInput.xDirection * 6
        elif player.state == 3:  # diving
            playerVelocityX = player.divingDirection * 8

    futurePlayerX = player.x + playerVelocityX
    player.x = futurePlayerX

    # Bordi del mondo per X
    if not player.isPlayer2:
        if futurePlayerX < PLAYER_HALF_LENGTH:
            player.x = PLAYER_HALF_LENGTH
        elif futurePlayerX > GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH:
            player.x = GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH
    else:
        if futurePlayerX < GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH:
            player.x = GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH
        elif futurePlayerX > GROUND_WIDTH - PLAYER_HALF_LENGTH:
            player.x = GROUND_WIDTH - PLAYER_HALF_LENGTH

    # Salto
    if (
        player.state < 3 and
        userInput.yDirection == -1 and
        player.y == PLAYER_TOUCHING_GROUND_Y_COORD
    ):
        player.yVelocity = -16
        player.state = 1
        player.frameNumber = 0
        player.sound.chu = True

    # Gravità e atterraggio
    futurePlayerY = player.y + player.yVelocity
    player.y = futurePlayerY

    if futurePlayerY < PLAYER_TOUCHING_GROUND_Y_COORD:
        player.yVelocity += 1
    elif futurePlayerY > PLAYER_TOUCHING_GROUND_Y_COORD:
        player.yVelocity = 0
        player.y = PLAYER_TOUCHING_GROUND_Y_COORD
        player.frameNumber = 0
        if player.state == 3:  # diving
            player.state = 4
            player.lyingDownDurationLeft = 3
        else:
            player.state = 0

    # Power hit o tuffo
    if userInput.powerHit == 1:
        if player.state == 1:  # in salto
            player.delayBeforeNextFrame = 5
            player.frameNumber = 0
            player.state = 2
            player.sound.pika = True
        elif player.state == 0 and userInput.xDirection != 0:
            player.state = 3
            player.frameNumber = 0
            player.divingDirection = userInput.xDirection
            player.yVelocity = -5
            player.sound.chu = True

    # Aggiornamento frame
    if player.state == 1:
        player.frameNumber = (player.frameNumber + 1) % 3
    elif player.state == 2:
        if player.delayBeforeNextFrame < 1:
            player.frameNumber += 1
            if player.frameNumber > 4:
                player.frameNumber = 0
                player.state = 1
        else:
            player.delayBeforeNextFrame -= 1
    elif player.state == 0:
        player.delayBeforeNextFrame += 1
        if player.delayBeforeNextFrame > 3:
            player.delayBeforeNextFrame = 0
            futureFrame = player.frameNumber + player.normalStatusArmSwingDirection
            if futureFrame < 0 or futureFrame > 4:
                player.normalStatusArmSwingDirection *= -1
            player.frameNumber += player.normalStatusArmSwingDirection

    # Stato finale partita
    if player.gameEnded:
        if player.state == 0:
            if player.isWinner:
                player.state = 5
                player.sound.pipikachu = True
            else:
                player.state = 6
            player.delayBeforeNextFrame = 0
            player.frameNumber = 0

        processGameEndFrameFor(player)




def processCollisionBetweenBallAndPlayer(ball, playerX, userInput, playerState):
    # Determina la nuova xVelocity in base alla distanza tra player e palla
    if ball.x < playerX:
        ball.xVelocity = - (abs(ball.x - playerX) // 3)
    elif ball.x > playerX:
        ball.xVelocity = abs(ball.x - playerX) // 3

    # Se xVelocity è 0, scegli -1, 0 o 1 casualmente
    if ball.xVelocity == 0:
        ball.xVelocity = random.randint(-1, 1)

    ballAbsYVelocity = abs(ball.yVelocity)
    ball.yVelocity = -ballAbsYVelocity

    if ballAbsYVelocity < 15:
        ball.yVelocity = -15

    # Se il giocatore sta effettuando un power hit (stato 2)
    if playerState == 2:
        if ball.x < GROUND_HALF_WIDTH:
            ball.xVelocity = (abs(userInput.xDirection) + 1) * 10
        else:
            ball.xVelocity = -(abs(userInput.xDirection) + 1) * 10

        ball.punchEffectX = ball.x
        ball.punchEffectY = ball.y

        ball.yVelocity = abs(ball.yVelocity) * userInput.yDirection * 2
        ball.punchEffectRadius = BALL_RADIUS

        ball.sound.powerHit = True
        ball.isPowerHit = True
    else:
        ball.isPowerHit = False

    calculateExpectedLandingPointXFor(ball)


def letComputerDecideUserInput(player, ball, theOtherPlayer, userInput):
    userInput.xDirection = 0
    userInput.yDirection = 0
    userInput.powerHit = 0

    virtualExpectedLandingPointX = ball.expectedLandingPointX

    if (
        abs(ball.x - player.x) > 100 and
        abs(ball.xVelocity) < player.computerBoldness + 5
    ):
        leftBoundary = int(player.isPlayer2) * GROUND_HALF_WIDTH
        rightEdge = int(player.isPlayer2) * GROUND_WIDTH + GROUND_HALF_WIDTH
        if (
            (ball.expectedLandingPointX <= leftBoundary or
             ball.expectedLandingPointX >= rightEdge)
            and player.computerWhereToStandBy == 0
        ):
            # Rimani al centro della propria metà campo
            virtualExpectedLandingPointX = leftBoundary + (GROUND_HALF_WIDTH // 2)

    if abs(virtualExpectedLandingPointX - player.x) > player.computerBoldness + 8:
        userInput.xDirection = 1 if player.x < virtualExpectedLandingPointX else -1
    elif random.randint(0, 19) == 0:
        player.computerWhereToStandBy = random.randint(0, 1)

    if player.state == 0:
        if (
            abs(ball.xVelocity) < player.computerBoldness + 3 and
            abs(ball.x - player.x) < PLAYER_HALF_LENGTH and
            -36 < ball.y < 10 * player.computerBoldness + 84 and
            ball.yVelocity > 0
        ):
            userInput.yDirection = -1

        leftBoundary = int(player.isPlayer2) * GROUND_HALF_WIDTH
        rightBoundary = (int(player.isPlayer2) + 1) * GROUND_HALF_WIDTH

        if (
            leftBoundary < ball.expectedLandingPointX < rightBoundary and
            abs(ball.x - player.x) > player.computerBoldness * 5 + PLAYER_LENGTH and
            leftBoundary < ball.x < rightBoundary and
            ball.y > 174
        ):
            userInput.powerHit = 1
            userInput.xDirection = 1 if player.x < ball.x else -1

    elif player.state in [1, 2]:
        if abs(ball.x - player.x) > 8:
            userInput.xDirection = 1 if player.x < ball.x else -1

        if abs(ball.x - player.x) < 48 and abs(ball.y - player.y) < 48:
            willInputPowerHit = decideWhetherInputPowerHit(
                player,
                ball,
                theOtherPlayer,
                userInput
            )
            if willInputPowerHit:
                userInput.powerHit = 1
                if (
                    abs(theOtherPlayer.x - player.x) < 80 and
                    userInput.yDirection != -1
                ):
                    userInput.yDirection = -1


def processGameEndFrameFor(player):
    if player.gameEnded and player.frameNumber < 4:
        player.delayBeforeNextFrame += 1
        if player.delayBeforeNextFrame > 4:
            player.delayBeforeNextFrame = 0
            player.frameNumber += 1

def decideWhetherInputPowerHit(player, ball, theOtherPlayer, userInput):
    if random.randint(0, 1) == 0:
        for x_direction in range(1, -2, -1):  # 1, 0
            for y_direction in range(-1, 2):  # -1, 0, 1
                expected_x = expectedLandingPointXWhenPowerHit(x_direction, y_direction, ball)
                player_side = int(player.isPlayer2)
                if (
                    expected_x <= player_side * GROUND_HALF_WIDTH or
                    expected_x >= player_side * GROUND_WIDTH + GROUND_HALF_WIDTH
                ) and abs(expected_x - theOtherPlayer.x) > PLAYER_LENGTH:
                    userInput.xDirection = x_direction
                    userInput.yDirection = y_direction
                    return True
    else:
        for x_direction in range(1, -2, -1):  # 1, 0
            for y_direction in range(1, -2, -1):  # 1, 0, -1
                expected_x = expectedLandingPointXWhenPowerHit(x_direction, y_direction, ball)
                player_side = int(player.isPlayer2)
                if (
                    expected_x <= player_side * GROUND_HALF_WIDTH or
                    expected_x >= player_side * GROUND_WIDTH + GROUND_HALF_WIDTH
                ) and abs(expected_x - theOtherPlayer.x) > PLAYER_LENGTH:
                    userInput.xDirection = x_direction
                    userInput.yDirection = y_direction
                    return True
    return False


def expectedLandingPointXWhenPowerHit(userInputXDirection, userInputYDirection, ball):
    copyBall = {
        "x": ball.x,
        "y": ball.y,
        "xVelocity": ball.xVelocity,
        "yVelocity": ball.yVelocity,
    }

    if copyBall["x"] < GROUND_HALF_WIDTH:
        copyBall["xVelocity"] = (abs(userInputXDirection) + 1) * 10
    else:
        copyBall["xVelocity"] = -(abs(userInputXDirection) + 1) * 10

    copyBall["yVelocity"] = abs(copyBall["yVelocity"]) * userInputYDirection * 2

    loopCounter = 0
    while True:
        loopCounter += 1

        futureCopyBallX = copyBall["x"] + copyBall["xVelocity"]
        if futureCopyBallX < BALL_RADIUS or futureCopyBallX > GROUND_WIDTH:
            copyBall["xVelocity"] = -copyBall["xVelocity"]

        if copyBall["y"] + copyBall["yVelocity"] < 0:
            copyBall["yVelocity"] = 1

        if (
            abs(copyBall["x"] - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH
            and copyBall["y"] > NET_PILLAR_TOP_TOP_Y_COORD
        ):
            if copyBall["yVelocity"] > 0:
                copyBall["yVelocity"] = -copyBall["yVelocity"]

        copyBall["y"] += copyBall["yVelocity"]

        if (
            copyBall["y"] > BALL_TOUCHING_GROUND_Y_COORD
            or loopCounter >= INFINITE_LOOP_LIMIT
        ):
            return copyBall["x"]

        copyBall["x"] += copyBall["xVelocity"]
        copyBall["yVelocity"] += 1
