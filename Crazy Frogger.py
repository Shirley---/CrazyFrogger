'''
Author: Shirley Du

Date: May.30/11

Descrption: The goal of this game is to pick up all the golds on the ground 
while safely crossing the road and river to reach the destination. It is a 
single-player game. Five lives will be given to the player. To win, the 
player has to avoid all the cars running randomly and pick up all the golds(100)
on the ground. In the meantime, there will be some special gold falling from 
the sky. The special gold holds 3 special abilities. The 
first one is Fire, which enables the player to hit cars without losing lives. 
The second one is Super Gold, which is worth 50 points.The third one is Life 
Bottle, which gives the player one more life. After all the golds are 
picked up, the player will have to go across a river to reach the 
destination. There will be boats floating on the river at a fairly fast speed 
and the player will carefully go on boats without falling into water. The 
player will use arrow keys to control the character.
'''

# I - IMPORT AND INITIALIZE
import pygame, froggerSprites, random
pygame.init() 
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))

def main():
    '''This function defines the 'mainline logic' for our Crazy Frogger Game'''
    
    # DISPLAY
    pygame.display.set_caption("Crazy Frogger!")
     
    # E - Entities 
    window = pygame.Surface(screen.get_size())
    window = window.convert()
    screen.blit(window, (0,0))

    # Sprites for menu: play_button,help_button,quit_button,back_button,mouse
    play_button = froggerSprites.Button("P L A Y",(450,300))
    help_button = froggerSprites.Button("H E L P",(450,360))
    quit_button = froggerSprites.Button("Q U I T",(450,420))
    back_button = froggerSprites.Button("B A C K",(500,450))
    mouse = froggerSprites.Mouse()
    background = froggerSprites.Background()
    
    # Sprites for both scenes: player, score_keeper, label1, label2
    player = froggerSprites.Player(screen)
    score_keeper = froggerSprites.ScoreKeeper(screen)
    label1 = froggerSprites.Label(screen)
    label2 = froggerSprites.Label(screen)
    
    allSprites = pygame.sprite.Group(background, play_button,quit_button,
                                     help_button, mouse)
    
    pygame.mixer.music.load("./sounds/intro.ogg")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    is_menu_background = True
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)

    # L - Loop
    while keepGoing:
        # T - Timer to set frame rate
        clock.tick(30)

        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the player clicks "play", the screen will jump to
                # the first scene
                if mouse.rect.colliderect(play_button.rect) and \
                is_menu_background == True:
                    label1.default()
                    label2.default()
                    score_keeper.default()
                    player.reset()
                    first_scene(player, score_keeper, label1, label2)   
                    pygame.mixer.music.load("./sounds/intro.ogg")
                    pygame.mixer.music.set_volume(1)
                    pygame.mixer.music.play(-1)
                # If the player clicks "help", the background will change 
                # to the help window with only a "back" button on the screen
                elif mouse.rect.colliderect(help_button.rect) and \
                is_menu_background == True:
                    background.help()      
                    allSprites = pygame.sprite.Group(background, back_button, 
                                                     mouse)
                    is_menu_background = not is_menu_background
                # If the player clicks "back", the background will change
                # back to the main menu window
                elif mouse.rect.colliderect(back_button.rect) and \
                is_menu_background == False:
                    background.menu()
                    allSprites = pygame.sprite.Group(background, play_button,
                                                     quit_button,help_button, 
                                                     mouse)
                    is_menu_background = not is_menu_background
                # If the player clicks "quit", the window will be closed
                elif mouse.rect.colliderect(quit_button.rect) and \
                is_menu_background == True:
                    keepGoing = False

                    
        for button in [play_button, quit_button, help_button, back_button]:
            if mouse.rect.colliderect(button.rect):
                button.change_color()
            else:
                button.change_color_back()


        # R - Refresh display
        allSprites.clear(screen,window)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
     
    # Close the window
    pygame.quit()
    
def first_scene(player, score_keeper, label1, label2):
    '''This function defines the first scene in our Crazy Frogger game. It
    takes player, score_keeper, label, and label2 sprites as parameters'''
    
    # ENTITIES
    background = pygame.image.load("./images/level1.jpg")
    background = background.convert()
    screen.blit(background, (0,0))
    
    # Sprites for: golds, cars, special gold, and text_bubble
    golds = []
    for i in range(100):
        golds.append(froggerSprites.Gold(screen))
    car1 = froggerSprites.MovingSprites(screen, "./images/car1.png", 410, 
                                        screen.get_width())
    car2 = froggerSprites.MovingSprites(screen, "./images/car2.png", 340, 
                                        screen.get_width())
    car3 = froggerSprites.MovingSprites(screen, "./images/car3.png", 250, 
                                        screen.get_width())
    car4 = froggerSprites.MovingSprites(screen, "./images/car4.png", 180, 
                                        screen.get_width())
    car5 = froggerSprites.MovingSprites(screen, "./images/car5.png", 100, 
                                        screen.get_width())
    text_bubble = froggerSprites.TextBubble(screen)
    
    special_gold = froggerSprites.SpecialGold(screen)
    carSprites = pygame.sprite.Group(car1, car2, car3, car4, car5)
    goldSprites = pygame.sprite.Group(golds)
    allSprites = pygame.sprite.OrderedUpdates(score_keeper,golds, 
                                              special_gold, carSprites, 
                                              player, text_bubble, label1)
    
    pygame.mixer.music.load("./sounds/Meet the pirates.mid")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    gold_eaten = pygame.mixer.Sound("./sounds/msg-gratz.wav")
    gold_eaten.set_volume(0.3)

    
    # ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    
    checked = False
    lucky_check = False
    hit_car = False
    count_death = 0
    count = 0
    lucky_num = 0
    luck = 0
    special_ability1 = False
    special_ability2 = False
    special_ability3 = False
    check_death = False
    golden_egg_position = 0
    level = True
    car_hit = False
    
    # LOOP
    while keepGoing:
        # TIME
        clock.tick(30)
        
        # EVENT HANDLING: the player is going to use arrow keys to control
        # the character
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    player.change_direction("right")
                elif event.key == pygame.K_UP:
                    player.change_direction("forward")
                elif event.key == pygame.K_DOWN:
                    player.change_direction("backward")       
            elif event.type == pygame.KEYUP:
                player.stop()
        
        # To display a "level 1" message
        if level:
            label1.set_text("LEVEL 1", 260)
            count += 1
            if count == 30:
                count = 0
                allSprites.remove(label1)
                level = False
        
        luck = random.randrange(100)
        
        # If luck is equal to 1, then the special golden egg will 
        # appear
        if luck == 1 and lucky_check == False and special_ability1 == False and\
           special_ability2 == False and special_ability3 == False:
            special_gold.appear()
            lucky_check = True
            lucky_num = random.randint(1,3)
        
        # If the player has hit the special gold, one of the 3 special
        # abilities will be enabled
        if player.rect.colliderect(special_gold.rect):
            lucky_check = False
            golden_egg_position = special_gold.rect.center
            special_gold.disappear()
            if lucky_num == 1:
                special_ability1 = True          
            elif lucky_num == 2:
                special_ability2 = True
            elif lucky_num == 3:
                special_ability3 = True
        
        # For special ability 1, the player will be able to move around
        # freely without being hit by any car for 10 seconds
        if special_ability1:
            text_bubble.fire(golden_egg_position)
            player.fire()
            hit_car = True
            count += 1
            if count == 300:
                text_bubble.disappear()
                hit_car = False
                player.misfire()
                special_ability1 = False
                count = 0
        
        # For special ability 2, 50 points will be added to the score keeper
        elif special_ability2:
            text_bubble.add_points(golden_egg_position)
            count += 1
            if count == 30:
                text_bubble.disappear()
                score_keeper.scored(50)
                special_ability2 = False
                count = 0
        
        # For special ability 3, the player will gain 1 more life
        elif special_ability3:
            text_bubble.life(golden_egg_position)
            count += 1
            if count == 30:
                text_bubble.disappear()
                score_keeper.life_gained()
                special_ability3 = False
                count = 0
        
        # If the player hits a gold, 1 point will be added to the score keeper
        for i in pygame.sprite.spritecollide(player, goldSprites, True):
            score_keeper.scored(1)
            gold_eaten.play()
        
        # If the player hits a car, 1 life will be deducted
        if pygame.sprite.spritecollide(player,carSprites, False) and \
           hit_car == False:
            car_hit = True
            
        if car_hit:
            player.stop()
            player.dies()
            count_death += 1
            if count_death == 10:
                count_death = 0
                player.reset()
                score_keeper.life_lost()
                car_hit = False
            
               
        # If the player has no life left, everything will stop moving,
        # and a fail text will appear at the centre of the screen.
        # It will terminate the game and go back to the menu.
        # Although it's not the most efficient way to end the game, the author
        # does not want to use 'keepGoing = False' and 'time.sleep(whatever)'
        # just so that users can go back to the menu at any time they want
        # (when get sick of the siren sound LOL)or terminate the game earlier
        # at any time they wish without having to wait for a few boring seconds,
        # also for the purpose of keeping the siren wailing.
        if score_keeper.game_over() and check_death == False:
            player.stop()
            label1.set_text("YOU LOST", 200)
            label2.set_text("Your score: %d" % score_keeper.get_score(), 300)
            allSprites = pygame.sprite.Group(score_keeper,label1, label2)
            pygame.mixer.music.load("./sounds/Police.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            check_death = True

        # If all the golds are eaten, then it will jump to the second scene            
        if not goldSprites and checked == False:
            player.misfire()
            player.reset()
            second_scene(player, score_keeper, label1, label2)
            checked = True
            keepGoing = False

        
        # REFRESH
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()

             
def second_scene(player, score_keeper, label1, label2):
    '''This function takes player, score_keeper, label1, and label2 sprites as 
    parameters, and it is the second scene in our Crazy Frogger game'''
    
    # ENTITIES
    background = pygame.image.load("./images/level2.jpg")
    background = background.convert()
    screen.blit(background, (0,0))
    
    # Sprites for: boats and house
    boat1 = froggerSprites.MovingSprites(screen, "./images/boat1.png", 430, 
                                         screen.get_width())
    boat11 = froggerSprites.MovingSprites(screen, "./images/boat1.png", 430, 
                                          screen.get_width()+250)
    boat2 = froggerSprites.MovingSprites(screen, "./images/boat2.png", 393, 
                                         screen.get_width())
    boat22 = froggerSprites.MovingSprites(screen, "./images/boat2.png", 393, 
                                          screen.get_width()+250)
    boat3 = froggerSprites.MovingSprites(screen, "./images/boat3.png", 374, 
                                         screen.get_width())
    boat33 = froggerSprites.MovingSprites(screen, "./images/boat3.png", 374, 
                                          screen.get_width()+250)
    boat4 = froggerSprites.MovingSprites(screen, "./images/boat4.png", 333, 
                                         screen.get_width())
    boat44 = froggerSprites.MovingSprites(screen, "./images/boat4.png", 333, 
                                          screen.get_width()+250)
    boat5 = froggerSprites.MovingSprites(screen, "./images/boat5.png", 285, 
                                         screen.get_width())
    boat55 = froggerSprites.MovingSprites(screen, "./images/boat5.png", 285, 
                                          screen.get_width()+250)
    house = froggerSprites.House(251)

    boat1Group = pygame.sprite.Group(boat1, boat2, boat3, boat4, boat5)
    boat2Group = pygame.sprite.Group(boat11, boat22, boat33, boat44, boat55)
    boatSprites = pygame.sprite.Group(boat1, boat11, boat2, boat22, 
                                      boat3,boat33, boat4, boat44, boat5, 
                                      boat55)
    allSprites = pygame.sprite.OrderedUpdates(boatSprites, house, 
                                              score_keeper,player, label1)
    
    pygame.mixer.music.load("./sounds/Airport.mid")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    
    # ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True
    count = 0
    count_death = 0
    check_death = False
    check_winner = False
    level = True
    die = False
    
    # LOOP
    while keepGoing:
        # TIME
        clock.tick(30)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_direction("left")
                elif event.key == pygame.K_RIGHT:
                    player.change_direction("right")
                elif event.key == pygame.K_UP:
                    player.change_direction("forward")
                elif event.key == pygame.K_DOWN:
                    player.change_direction("backward")       
            elif event.type == pygame.KEYUP:
                player.stop()
                
        # To display a "level 2" message
        if level:
            label1.set_text("LEVEL 2", 260)
            count += 1
            if count == 31:
                count = 0
                allSprites.remove(label1)
                level = False
            
        # If the player has collided with one of the boats, the boat
        # will carry the player
        for i in pygame.sprite.spritecollide(player,boatSprites, False): 
            player.take_boat(i.get_speed())

        
        # If the player falls into water or hits the ground instead of 
        # the house, 1 life will be deducted
        if not (pygame.sprite.spritecollide(player,boatSprites,False) or \
                player.rect.colliderect(house.rect)) and \
           player.rect.bottom < 430:
            die = True
                
        if die:
            player.stop()
            player.dies()
            count_death += 1
            if count_death == 10:
                count_death = 0
                player.reset()
                score_keeper.life_lost()
                die = False
            
                
        # The house will change a location every 500 frames (approximately
        # 16 seconds)
        count += 1
        if count == 500:
            house.move()
            count = 0
        
        # Checking if two boats are overlapping each other. If so, 
        # the boat at the back will go back 20 pixels and speed down
        for boat in boat1Group:
            for boat2 in boat2Group:
                if boat.rect.left < boat2.rect.left:
                    if boat2.rect.left <= boat.rect.right and \
                       boat2.rect.bottom == boat.rect.bottom:
                        boat2.rect.left == boat.rect.right + 20
                        boat2.speed_down()
                elif boat2.rect.left < boat.rect.left:
                    if boat.rect.left <= boat2.rect.right and \
                       boat2.rect.bottom == boat.rect.bottom:
                        boat.rect.left == boat.rect.right + 20
                        boat.speed_down()
       
        # If the player hits the house -- then YOU WIN!!!
        if player.rect.colliderect(house.rect) and check_winner == False:
            pygame.mixer.music.load("./sounds/Cheers.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)
            player.stop()
            label1.set_text("CONGRATZ!", 200)
            label2.set_text("Your score: %d" % score_keeper.get_score(), 300)
            allSprites = pygame.sprite.Group(score_keeper,label1, label2)
            check_winner = True
            
                        
        # If the player has no life left, everything will stop moving,
        # and a fail text will appear at the centre of the screen.
        # It will terminate the game and go back to menu.
        if score_keeper.game_over() and check_death == False:
            player.stop()
            label1.set_text("YOU LOST", 200)
            label2.set_text("Your score: %d" % score_keeper.get_score(), 300)
            allSprites = pygame.sprite.Group(score_keeper,label1, label2)
            pygame.mixer.music.load("./sounds/Police.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            check_death = True

        # REFRESH
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    


# Call the main function
main()