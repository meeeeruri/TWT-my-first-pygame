import pygame

pygame.init()

### setup and start game window
screen_width = 500
screen_height = 480
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First Pygame")

### load impages
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), 
            pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), 
            pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), 
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), 
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
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
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0 # fram of walking count
        self.standing = True

    def draw(self, win):
        if self.walkCount +1 >= 27: # calculate fram of walking image
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y)) # load left walk image by fram (3 fram per image)
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))




class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius )



### draw the window
def redrawGameWindow():
    win.blit(bg, (0, 0)) # load backgro    und image
    man.draw(win) # draw character
    for bullet in bullets: # draw bullets
        bullet.draw(win)
    pygame.display.update() # publish the new picture to screen


### main loop
man = player(300, 410, 64, 64)
bullets = []
run = True

while run:
    ### pygame.time.delay(50) # alternate interval, also refresh rate between check input
    clock.tick(27) # set to 27 fps

    for bullet in bullets:
        if bullet.x < screen_width and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet)) # delete the bullet from list when exit screen

    for event in pygame.event.get(): # check input

        if event.type == pygame.QUIT: # check if user tent to quit game
            run = False
    
    ### check input
    keys = pygame.key.get_pressed() # identify input of movement
    
    if keys[pygame.K_SPACE]:
        # the direction of bullet
        if man.left:
            facing = -1
        else:
            facing = 1
        # add new bullet
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), 
                                      round(man.y + man.height // 2), 
                                      6, (0, 0, 0), facing))
    ## moving direction
    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.velocity
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.width:
        man.x += man.velocity
        man.right = True
        man.left = False
        man.standing = False
    else: # if we doing nothing
        man.standing = True
        man.walkCount = 0

    ## jumping process
    if not(man.isJump): # condition when opject is not jumping
        if keys[pygame.K_UP]:
            man.isJump = True
            # man.right = False
            # man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10: # reverse up to down at top position
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
