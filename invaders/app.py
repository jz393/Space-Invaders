"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There 
is no need for any additional classes in this module.  If you need more classes, 99% of 
the time they belong in either the wave module or the models module. If you are unsure 
about where a new class should go, post a question on Piazza.

Author: Jane Zhang (jz393)
Date: December 3, 2017

"""
import cornell
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.
    
    The primary purpose of this class is to manage the game state: which is when the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message 
                [GLabel, or None if there is no message to display]

    
    STATE SPECIFIC INVARIANTS: 
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.
    
    For a complete description of how the states work, see the specification for the
    method update.
    
    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be 
    documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _textLives: message on active screen displaying how many lives player has
                [GLabel, or None if there is no message to display]
    _originalScore: Initial score at the start of the current wave
        (zero if first wave, higher if player has accomplished more than one wave)
                [int>=0]
    _score: Total score obtained by player (increases as more aliens get hit)
                [int>=0]
    _textScore: message on active screen displaying score player has
                [GLabel, or None if there is no message to display]
    _level: the level the player is on (how much waves the player has completed)
                [int>=0]
    _textLevel: message on active screen displaying level player is on
                [GLabel]
    _sound: True if player has enabled sound effects/music, False otherwise
                [bool]
    _soundIs: string representation of sound ('off' if _sound is False, 'on' if True)
                [str]
    _soundtime: amount of seconds elapsed since user last changed sound settings
                [number (int or float) >=0]
    _textSound: message on active screen displaying whether sound is on or not
                [GLabel]
    """
    
    
    # THREE MAIN GAMEAPP METHODS
    
    def start(self):
        """
        Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state=STATE_INACTIVE
        self._originalScore=0
        self._score=0
        self._level=0
        self._sound=False
        self._soundIs='OFF'
        self._soundtime=0
        
        
    def update(self,dt):
        """
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.
        
        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these 
        does its own thing and might even needs its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the 
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).
        
        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen. 
        The application switches to this state if the state was STATE_INACTIVE in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. The 
        application switches to this state if the state was STATE_PAUSED in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_COMPLETE: The wave is over, and is either won or lost.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._updateSound(dt)
        
        if self._state==STATE_INACTIVE:
            self._updateInactive()
            
        if self._state==STATE_NEWWAVE:
            self._updateNewWave()
         
        if self._state==STATE_ACTIVE:
            self._updateActive(dt)
            
        if self._state==STATE_PLAYER_PAUSED:
            self._updatePlayerPaused()
            
        if self._state==STATE_PAUSED:
            self._updatePaused()
        
        if self._state==STATE_CONTINUE:
            self._updateContinue()
        
        if self._state==STATE_COMPLETE:
            self._updateComplete()
               
        
    def draw(self):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in 
        Wave. In order to draw them, you either need to add getters for these attributes 
        or you need to add a draw method to class Wave.  We suggest the latter.  See 
        the example subcontroller.py from class.
        """
        if self._state==STATE_NEWWAVE:
            self._wave.drawAlienWave(self.view)
            self._wave.drawShip(self.view)
            self._wave.drawLine(self.view)
        
        elif self._state==STATE_ACTIVE:
            self._wave.drawAlienWave(self.view)
            self._wave.drawLine(self.view)
            self._wave.drawBolts(self.view)
            self._wave.drawShip(self.view)
            self._textScore.draw(self.view)
            self._textLives.draw(self.view)
            self._textLevel.draw(self.view)
            self._textSound.draw(self.view)
            
        else:
            self._text.draw(self.view)
            
            
    # HELPER METHODS FOR THE STATES GO HERE
    
    def _updateSound(self, dt):
        """
        Helper method to adjust user's sound preferences
        
        Changes value of bool _sound each time user
        presses key 'X'. Maximum number of times sound
        settings can be changed is once 10 times dt
        (to prevent mistakes from continually holding down 'X')
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._soundtime>TIME_SOUND_SWITCH:
            if self.input.is_key_down('x'):
                self._soundtime=0
                if self._sound:
                    self._sound=False
                    self._soundIs='OFF'
                else:
                    self._sound=True
                    self._soundIs='ON'
        else:
            self._soundtime+=dt
    
    
    def _updateInactive(self):
        """
        Helper method for the inactive state's
        protocol for update
        """
        self._text=GLabel(text=STR_VAL_START,font_size=40,
                          font_name='Arcade',x=400,y=400)
        if self.input.is_key_down('s'):
                self._state=STATE_NEWWAVE
    
         
    def _updateNewWave(self):
        """
        Helper method for the new wave state's
        protocol for update
        """    
        self._wave=Wave()
        self._level+=1
        self._originalScore=self._score
        self._state=STATE_ACTIVE
    
        
    def _updateActive(self, dt):
        """
        Helper method for the active state's
        protocol for update
        """
        
        self._wave.moveShip(self.input)
        self._wave.moveAliens(self._level, dt, self._sound)
        self._wave.moveBolts(self.input, self._sound)
        self._wave.checkAlienCollisions(self._sound)      
        
        self._textScore=GLabel(text='Score: '
                +repr(self._score),font_size=30,
                font_name='Arcade',x=LABEL_DX_APART,
                y=GAME_HEIGHT-ALIEN_CEILING/2)

        self._textLevel=GLabel(text='Level: '
                +repr(self._level),font_size=30,
                font_name='Arcade',x=GAME_WIDTH/2-LABEL_DX_APART,
                y=GAME_HEIGHT-ALIEN_CEILING/2)
        
        self._textLives=GLabel(text='Lives: '
                +repr(self._wave.getLives()),font_size=30,
                font_name='Arcade',x=GAME_WIDTH/2+LABEL_DX_APART,
                y=GAME_HEIGHT- ALIEN_CEILING/2)        
        
        self._textSound=GLabel(text='Sound: '+self._soundIs,
                font_size=30,font_name='Arcade',x=GAME_WIDTH-LABEL_DX_APART,
                y=GAME_HEIGHT-ALIEN_CEILING/2)
        self._score=self._originalScore+self._wave.getScore()            
        self._transitionActive()
    
    
    def _transitionActive(self):
        """
        Helper method that lists all the posible transitions
        from the active state in the form of if statements      
        and the different states to switch to         
        """
        if self.input.is_key_down('p'):
                self._state=STATE_PLAYER_PAUSED
                
        elif self._wave.noMoreAliens():
            self._state=STATE_COMPLETE
                    
        elif self._wave.isShipCollision(self._sound) and self._wave.getLives()>0: 
            self._state=STATE_PAUSED
        
        elif self._wave.getLives()==0:
            self._state=STATE_COMPLETE
                    
        elif self._wave.crossedDefenseLine(self._sound):
            self._state=STATE_COMPLETE
               
            
    def _updatePaused(self):
        """
        Helper method for the paused (resulting from lost life) state's
        protocol for update
        """
        self._text=GLabel(text=STR_VAL_PAUSED,
                    font_size=40,font_name='Arcade',x=400,y=400)
            
        self._wave.clearBolts()
        if self.input.is_key_down('s'):
                self._state=STATE_CONTINUE
    
    
    def _updatePlayerPaused(self):
        """
        Helper method for the player-induced paused state's
        protocol for update
        """
        self._text=GLabel(text=STR_VAL_PLAYER_PAUSED, font_size=40,
                    font_name='Arcade',x=400,y=400)
        
        if self.input.is_key_down('s'):
                self._state=STATE_CONTINUE
           
            
    def _updateContinue(self):
        """
        Helper method for the continue state's
        protocol for update
        """
        self._wave.setNewShip()
        self._state=STATE_ACTIVE
    
    
    def _updateComplete(self):
        """
        Helper method for the completed state's
        protocol for update
        """
        
        if self._wave.noMoreAliens():
            self._text=GLabel(text='Level '+repr(self._level)+' completed'
                    +'\n\nPress S to advance to next level',font_size=40,
                          font_name='Arcade',x=400,y=400)
            if self.input.is_key_down('s'):
                self._state=STATE_NEWWAVE
                    
        elif self._wave.getLives()==0 or self._wave.crossedDefenseLine(self._sound):
            self._text=GLabel(text='You lost the game '
                              +'\n\nTotal score: '+repr(self._score),
                              font_size=50,font_name='Arcade',x=400,y=400)
                    
    