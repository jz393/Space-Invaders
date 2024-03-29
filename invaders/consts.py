"""
Constants for Alien Invaders

This module global constants for the game Alien Invaders. These constants need to be used 
in the model, the view, and the controller. As these are spread across multiple modules, 
we separate the constants into their own module. This allows all modules to access them.

Author: Jane Zhang (jz393)
Date: December 3, 2017
"""
import cornell
import sys

### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display 
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


### SHIP CONSTANTS ###

# the width of the ship
SHIP_WIDTH    = 44
# the height of the ship
SHIP_HEIGHT   = 44
# the distance of the (bottom of the) ship from the bottom of the screen
SHIP_BOTTOM   = 32
# The number of pixels to move the ship per update
SHIP_MOVEMENT = 5
# The number of lives a ship has
SHIP_LIVES    = 5

# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 50


### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 33
# the height of an alien
ALIEN_HEIGHT  = 33
# the horizontal separation between aliens
ALIEN_H_SEP   = 43
# the vertical separation between aliens
ALIEN_V_SEP   = 50
# the number of horizontal pixels to move an alien
ALIEN_H_WALK  = ALIEN_WIDTH // 4
# the number of vertical pixels to move an alien
ALIEN_V_WALK  = ALIEN_HEIGHT // 2
# The distance of the top alien from the top of the window
ALIEN_CEILING = 100
# the number of rows of aliens, in range 1..10
ALIEN_ROWS     = 5
# the number of aliens per row
ALIENS_IN_ROW  = 12
# the image files for the aliens (bottom to top)
ALIEN_IMAGES   = ('alien1.png','alien2.png','alien3.png')
# the number of seconds (0 < float <= 1) between alien steps
ALIEN_SPEED = 1


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 4
# the height of a laser bolt
BOLT_HEIGHT = 8
# the number of pixels to move the bolt per update
BOLT_SPEED  = 15
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5


### GAME CONSTANTS ###

# state before the game has started
STATE_INACTIVE = 0 
# state when we are initializing a new wave
STATE_NEWWAVE  = 1 
# state when the wave is activated and in play
STATE_ACTIVE   = 2 
# state when we are automatically paused between lives lost
STATE_PAUSED   = 3
# state when we restoring a destroyed ship
STATE_CONTINUE = 4
#: state when the game is complete (won or lost)
STATE_COMPLETE = 5
#: state when player manually pauses the game
STATE_PLAYER_PAUSED = 6



### USE COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF ALIENS IN A ROW"""
"""
sys.argv is a list of the command line arguments when you run Python. These arguments are 
everything after the word python. So if you start the game typing

    python invaders 3 4 0.5
    
Python puts ['breakout.py', '3', '4', '0.5'] into sys.argv. Below, we take advantage of 
this fact to change the constants ALIEN_ROWS, ALIENS_IN_ROW, and ALIEN_SPEED.
"""
try:
    rows = int(sys.argv[1])
    if rows >= 1 and rows <= 10:
        ALIEN_ROWS = rows
except:
    pass # Use original value

try:
    perrow = int(sys.argv[2])
    if perrow >= 1 and perrow <= 15:
        ALIENS_IN_ROW = perrow
except:
    pass # Use original value

try:
    speed = float(sys.argv[3])
    if speed > 0 and speed <= 3:
        ALIEN_SPEED = speed
except:
    pass # Use original value

### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY ###

#starting x coordinate of ship
SHIP_CENTER=GAME_WIDTH/2

#default message to display on start screen
STR_VAL_START=('Press S to start ' +
        '\n\nLeft/Right: Move ship ' +
        '\nSpace: Fire bolts\nP: Pause game \nX: Enable or disable sound\n\n')

#default message to display while paused from losing life
STR_VAL_PAUSED=('Aliens hit your ship ' +
        '\n\nOne life lost ' +
        '\n\nPress S to continue')

#default message to display while player paused game    
STR_VAL_PLAYER_PAUSED=('You paused the game ' +
        '\n\nPress S to continue'+
        '\n\nLeft/Right: Move ship ' +
        '\nSpace: Fire bolts\nP: Pause game \nX: Enable or disable sound\n\n')

#various scores of aliens
#Invariant: must consist of all ints, contain same length as ALIEN_IMAGES
ALIEN_SCORES=(50,40,30)

#amount we should increment (multiply) ALIEN_SPEED with each level
INCR_SPEED_LEVEL=0.75

#amount we should increment (multiply) ALIEN_SPEED with each alien hit
INCR_SPEED_ALIEN=0.98

#number of seconds elapsed before sound can be switched again
#so user pressing down X will not continuously change it
TIME_SOUND_SWITCH=0.2

#horizontal distance between text labels on active state screen
LABEL_DX_APART=100

