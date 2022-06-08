import pygame

pygame.init()

### setup and start game window
screen_width = 500
screen_height = 480
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First Pygame")

### load impages
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')


clock = pygame.time.Clock() # load time to set fps

### object class
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self. velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0 # fram of walking count
    def draw(self, win):
        if self.walkCount +1 >= 27: # calculate fram of walking image
            self.walkCount = 0
        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) # load left walk image by fram (3 fram per image)
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))


### draw the window
def redrawGameWindow():
    win.blit(bg, (0, 0)) # load background image
    man.draw(win)
    pygame.display.update() # publish the new picture to screen


### main loop
man = player(300, 410, 64, 64)
run = True

while run:
    ### pygame.time.delay(50) # alternate interval, also refresh rate between check input
    clock.tick(27) # set to 27 fps

    for event in pygame.event.get(): # check input

        if event.type == pygame.QUIT: # check if user tent to quit game
            run = False

    keys = pygame.key.get_pressed() # identify input of movement
    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.velocity
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.width:
        man.x += man.velocity
        man.right = True
        man.left = False
    else: # if we doing nothing
        man.left = False
        man.right = False
        man.walkCount = 0
    if not(man.isJump): # condition when opject is not jumping
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0

    ### jumping process
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()
    
pygame.quit()
