import pygame

pygame.init()

screen_width = 500
screen_height = 500

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First Pygame")

### object property
x = 50
y = 400
width = 40
height = 60
velocity = 10

isJump = False
jumpCount = 10

run = True

while run:
    pygame.time.delay(100) # interval, also refresh rate between check input

    for event in pygame.event.get(): # check input

        if event.type == pygame.QUIT: # check if user tent to quit game
            run = False

    keys = pygame.key.get_pressed() # identify input of movement
    if keys[pygame.K_LEFT] and x > 0:
        x -= velocity
    if keys[pygame.K_RIGHT] and x < screen_width - width:
        x += velocity
    if not(isJump): # condition when opject is not jumping
        if keys[pygame.K_UP] and y > 0:
            y -= velocity
        if keys[pygame.K_DOWN] and y < screen_height - height:
            y += velocity
        if keys[pygame.K_SPACE]:
            isJump = True
    ### jumping process
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    
    


    win.fill((0, 0, 0)) # fill the screen with black before drawing object's new position
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) # draw the object
    pygame.display.update() # publish the new picture to screen

pygame.quit()
