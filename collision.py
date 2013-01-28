#! /usr/bin/env/python3
#################################################################################
# Programmed By:  Sophia Castellarin
# Program Description:  A program that will be used to simulate collision theory
# 			as it applies to model rockets with KNO-sucrose fuel.  
#			The porgram is designed for use in SCH 4UP ISP 
#			prestentation.  The program will display the effect of
#			increasing concentration of sugar on the reaction.
#################################################################################

import pygame
import random

sugar = (255,31,120)	#|
kno = (0,255,0)		#| The colours that will represent all the components of
corn = (255,247,0)	#| the fuel
water = (0,0,255)	#|

white = (255,255,255)	#|
black = (0,0,0)		#| Misc colours
fire = (255,0,0)	#|

num_kno = 40	#|
num_corn = 7	#| Default values for the amount of each substance
num_water = 32	#| in the fuel
num_sugar = 20	#|

num_collision = 0	# Keeps track of the number of collisions

print("sugar is pink\npotassium nitrate is green\ncorn is yellow\nwater is blue")

class fuel(pygame.sprite.DirtySprite):

    def __init__(self, colour, width, height):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.Surface([width,height])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(150, 550)
        self.rect.y = random.randrange(100, 550)
        self.image.fill(colour)
        self.dirty = 2

    # Updates the position of the sprite
    def update(self):
        global x_change
        global y_change

        self.rect.y += y_change
        self.rect.x += x_change

        if self.rect.y > 600 or self.rect.y < 50:
            y_change = (-1) * y_change
        else: pass        

        if self.rect.x > 600 or self.rect.x < 100:
            x_change = (-1) * x_change 
        else: pass

# Initializes pygame
pygame.init()
# Sets up the screen
pygame.display.set_caption("COOLISION, Waaa")
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode([screen_width,screen_height])

# Creates a font variable so things can be written on the screen
font = pygame.font.Font(None, 25)
SMLB = font.render("More Sugar", True, black)
SMLS = font.render("Less Sugar", True, black)
CCL = font.render("Number of sugar collisions:", True, black)

# Keeps the sprites make organized in lists
sugar_list = pygame.sprite.RenderPlain()	# For tracking sugar
all_list = pygame.sprite.RenderPlain()		# For moving sprites
control_list = pygame.sprite.RenderPlain()	# For controls

# Checks for any collisions between sugar or anything else
def check_collision():
    global num_collision

    a = pygame.sprite.groupcollide(sugar_list, all_list, False, False, None)
    b = pygame.sprite.truth(a)

    if b == True:
        num_collision += 1
    else:
        pass

# Resets the sprites after the user has changed the sugar settings
def reset():
    
    global all_list
    global sugar_list
    global num_collision

    # Resets the number of collision counter
    num_collision = 0

    # Clears all list so that new sprites can be made
    for item in all_list:
        all_list.remove(item)
    for item in sugar_list:
        sugar_list.remove(item)
 
    # Will create the sprites for all the ingredients but the sugar
    # Sprites for KNO
    for i in range(num_kno):
        kno_sprite = fuel(kno, 10, 10)
        kno_sprite.rect.x = random.randrange(100, 600)
        kno_sprite.rect.y = random.randrange(50, 600)
        #kno_list.add(kno_sprite)
        all_list.add(kno_sprite)

    # Sprites for corn syrup
    for i in range(num_corn):
        corn_sprite = fuel(corn, 10, 10)
        corn_sprite.rect.x = random.randrange(100, 600)
        corn_sprite.rect.y = random.randrange(50, 600)
        #corn_list.add(corn_sprite)
        all_list.add(corn_sprite)

    # Sprites for water
    for i in range(num_water):
        water_sprite = fuel(water, 10, 10)
        water_sprite.rect.x = random.randrange(100, 600)
        water_sprite.rect.y = random.randrange(50, 600)
        #water_list.add(water_sprite)
        all_list.add(water_sprite)

    # Sprites for sugar
    for i in range(num_sugar):
        sugar_sprite = fuel(sugar, 10, 10)
        sugar_sprite.rect.x = random.randrange(100, 600)
        sugar_sprite.rect.y = random.randrange(50, 600)
        sugar_list.add(sugar_sprite)
        #all_list.add(sugar_sprite)

# Sprite that will show the [sugar] in the fuel
sugar_key = fuel(black, 25, 20)
sugar_key.rect.x = 25
sugar_key.rect.y = 300
control_list.add(sugar_key)

# Manages how fast the screen updates
clock = pygame.time.Clock()

# Key repeating
pygame.key.set_repeat(100,5)

done = True

reset()

# Main program loop
while done == True:    
    num_collision_string = str(num_collision)  

    check_collision() 

    # Speed of particles
    y_change = 1
    x_change = 1 

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = False  
            if event.key == pygame.K_f:
            # Defines a box with dimensions 100-600 (x), 50-600 (y) after flame
                pygame.draw.line(screen, fire, [100,50], [600, 50], 5)  
                pygame.draw.line(screen, fire, [100,50], [100, 600], 5)
                pygame.draw.line(screen, fire, [600,50], [600, 600], 5) 
                pygame.draw.line(screen, fire, [100,600], [600, 600], 5)  
                y_change = 10
                x_change = 10
            if event.key == pygame.K_UP:
                if sugar_key.rect.y > 130:
                    sugar_key.rect.y -= 16
                    num_kno -= 4 
                    num_water -= 3
                    num_corn -= 1
                    num_sugar += 8
                    reset()
                else:
                    pass
            if event.key == pygame.K_DOWN:
                if sugar_key.rect.y < 340:
                    sugar_key.rect.y += 16
                    num_kno += 4
                    num_water += 3
                    num_corn += 1
                    num_sugar -= 8
                    reset()
                else:
                    pass 

    control_list.draw(screen)	# Draws the [sugar] monitor to the screen
    all_list.draw(screen)	# Draws all the sprites to the screen
    sugar_list.draw(screen)
    clock.tick(60)		# 20 fps
    pygame.display.flip()	# Updates the screen
    screen.fill(white)
    all_list.update()
    sugar_list.update()
    
    CC = font.render(num_collision_string, True, black)
    # The [sugar] and collision monitors 
    screen.blit(SMLB, [0, 90])
    screen.blit(SMLS, [0, 395])
    screen.blit(CCL, [0, 650])
    screen.blit(CC, [250, 650])
    pygame.draw.line(screen, black, [25, 122], [50, 122], 5)
    pygame.draw.line(screen, black, [25, 370], [50, 370], 5)
    pygame.draw.line(screen, black, [25, 122], [25, 370])
    pygame.draw.line(screen, black, [50, 122], [50, 370])
   
    # Defines a box with dimensions 100 - 600 (x), 50 - 600 (y) before flame
    pygame.draw.line(screen, black, [100,50], [600, 50], 5)  
    pygame.draw.line(screen, black, [100,50], [100, 600], 5)
    pygame.draw.line(screen, black, [600,50], [600, 600], 5) 
    pygame.draw.line(screen, black, [100,600], [600, 600], 5)  

 

pygame.quit()	# Ends the sim

