import pygame

pygame.init()

### setup and start game window
screen_width = 500
screen_height = 500
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First Pygame")

### load impages
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')


clock = pygame.time.Clock() # load time to set fps

### object property
x = 50
y = 425
width = 64
height = 64
velocity = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0 # fram of walking count

### draw the window
def redrawGameWindow():
    global walkCount
    win.blit(bg, (0, 0)) # load background image
    
    if walkCount +1 >= 27: # calculate fram of walking image
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//3], (x, y)) # load left walk image by fram (3 fram per image)
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x, y))
        walkCount += 1
    else:
        win.blit(char, (x, y))


    pygame.display.update() # publish the new picture to screen

run = True

while run:
    ### pygame.time.delay(50) # alternate interval, also refresh rate between check input
    clock.tick(27) # set to 27 fps

    for event in pygame.event.get(): # check input

        if event.type == pygame.QUIT: # check if user tent to quit game
            run = False

    keys = pygame.key.get_pressed() # identify input of movement
    if keys[pygame.K_LEFT] and x > 0:
        x -= velocity
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < screen_width - width:
        x += velocity
        right = True
        left = False
    else: # if we doing nothing
        left = False
        right = False
        walkCount = 0
    if not(isJump): # condition when opject is not jumping
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0

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

    redrawGameWindow()
    
pygame.quit()
