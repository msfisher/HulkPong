# Hulk Pong game to use as instruction for teaching a Python
# workshop at Trinity Christian School summer of 2021
# Marcus Fisher
# 06/28/2021

# Import the modules needed
import turtle
import random
import math

gWidth     = 600  # game screen width
gHeight    = 600  # game screen height
#playerSize = 5    # the width of the player
playGame   = True # boolean to control game loop

gameScreen = turtle.Screen()  # create game screen to draw on
gameScreen.bgcolor("black")  # set background color to black
gameScreen.title("Hulk Pong with Loki's Head")  # set title of window
gameScreen.setup(width=gWidth, height=gHeight)
gameScreen.bgpic("hulkBackground.gif")
gameScreen.tracer(0)            # shut off the screen updates

# Register the shapes so that they can be used
gameScreen.register_shape("loki.gif")
gameScreen.register_shape("playerOneGif.gif")
gameScreen.register_shape("playerTwoGif.gif")

# Create the two players
playerOne = turtle.Turtle()  # create the player's character
playerOne.speed(0)  # how fast it is drawn, 0 is the fastest
playerOne.shape("playerOneGif.gif")  # player shape
playerOne.penup()  # don't draw on screen yet
playerOne.goto(250, 0)  # starting position

playerTwo = turtle.Turtle()  # create the seconds player
playerTwo.speed(0)  # how fast it is drawn, 0 is the fastest
playerTwo.shape("playerTwoGif.gif")  # player shape
playerTwo.penup()  # don't draw on screen yet
playerTwo.goto(-250, 0)  # starting position

# Create loki to be the ball batted back and forth
loki = turtle.Turtle()
loki.shape("loki.gif")
loki.speed(0)
loki.penup()
lokiSpeedX  = 0.08       # how fast loki's head moves in X direction
lokiSpeedY  = 0.08       # how fast Loki's head moves in Y direction
lokiInit    = False     # used to determine if we need to reinitialize the ball
playerSpeed = 15         # how fast player moves when user presses a key

# Setup the scoring text to be displayed on screen
scoreOne = turtle.Turtle()
scoreOne.speed(0)
scoreOne.color("white")
scoreOne.penup()
scoreOne.setposition(220, 270)
playerOneScore = 0
scoreOneString = "Score: {}".format(playerOneScore)
scoreOne.write(scoreOneString, False, align="left", font=("Arial", 10, "normal"))
scoreOne.hideturtle()
scoreTwo = turtle.Turtle()
scoreTwo.speed(0)
scoreTwo.color("white")
scoreTwo.penup()
scoreTwo.setposition(-270, 270)
playerTwoScore = 0
scoreTwoString = "Score: {}".format(playerTwoScore)
scoreTwo.write(scoreTwoString, False, align="left", font=("Arial", 10, "normal"))
scoreTwo.hideturtle()

# functions to be called when the player presses a key
def move1Up():
    y = playerOne.ycor()  # get y-coord of the player

    # keep the player from moving off screen
    if ((y + playerSpeed) < (gHeight / 2)):
        y = y + playerSpeed  # Update the position of the player
        playerOne.sety(y)  # move the player


def move1Down():
    y = playerOne.ycor()  # get y-coord of the player

    # keep player from moving off screen
    if ((y - playerSpeed) > -(gHeight / 2)):
        y = y - playerSpeed  # Update the position of the player
        playerOne.sety(y)  # Move the player


def move2Up():
    y = playerTwo.ycor()  # get y-coord of the player

    # keep the player from moving off screen
    if ((y + playerSpeed) < (gHeight / 2)):
        y = y + playerSpeed  # Update the position of the player
        playerTwo.sety(y)  # move the player


def move2Down():
    y = playerTwo.ycor()  # get y-coord of the player

    # keep player from moving off screen
    if ((y - playerSpeed) > -(gHeight / 2)):
        y = y - playerSpeed  # Update the position of the player
        playerTwo.sety(y)  # Move the player

# Initialize loki
def initLoki():
    global lokiSpeedX   # make it global so that we can change the value
    global lokiInit     # set this to false since we are initializing now
    global loki

    # randomly place loki on the game screen
    loki.setx(random.randint(-100, 100))
    loki.sety(random.randint(-100, 100))

    # randomly determine which direction to start in
    lokiDirection = random.randint(1,2)
    if(lokiDirection == 1):
        lokiSpeedX = lokiSpeedX * -1

    # set the flag so that we don't run initialize again
    lokiInit = True

def moveLoki():
    global lokiSpeedY, lokiSpeedX
    global playerOneScore, playerTwoScore
    global scoreTwoString, scoreOneString
    global playGame

    restartLoki = False

    x = loki.xcor()
    y = loki.ycor()

    # Handle y-coordinate - Bounce loki off top and bottom walls
    y = y + lokiSpeedY
    if(y>300):
        lokiSpeedY = lokiSpeedY * -1
    if(y<-300):
        lokiSpeedY = lokiSpeedY * -1
    loki.sety(y)

    # Handle Loki hitting a paddle (Hulk) and have Loki bounce off paddle
    # determine if there is a collision using the distance formula
    # calculate the distance between two points, if the distance is
    # very small then they have basically collided
    # formula is distance = sqrt( (x2-x1)^2 + (y2-y1)^2 )
    # Turtle module has a distance function as well .. but lets learn some math
    first = math.pow((loki.xcor() - playerOne.xcor()),2)
    second = math.pow((loki.ycor()-playerOne.ycor()),2)
    result = math.sqrt(first+second)
    if(result <= 30):
        lokiSpeedX = lokiSpeedX * -1

    if(playerTwo.distance(loki.xcor(), loki.ycor()) <= 30):
        lokiSpeedX = lokiSpeedX * -1

    # Handle x-coordinate - if Loki goes of the edges then the opposite
    # player gets a point, start Loki again and let them keep playing
    x = x + lokiSpeedX
    if(x>290):
        playerTwoScore = playerTwoScore + 10
        scoreTwoString = "Score: {}".format(playerTwoScore)
        scoreTwo.clear()
        scoreTwo.write(scoreTwoString, False, align="left", font=("Arial", 10, "normal"))
        restartLoki = True
    if(x<-290):
        playerOneScore = playerOneScore + 10
        scoreOneString = "Score: {}".format(playerOneScore)
        scoreOne.clear()
        scoreOne.write(scoreOneString, False, align="left", font=("Arial", 10, "normal"))
        restartLoki = True

    # End the game when a player scores 50 points
    if(playerOneScore >= 50 or playerTwoScore >= 50):
        playGame = False
        scoreOne.clear()
        scoreTwo.clear()
        scoreOneString = "GaMe OvEr"
        scoreOne.setposition(0, 0)
        scoreOne.write(scoreOneString, False, align="left", font=("Arial", 24, "normal"))

    # determine to either reset Loki because it has gone off the screen
    # or it hasn't so just move Loki
    if(restartLoki == True):
        initLoki()
    else:
        loki.setx(x)


# Listen for key events and bind the keys to the functions
gameScreen.listen()
gameScreen.onkeypress(move1Up, "Up")
gameScreen.onkeypress(move1Down, "Down")
gameScreen.onkeypress(move2Up, "w")
gameScreen.onkeypress(move2Down, "s")

# Main Game Loop
while playGame:
    gameScreen.update()     # update the screen
    if(lokiInit == False):
        initLoki()
    # move Loki
    moveLoki()

# exit the game when the user clicks mouse
gameScreen.exitonclick()