"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Author: Jane Zhang (jz393)
Date: December 3, 2017

"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _totalsteps: The total amount of alien steps alien has marched 
                [int >= 0]
        _steps: The amount of alien steps since the last bolt fired from alien
                [int >= 0]
        _score: Total score obtained by player (increases as more aliens get hit)
                [int >=0]
        _aliensGone: Total amount of aliens killed, speed depends on this
                [int >=0]
        _pew1: Sound played in game when player fires
                [Sound object]
        _pew2: Sound played in game when alien fires
                [Sound object]
        _pop2: Sound played in game when bolt collides with alien
                [Sound object]
        _blast1: Sound played in game when bolt collides with ship
                [Sound object]
        _blast2: Sound played in game when aliens cross defense line
                [Sound object]
        _MUSIC_SEQUENCE: Tuple of sound files played in looping
            sequence when aliens move [nonempty Tuple containing
                                    strings of valid sound file names]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getScore(self):
        """
        Returns score player has accummulated in current Wave
        """
        return self._score

    
    def getLives(self):
        """
        Returns how much lives player has left before game is lost
        """
        return self._lives

    
    def setNewShip(self):
        """
        Creates a new ship and sets it to self._ship
        """
        self._ship=Ship(SHIP_CENTER,SHIP_BOTTOM,SHIP_WIDTH,SHIP_HEIGHT,'ship.png')

    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS

    def __init__(self):
        """
        Initializer: creates the Wave subcontroller
        """
        self.setNewShip()
        self._aliens=self._makeAlienWave()
        self._bolts=[]
        self._dline=DefenseLine()
        self._lives=SHIP_LIVES
        self._time=0
        self._steps=0
        self._totalsteps=0
        self._score=0
        self._aliensGone=0
        #sounds
        self._pew1=Sound('pew1.wav')
        self._pew2=Sound('pew2.wav')
        self._pop2=Sound('pop2.wav')
        self._blast1=Sound('blast1.wav')
        self._blast2=Sound('blast2.wav')
        #tuple of sound files played in looping sequence when aliens move
        self._MUSIC_SEQUENCE=(Sound('A.wav'),
                    Sound('B_flat.wav'), Sound('B.wav'), Sound('C.wav'))
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS

    def moveBolts(self, input, sound):
        """
        Fires bolts from ship to user input
        if space key is pressed, fires bolts from alien wave with
        random frequency and from random alien. Plays sound
        if sound is enabled
        
        Parameter input: the keyboard input
        Precondition: input is string of valid key
        
        Parameter sound: whether user has enabled sound or not
        Precondition: sound is a bool
        """
        #for player bolts
        if input.is_key_down('spacebar') and self._numPlayerBolts()<1:
            bolt=Bolt(self._ship.getXPos(), SHIP_BOTTOM+SHIP_HEIGHT, True)
            self._bolts.append(bolt)
            if sound:
                self._pew1.play()
        
        #for alien bolts      
        self._moveAlienBolts(sound)      
        
        #for both
        for bolt in self._bolts:
            bolt.moveYPos(bolt.getVelocity())
            inBounds=bolt.getYPos()<GAME_HEIGHT and bolt.getYPos()>0
            if not inBounds:
                self._bolts.remove(bolt)

        
    def moveShip(self, input):
        """
        Moves the ship according
        to user input (left key moves ship left,
        right key moves right)
        
        Parameter input: the keyboard input
        Precondition: input is string of valid key
        """
        
        if input.is_key_down('left'):
            self._ship.moveXPos(-SHIP_MOVEMENT)
        if input.is_key_down('right'):
            self._ship.moveXPos(SHIP_MOVEMENT)
        
        
    def moveAliens(self, level, dt, sound): 
        """
        Moves the aliens every dt seconds, horizontally by ALIEN_H_WALK
        and vertically by ALIEN_V_WALK when alien wave reaches left side.
        Plays sound if sound is enabled        
        
        Aliens increase their speed as level increases
        
        Parameter level: the level the player is on, passed as a
        parameter through app class
        Precondition: level is an int > 0
        
        Parameter dt: number of seconds that have
        passed since the last animation frame
        Precondition: dt is a float > 0
        
        Parameter sound: whether user has enabled sound or not
        Precondition: sound is a bool
        """
        
        TouchingLeftSide=self._findAlienSmallestX()<=ALIEN_H_SEP 
        TouchingRightSide=self._findAlienBiggestX()+ALIEN_WIDTH>=GAME_WIDTH         
        inBounds= not TouchingLeftSide and not TouchingRightSide 
        goingRight= TouchingLeftSide or (self._isMovingRight() and inBounds)
        goingLeft= TouchingRightSide or (self._isMovingLeft() and inBounds)
        
        levelM=INCR_SPEED_LEVEL**(level-1) #level multiplier
        aliensM=INCR_SPEED_ALIEN**(self._aliensGone) #aliens multiplier
        
        if self._time>ALIEN_SPEED*levelM*aliensM:
            if sound:
                pos= self._totalsteps % len(self._MUSIC_SEQUENCE)
                self._MUSIC_SEQUENCE[pos].play()
            
            if TouchingLeftSide and self._isMovingLeft():
                self._moveAlienWaveDown()
       
            if goingRight:
                self._moveAlienWaveRight()
         
            elif goingLeft:
                self._moveAlienWaveLeft()
            
            self._totalsteps+=1

        else:
            self._time+=dt
            
            
    #UPDATE (NOT HELPER) METHODS FOR COLLISION DETECTION

    def checkAlienCollisions(self, sound):
        """
        Checks if there is a collision between any aliens
        in _aliens and a bolt fired by player, deletes the
        alien and bolt from their respective lists and changes
        index values to None if collision is detected. Plays
        sound if sound is enabled.
        
        Parameter sound: whether user has enabled sound or not
        Precondition: sound is a bool
        """
        
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if isinstance(self._aliens[row][col], Alien):
                    for bolt in self._bolts:
                        if bolt.isPlayerBolt() and self._aliens[row][col].collides(bolt):
                            self._score+=self._aliens[row][col].getScore()
                            self._aliens[row][col]=None
                            self._bolts.remove(bolt)
                            self._aliensGone+=1
                            if sound:
                                self._pop2.play()
                            

    
    def isShipCollision(self, sound):
        """
        Returns True if ship collision with alien bolt is detected
        
        Checks if there is a collision between any bolts
        in _bolts fired by alien and the ship, deletes the
        bolt from the list (and the player) and changes index values to None
        if collision is detected. PLays sound effect if sound is enabled
        
        Parameter sound: whether user has enabled sound or not
        Precondition: sound is a bool
        """
        
        for bolt in self._bolts:
            if not bolt.isPlayerBolt() and self._ship.collides(bolt):
                    if sound:
                        self._blast1.play()
                    self._ship=None
                    self._lives-=1
                    return True
        return False

    
    def clearBolts(self):
        """
        Clears the list of _bolts and makes it an empty list
        
        Called in paused state when life is lost, so that player
        can resume game without any previous bullets on screen
        """
        self._bolts=[]

    
    def crossedDefenseLine(self, sound):
        """
        Returns True if alien wave has reached the defense line,
        False otherwise
        
        Finds the lowest y coordinate alien in wave and compares it to
        the y coordinate of the defense line. Called in update method
        of controller class to determine state of game, plays sound effect
        if sound is enabled
        
        Parameter sound: whether user has enabled sound or not
        Precondition: sound is a bool
        """
        if sound and self._findAlienSmallestY()==self._dline.getYPos():
            self._blast2.play()
        
        return self._findAlienSmallestY()<=self._dline.getYPos()

    
    def noMoreAliens(self):
        """
        Returns True if all the aliens have been successfully
        fired at and the player has won the game, False otherwise
        
        Checks to see of _aliens is an empty list
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None:
                    return False
                
        return True
    
        
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    
    def drawAlienWave(self, view):
        """
        Draws the alien wave in the provided view.
        
        Parameter view: the view to draw to
        Precondition: view is a GView
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if isinstance(self._aliens[row][col],Alien):
                    self._aliens[row][col].draw(view)
          
                
    def drawShip(self, view):
        """
        Draws the alien wave in the provided view.
        
        Parameter view: the view to draw to
        Precondition: view is a GView
        """
        self._ship.draw(view)
          
                
    def drawLine(self, view):
        """
        Draws the defense line in the provided view.
        
        Parameter view: the view to draw to
        Precondition: view is a GView
        """
        self._dline.draw(view)

        
    def drawBolts(self, view):
        """
        Draws the current list of bolts (_bolts)
        in the provided view.
        
        Parameter view: the view to draw to
        Precondition: view is a GView
        """
        for bolt in self._bolts:
            bolt.draw(view)
        
        
    #OTHER HELPER METHODS I ADDED
    
    def _moveAlienWaveRight(self):
        """
        Helper method called in moveAliens to move entire wave
        of aliens right by ALIEN_H_WALK
        """
        self._steps+=1
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if isinstance(self._aliens[row][col], Alien):
                    self._aliens[row][col].setLastXPos(self._aliens[row][col].x)
                    self._aliens[row][col].moveXPos(ALIEN_H_WALK)
                    self._time=0
    
                    
    def _moveAlienWaveLeft(self):
        """
        Helper method called in moveAliens to move entire wave
        of aliens left by ALIEN_H_WALK
        """
        self._steps+=1
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if isinstance(self._aliens[row][col], Alien):
                    self._aliens[row][col].setLastXPos(self._aliens[row][col].x)
                    self._aliens[row][col].moveXPos(-ALIEN_H_WALK)
                    self._time=0

        
    def _moveAlienBolts(self, sound):
        """
        Helper method to fire alien bolts from alien waves
        with random frequency from random alien in wave
        Plays sound if sound is enabled
        
        Parameter sound: whether user has enabled sound or not
        Precondition: sound is a bool
        """
        
        numAlienSteps=random.randint(1,BOLT_RATE)
        if self._steps>numAlienSteps:
            self._steps=0
            colToFire=random.randint(0,ALIENS_IN_ROW-1)
    
            while self._isEmptyCol(colToFire):
                colToFire=random.randint(0,ALIENS_IN_ROW-1)
            
            rowToFire=self._findAlienColSmallestRow(colToFire)
            boltXPos=self._aliens[rowToFire][colToFire].getXPos()
            boltYPos=self._aliens[rowToFire][colToFire].getYPos()
            alienbolt=Bolt(boltXPos,boltYPos,False)
            self._bolts.append(alienbolt)
            if sound:
                self._pew2.play()
        
        
    def _isEmptyCol(self, x):
        """
        Returns True if _aliens has no more alien
        objects in specified column x in _aliens
        
        Determines whether column x of _aliens filled
        with None values
        
        Parameter x: _aliens column index to check
        Precondition: x is a valid int between 0 and
        ALIENS_IN_ROW - 1 
        """
        for row in range(ALIEN_ROWS):
            if self._aliens[row][x] is not None:
                return False
            
        return True
        
    
    def _numPlayerBolts(self):
        """
        Returns: number of bolts fired by the player that
        are currently on the screen
        
        Called by moveBolts as a helper to determine whether the
        player can fire another bolt
        """
        count=0
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                count+=1
    
        return count
    
    
    def _findAlienBiggestX(self):
        """
        Returns: x coordinate of alien to the most right
        
        Called in moveAliens so that we can know when to start
        moving the alien wave to the left after the alien to the
        most right hits the window's right boundary
        """
        biggestXPos=0
        count=0
        
        for col in range(ALIENS_IN_ROW,0,-1):
            for row in range(ALIEN_ROWS):
                if count==0:
                    if isinstance(self._aliens[row][col-1], Alien):
                        biggestXPos=self._aliens[row][col-1].getXPos()
                        count+=1
                            
        return biggestXPos
    
        
    def _findAlienSmallestX(self): 
        """
        Returns: x coordinate of alien to the most left
        
        Called in moveAliens so that we can know when to start
        moving the alien wave to the right after the alien to the
        most left hits the window's left boundary
        """
        smallestXPos=0
        count=0
        
        for col in range(ALIENS_IN_ROW):
            for row in range(ALIEN_ROWS):
                if count==0:
                    if isinstance(self._aliens[row][col], Alien):
                        smallestXPos=self._aliens[row][col].getXPos()
                        count+=1
                        
        return smallestXPos
    
    
    def _findAlienSmallestY(self): 
        """
        Returns: y coordinate of alien on the most bottom
        
        Useful for determining when the aliens have crossed the
        defense line.
        """
        smallestYPos=0
        count=0
        for row in range(ALIEN_ROWS,0,-1):
            if len(self._aliens[row-1])>0:
                for col in range(ALIENS_IN_ROW):
                    if count==0:
                        if isinstance(self._aliens[row-1][col], Alien):
                            smallestYPos=self._aliens[row-1][col].getYPos()
                            count+=1
        
        return smallestYPos - (SHIP_BOTTOM+SHIP_HEIGHT)
    
    
    def _findAlienColSmallestRow(self,col): 
        """
        Returns: row index value of alien on the most bottom
        in column col
        
        Useful for determining where the bullet fired from
        specificed alien col will start at
        
        Parameter col: the column of _aliens to search
        Precondition: col is a valid int between 0 and
        ALIENS_IN_ROW-1 (it is guaranteed by another helper
        within wave class that col will have at least one alien)
        """
        alien=None
        max_row=0
        
        for row in range(ALIEN_ROWS):
            if self._aliens[row][col] is not None:
                alien=self._aliens[row][col]
                max_row=row
        
        return max_row
        
    
    def _isMovingLeft(self): 
        """
        Returns True if Alien is currently moving
        left, False otherwise
        
        Evaluates motion of Alien
        
        Parameter prevXPos: the alien's previous
        x position
        Precondition: prexXPos is an int that fits within
        the bounds of the game window
        """
        #find alien that is not None
        count=0
        alien=None
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if isinstance(self._aliens[row][col], Alien):
                    if count==0:
                        alien=self._aliens[row][col]
                        break
        
        if alien.getLastXPos()>alien.getXPos(): 
            return True
        
        else:
            return False
    
    
    def _isMovingRight(self): 
        """
        Returns True if Alien is currently moving
        left, False otherwise
        
        Evaluates motion of Alien
        
        Parameter prevXPos: the alien's previous
        x position
        Precondition: prexXPos is an int that fits within
        the bounds of the game window
        """
        #find alien that is not None
        count=0
        alien=None
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if isinstance(self._aliens[row][col], Alien):
                    if count==0:
                        alien=self._aliens[row][col]
                        break
        
        if alien.getLastXPos()<alien.getXPos(): 
            return True
        
        else:
            return False
    
        
    def _moveAlienWaveDown(self):
        """
        Moves the whole alien wave down by
        ALIEN_V_WALK units, modifies each alien's
        y attribute
        
        Called as a helper by moveAliens update function
        each time the alien reaches left bound, before
        they start to move right again
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if isinstance(self._aliens[row][col], Alien):
                    self._aliens[row][col].moveYPos(-ALIEN_V_WALK)
        
        self._steps+=1
        self._time=0
    
    
    def _noMoreLives(self):
        """
        Returns True if all the player's lives have been used,
        False otherwise
        
        Checks to see of _lives is 0
        """
        return self._lives==0
    
    
    def _determineScore(self, image):
        """
        Returns corresponding score of alien
        
        Each value of ALIEN_IMAGES corresponds with a score
        in ALIEN_SCORES by index
        
        Parameter image: image of alien we are trying
        to determine score of
        Preconditon: image is a valid string image name
        found in folder contents
        """
        x=ALIEN_IMAGES.index(image)
        return ALIEN_SCORES[x]
    
    
    def _makeAlienWave(self):
        """
        Returns: wave of alien objects
        
        Creates 2D list of aliens according to specified
        constants in consts.py and returns the new list
        """
        aliens=[]
        import math
        num_images=len(ALIEN_IMAGES)
        y=GAME_HEIGHT-ALIEN_CEILING
        poscounter=0 #accumulator
        mod2counter=0 #accumulator
        
        for row in range(ALIEN_ROWS):
            alienrow=[]
            x=ALIEN_H_SEP
          
            for col in range (ALIENS_IN_ROW):
                image=ALIEN_IMAGES[mod2counter%num_images]
                alienrow.append(Alien(x,y,ALIEN_WIDTH,ALIEN_HEIGHT,
                                      image, self._determineScore(image)))
                x+=ALIEN_H_SEP
            poscounter+=1
          
            if poscounter%2==0: 
                mod2counter+=1
            aliens.append(alienrow)   
            y-=ALIEN_V_SEP
        
        return aliens
