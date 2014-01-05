'''
Author: Shirley Du

Date: May. 30/11

Description: This module has 11 classes: Button, Mouse, Player, Gold, 
StillImage, ScoreKeeper, MovingSprites, SpecialGold, Label, TextBubble, and
Background, which defines all the necessary sprites for the Crazy Frogger game.
'''

import pygame, random
pygame.init()
screen = pygame.display.set_mode((640,480))

class Button(pygame.sprite.Sprite):
    '''This class defines the buttons on the menu window'''
    def __init__(self, message, x_y_center):
        '''This initializer takes a message and a x_y_center tuple as 
        parameters, initializes the font, text, center, color, image, 
        and rect attributes'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font("./fonts/RUSTICK.ttf", 30)
        self.__text = message
        self.__color = (255,255,255)
        self.image = self.__font.render(self.__text, 1, self.__color)
        self.rect = self.image.get_rect()
        self.rect.center = x_y_center
        
    def change_color(self):
        '''This method changes the color of the text'''
        self.__color = (200,125,150)
        
    def change_color_back(self):
        '''This method changes the color of the text back to normal'''
        self.__color = (255,255,255)
        
    def update(self):
        '''This method will be called automatically to display the buttons
        on the menu'''
        self.image = self.__font.render(self.__text, 1, self.__color)
        
class Mouse(pygame.sprite.Sprite):
    '''This class defines the mouse sprite for our menu'''
    def __init__(self):
        '''This initializer initializes the image and rect of our mouse 
        sprite'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./images/mouse pointer.gif").convert()
        self.rect = self.image.get_rect()
        
    def update(self):
        '''This method will be called automatically to display the mouse 
        pointer at different positions as the mouse moves around the screen'''
        self.rect.center = pygame.mouse.get_pos()

class Player(pygame.sprite.Sprite):
    '''This class defines the main sprite for our player'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a paramter. 
        It loads different motions of the character and positions
        the character on the midbotom of the screen.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Loading the walking-motion pictures for the character
        self.__walking_left = [pygame.image.load("./images/left1.png"), 
                               pygame.image.load("./images/left2.png"), 
                               pygame.image.load("./images/left3.png"), 
                               pygame.image.load("./images/left4.png")]
        self.__walking_right = [pygame.image.load("./images/right1.png"), 
                                pygame.image.load("./images/right2.png"), 
                                pygame.image.load("./images/right3.png"), 
                                pygame.image.load("./images/right4.png"), 
                                pygame.image.load("./images/right5.png")]
        self.__walking_backward = [pygame.image.load("./images/front1.png"), 
                                  pygame.image.load("./images/front2.png"), 
                                  pygame.image.load("./images/front3.png"), 
                                  pygame.image.load("./images/front4.png"), 
                                  pygame.image.load("./images/front5.png")]
        self.__walking_forward = [pygame.image.load("./images/back1.png"), 
                                   pygame.image.load("./images/back2.png"), 
                                   pygame.image.load("./images/back3.png"), 
                                   pygame.image.load("./images/back4.png"), 
                                   pygame.image.load("./images/back5.png")]
        # Fire-mode pictures
        self.__fire_right = [pygame.image.load("./images/fire1.png"),
                       pygame.image.load("./images/fire2.png"),
                       pygame.image.load("./images/fire3.png"),
                       pygame.image.load("./images/fire4.png")]
        self.__fire_left = [pygame.image.load("./images/fire_left1.png"),
                       pygame.image.load("./images/fire_left2.png"),
                       pygame.image.load("./images/fire_left3.png"),
                       pygame.image.load("./images/fire_left4.png")]
        # Dead picture
        self.__dies = pygame.image.load("./images/dead.png")
        
        self.__forward = self.__walking_forward[0]
        
        # Instance variables to keep track of the screen surface and set
        # the initial x, y vectors for the player
        self.__screen = screen
        self.__dx = 0
        self.__dy = 0
        self.__index = 0
        
        self.__is_left = False
        self.__is_right = False
        self.__is_forward = False
        self.__is_backward = False
        self.__is_firing = False
        
        self.image = self.__forward
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.__screen.get_width()/2, 
                               self.__screen.get_height())
        
    def change_direction(self, direction):
        '''This method takes a direction as a parameter and sets the x, y
        vectors for the player'''
        if direction == "left":
            self.__is_left = True
            self.__dx = -7
            self.__dy = 0 
        elif direction == "right":
            self.__is_right = True
            self.__dx = 7
            self.__dy = 0   
        elif direction == "forward":
            self.__is_forward = True
            self.__dx = 0
            self.__dy = -7  
        elif direction == "backward":
            self.__is_backward = True
            self.__dx = 0
            self.__dy = 7          
               
    def dies(self):
        '''This method changes the image to the dead figure for the player'''
        self.image = self.__dies
   
    def take_boat(self, speed):
        '''This method takes a speed integer as a parameter and sets the x vector
        equal to the speed'''
        self.__dx = speed
        
    def reset(self):
        '''This method resets the player's position, sets the speed to 0
        and loads the default image'''
        self.__dx = 0
        self.image = self.__forward
        self.rect.midbottom = (self.__screen.get_width()/2, 
                               self.__screen.get_height())
    
    def stop(self):
        '''This method stops the player from moving'''
        self.__is_left = False
        self.__is_right = False
        self.__is_forward = False
        self.__is_backward = False        
        self.__dx = 0
        self.__dy = 0
        
    def fire(self):
        '''This method changes the image to the motions of firing for the 
        player'''
        self.__is_firing = True
        self.__walking_right = self.__fire_right
        self.__walking_left = self.__fire_left
    
    def misfire(self):
        '''This method changes the firing images back to normal for 
        the player'''
        self.__is_firing = False
        self.__walking_left = [pygame.image.load("./images/left1.png"), 
                               pygame.image.load("./images/left2.png"), 
                               pygame.image.load("./images/left3.png"), 
                               pygame.image.load("./images/left4.png")]
        self.__walking_right = [pygame.image.load("./images/right1.png"), 
                                pygame.image.load("./images/right2.png"), 
                                pygame.image.load("./images/right3.png"), 
                                pygame.image.load("./images/right4.png"), 
                                pygame.image.load("./images/right5.png")]
        
    def update(self):
        '''This method will be called automatically to reposition the player
        sprite on the screen and to load the appropriate animated picture
        for the character'''
        self.rect.left += self.__dx
        self.rect.top += self.__dy 
        # Since different motions have different amount of elements in the
        # motion lists, we use a "try - except" to keep track of 
        # the index of the list
        try:
            if self.__is_left:
                self.image = self.__walking_left[self.__index]
            if self.__is_right:
                self.image = self.__walking_right[self.__index]
            if self.__is_forward:
                self.image = self.__walking_forward[self.__index]
            if self.__is_backward:
                self.image = self.__walking_backward[self.__index]
        except IndexError:
            self.__index = 0
            
        if self.rect.left <= 0:
            self.rect.left = 0 
        if self.rect.right >= self.__screen.get_width():
            self.rect.right = self.__screen.get_width()
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.__screen.get_height():
            self.rect.bottom = self.__screen.get_height()
            
        self.__index += 1
        
            
class Gold(pygame.sprite.Sprite):
    '''This class defines the gold sprite for our game'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, initializes 
        the image and rect for our gold sprite'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__screen = screen
        self.image = pygame.image.load("./images/gold.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, self.__screen.get_width()), 
                            random.randint(50, self.__screen.get_height()-50))
        
class House(pygame.sprite.Sprite):
    '''This class defines the destination in our game'''
    def __init__(self, bottom):
        '''This initializer takes a bottom integer as a parameter to position 
        the house image on the right spot'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./images/house.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom 
        self.rect.left = random.randint(1,400)
        
    def move(self):
        '''This method moves the still image horizontally within a range
        of 1 to 400'''
        self.rect.left = random.randint(1, 400)
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines the score keeper for our game'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, 
        loads the custom font "AltamonteNF.ttf", and sets the initial 
        score to 0 and life to 5'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font("./fonts/AltamonteNF.ttf", 50)
        self.__score = 0
        self.__life = 5
        self.__screen = screen
        
    def scored(self, score):
        '''This method takes a score integer as a parameter, and adds the 
        score points to the instance variable __score'''
        self.__score += score
    
    def life_lost(self):
        '''This method minuses 1 life'''
        self.__life -= 1
        
    def life_gained(self):
        '''This method adds 1 life'''
        self.__life += 1
        
    def game_over(self):
        '''This method returns if all the lives are gone'''
        return self.__life == 0
    
    def get_score(self):
        '''This method returns the current score the player has gained'''
        return self.__score
    
    def default(self):
        '''This method changes the score and life back to the default value:
        score to 0 and life to 5'''
        self.__score = 0
        self.__life = 5
        
    def update(self):
        '''This method will be called automatically to display the current
        score and life left at the bottom right of the screen'''
        message = "Score: %d   Life: %d" % (self.__score, self.__life)
        self.image = self.__font.render(message, 1, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.bottomright = (self.__screen.get_width(), 
                                 self.__screen.get_height())
        
class MovingSprites(pygame.sprite.Sprite):
    '''This class defines all the moving sprites in our game'''
    def __init__(self, screen, image, bottom, left):
        '''This initializer takes a screen surface, an image path, a bottom 
        integer, and a left integer as parameters; loads the appropriate 
        image and positions it on the appropriate location'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__screen = screen
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.left = left
         
        self.__dx = random.randint(-15,-5)
        
    def reset(self):
        '''This method resets the position of the moving sprite, and changes
        the speed randomly'''
        self.rect.left = self.__screen.get_width()
        self.__dx = random.randint(-15,-7)
        
    def speed_down(self):
        '''This method causes the moving sprite to speed down'''
        self.__dx = -5
        
    def get_speed(self):
        '''This method returns the current speed'''
        return self.__dx
    
    def update(self):
        '''This method will be called automatically to reposition the 
        moving sprite on the screen. If the moving sprite runs out of the 
        screen, it will call the reset() method'''
        self.rect.left += self.__dx
        
        if self.rect.right <= 0:
            self.reset()
        

class SpecialGold(pygame.sprite.Sprite):
    '''This class defines the golden egg (special gold) for our game'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, loads the
        golden egg image and positions it initially out of the screen'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./images/golden egg.png")
        self.__screen = screen
        self.rect = self.image.get_rect()
        self.rect.top = self.__screen.get_height()+10
        
    def appear(self):
        '''This method causes the special gold to appear randomly 
        on the screen'''
        self.rect.center = (random.randint(0, self.__screen.get_width()), 
                            random.randint(0, self.__screen.get_height()))
        
    def disappear(self):
        '''This method causes the special gold to appear out of the screen'''
        self.rect.top = self.__screen.get_height()+10

class Label(pygame.sprite.Sprite):
    '''This class defines the label sprite for our game'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter,
        loads a custom font "ChineseTakeaway.ttf", and sets the initial
        text to blank'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__font = pygame.font.Font("./fonts/ChineseTakeaway.ttf", 60)
        self.__text = ''
        self.__screen = screen
        self.__centerx = self.__screen.get_width()/2
        self.__bottom = 0
        
    def default(self):
        '''This method changes the text back to blank'''
        self.__text = ''
        
    def set_text(self, message, bottom):
        '''This method takes a message and a bottom integer as parameters,
        sets the message to __text and bottom to __bottom'''
        self.__text = message
        self.__bottom = bottom
        
    def update(self):
        '''This method will be called automatically to display the text
        on the screen'''
        self.image = self.__font.render(self.__text, 1, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.__centerx, self.__bottom)
        
class TextBubble(pygame.sprite.Sprite):
    '''This class defines the text bubble sprites for our game'''
    def __init__(self,screen):
        '''This initializer takes a screen surface as a parameter, loads
        images that will be used in advance, and sets the current image
        to nothing'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__screen = screen
        self.__points = pygame.image.load("./images/points.png")
        self.__fire = pygame.image.load("./images/fire.png")
        self.__life = pygame.image.load("./images/life.png")
        self.image = pygame.Surface((0,0))
        self.rect = self.image.get_rect()
        
        
    def add_points(self, center):
        '''This method takes a tuple as a parameter. When it is called, 
        it will display a picture with the information that points have been 
        added.'''
        self.image = self.__points
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def fire(self, center):
        '''This method takes a tuple as a parameter. When it is called, it
        will display a picture with the information that now the player is 
        able to fire (namely, to resist cars)'''
        self.image = self.__fire
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def life(self,center):
        '''This method takes a tuple as a parameter. When it is called, it
        will display a picture with the information that 1 life has been 
        added to the player'''
        self.image = self.__life
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def disappear(self):
        '''This method will put the text bubble sprite out of the screen'''
        self.rect.top = self.__screen.get_height()+10

class Background(pygame.sprite.Sprite):
    '''This class defines the menu and help backgrounds for our menu'''
    def __init__(self):
        '''This initializer sets the default background to be the menu window'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./images/menu.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        
    def menu(self):
        '''This method changes the background back to menu interface'''
        self.image = pygame.image.load("./images/menu.jpg").convert()
        
    def help(self):
        '''This method changes the background to help interface'''
        self.image = pygame.image.load("./images/help.jpg").convert()
           