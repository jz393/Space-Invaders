"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

Author: Jane Zhang (jz393)
Date: December 3, 2017
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getXPos(self):
        """
        Returns attribute x of Ship
        """
        return self.x
    
    
    def getYPos(self):
        """
        Returns attribute y of Ship
        """
        return self.y
    
    
    # INITIALIZER TO CREATE A NEW SHIP
    
    def __init__(self,x1,y1,width1,height1,source1):
        """
        Initializer: creates a new ship
        
        Parameter x1: The ship's x coordinate
        Precondition: x1 is an int > 0
        
        Parameter y1: The ship's y coordinate
        Precondition: y1 is an int > 0
        
        Parameter width1: The window width
        Precondition: width1 is a float > 0
        
        Parameter height1: The window height
        Precondition: height1 is a float > 0.
        
        Parameter source1: The ship's photo file name
        Precondition: source1 is a string
            e.g. 'ship.png'
        
        """
        super().__init__(x=x1,y=y1,width=width1,height=height1,source=source1)
    
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    
    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the alien and
        collides with this ship
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        
        boolean=False
        if bolt.isPlayerBolt():
            return boolean
        
        #top left
        elif self.contains((bolt.getXPos()-(BOLT_WIDTH/2),
                         bolt.getYPos()+(BOLT_HEIGHT/2))): 
            boolean=True
        #top right
        elif self.contains((bolt.getXPos()+(BOLT_WIDTH/2),
                           bolt.getYPos()+(BOLT_HEIGHT/2))): 
            boolean=True
        #bottom left
        elif self.contains((bolt.getXPos()-(BOLT_WIDTH/2),
                           bolt.getYPos()-(BOLT_HEIGHT/2))): 
            boolean=True
        #bottom right
        elif self.contains((bolt.getXPos()+(BOLT_WIDTH/2),
                           bolt.getYPos()-(BOLT_HEIGHT/2))): 
            boolean=True
        
        return boolean
    
    
    def moveXPos(self, dx):
        """
        Moves x position of the ship dx positions to the left
        if dx is negative, to the right if dx is positive,
        called in moveShip function in wave class 
        
        Parameter dx: how much the x value is to shift
        Precondition: dx is an int 
        """
        newval=max(0.5*SHIP_WIDTH, self.x+dx)
        newval=min(newval, GAME_WIDTH-0.5*SHIP_WIDTH)
        self.x=newval
        

class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _lastXPos: the alien's X position in the previous frame [0<int<GAME_WIDTH]
    _score: the score killing the alien will bring [int>0]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getScore(self):
        """
        Returns score alien is worth
        """
        return self._score
    
    
    def getXPos(self):
        """
        Returns attribute x of alien
        """
        return self.x
    
    
    def getYPos(self):
        """
        Returns attribute y of alien
        """
        return self.y
    
    
    def setLastXPos(self, x):
        """
        Sets _lastXPos to x
        
        This function saves the alien's previous x position
        into an attribute
        
        Parameter x: the alien's last x position
        Precondition: x is an int in the bounds of
        game window
        """
        self._lastXPos=x
    
    
    def getLastXPos(self):
        """
        Returns attribute _lastXPos
        """
        return self._lastXPos
    
    
    # INITIALIZER TO CREATE AN ALIEN
    
    def __init__(self,x1,y1,width1,height1,source1, score):
        """
        Initializer: creates a new alien
        
        Parameter x1: The alien's x coordinate
        Precondition: x1 is an int > 0
        
        Parameter y1: The alien's y coordinate
        Precondition: y1 is an int > 0
        
        Parameter width1: The window width
        Precondition: width1 is a float > 0
        
        Parameter height1: The window height
        Precondition: height1 is a float > 0.
        
        Parameter source1: The alien's photo file name
        Precondition: source1 is a string
            e.g. 'alien1.png'
        
        """
        super().__init__(x=x1,y=y1,width=width1,height=height1,source=source1)
        self.setLastXPos(x1)
        self._score=score
    
        
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    
    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the player and
        collides with this alien
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        
        boolean=False
        
        if not bolt.isPlayerBolt():
            return boolean
        
        #top left
        if self.contains((bolt.getXPos()-(BOLT_WIDTH/2),
                         bolt.getYPos()+(BOLT_HEIGHT/2))): 
            boolean=True
        #top right
        elif self.contains((bolt.getXPos()+(BOLT_WIDTH/2),
                           bolt.getYPos()+(BOLT_HEIGHT/2))): 
            boolean=True
        #bottom left
        elif self.contains((bolt.getXPos()-(BOLT_WIDTH/2),
                           bolt.getYPos()-(BOLT_HEIGHT/2))): 
            boolean=True
        #bottom right
        elif self.contains((bolt.getXPos()+(BOLT_WIDTH/2),
                           bolt.getYPos()-(BOLT_HEIGHT/2))): 
            boolean=True
        
        return boolean
    
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    
    def moveXPos(self, dx):
        """
        Moves position of the alien dx positions to the left
        if dx is negative, to the right if dx is positive,
        called in moveAlien function in wave class 
        
        Parameter dx: how much the x value is to shift
        Precondition: dx is an int 
        """
        self.x=self.x+dx
    
        
    def moveYPos(self, dy):
        """
        Moves position of the alien dy positions to the left
        if dx is negative, to the right if dx is positive,
        called in moveAlien function in wave class 
        
        Parameter dy: how much the y value is to shift
        Precondition: dy is an int 
        """
        self.y=self.y+dy


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
        _isPlayerBolt: boolean value, True if originally came from ship,
                        False if came from alien
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getVelocity(self):
        """
        Returns _velocity attribute of bolt
        """
        return self._velocity

    
    def getXPos(self):
        """
        Returns attribute x of bolt
        """
        return self.x

    
    def getYPos(self):
        """
        Returns attribute y of bolt
        """
        return self.y

    
    def isPlayerBolt(self):
        """
        Getter method that returns attribute
        _isPlayerBolt
        """
        return self._isPlayerBolt

    
    # INITIALIZER TO SET THE VELOCITY

    def __init__(self, x, y, isPlayerBolt):
        """
        Initializer: creates a new Bolt to be fired at the aliens
        
        Parameter x: the starting x coordinate of the bolt
        Precondition: x is an number within the range of GAME_WIDTH
        
        Parameter y: the starting y coordinate of the bolt
        Precondition: y is an number within the range of GAME_HEIGHT
       
        Parameter isPlayerBolt: True if bolt originally
        came from ship, False if came from alien
        Precondition: isPlayerBolt is a bool
        """
        self._isPlayerBolt=isPlayerBolt
        
        if isPlayerBolt:
            self._velocity=BOLT_SPEED
        else:
            self._velocity=-BOLT_SPEED
        
        super().__init__(x=x,y=y,
                         width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor='blue')

    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

    def moveYPos(self, dy):
        """
        Moves position of the bolt dy positions to the left
        if dx is negative, to the right if dx is positive,
        called as helper in moveBolts function in wave class 
        
        Parameter dy: how much the y value is to shift
        Precondition: dy is an int 
        """
        self.y=self.y+dy


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE

class DefenseLine(GPath):
    """
    A class representing the ship's Defense Line.
    
    As quoted by the CS 1110 website, "The defense line is the line above
    the ship that it is defending from the aliens. It is DEFENSE_LINE pixels
    above the bottom of the window. You should create and draw this line.
    A line is represented by a GPath object."
    """
    
    def getYPos(self):
        """
        Returns attribute y of DefenseLine
        """
        return self.y

    
    def __init__(self):
        """
        Initializer: creates a new DefenseLine object
        """
        super().__init__(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE]
                        , y=DEFENSE_LINE, linecolor='black', linewidth=1)
        
    