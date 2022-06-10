from statistics import harmonic_mean
import pygame
import os

pygame.init()

# setup and start game window
screen_width = 500
screen_height = 480
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("First Pygame")

# load impages
walkRight = [pygame.image.load(os.path.join('images', 'R1.png')), pygame.image.load(os.path.join('images', 'R2.png')), pygame.image.load(os.path.join('images', 'R3.png')),
             pygame.image.load(os.path.join('images', 'R4.png')), pygame.image.load(os.path.join(
                 'images', 'R5.png')), pygame.image.load(os.path.join('images', 'R6.png')),
             pygame.image.load(os.path.join('images', 'R7.png')), pygame.image.load(os.path.join('images', 'R8.png')), pygame.image.load(os.path.join('images', 'R9.png'))]
walkLeft = [pygame.image.load(os.path.join('images', 'L1.png')), pygame.image.load(os.path.join('images', 'L2.png')), pygame.image.load(os.path.join('images', 'L3.png')),
            pygame.image.load(os.path.join('images', 'L4.png')), pygame.image.load(os.path.join(
                'images', 'L5.png')), pygame.image.load(os.path.join('images', 'L6.png')),
            pygame.image.load(os.path.join('images', 'L7.png')), pygame.image.load(os.path.join('images', 'L8.png')), pygame.image.load(os.path.join('images', 'L9.png'))]
bg = pygame.image.load(os.path.join('images', 'bg.jpg')).convert()
char = pygame.image.load(os.path.join('images', 'standing.png'))

clock = pygame.time.Clock()  # load time to set fps

bulletSound = pygame.mixer.Sound(os.path.join('sounds', 'bullet.mp3'))
hitSound = pygame.mixer.Sound(os.path.join('sounds', 'hit.mp3'))

music = pygame.mixer.music.load(os.path.join('sounds', 'music.mp3'))
pygame.mixer.music.play(-1)


score = 0

# object class


class player(object):
    def __init__(self, x, y, width, height):  # initialize the character
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.jumpDirect = 1
        self.left = False
        self.right = False
        self.walkCount = 0  # fram of walking count
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  # initialize hitbox

    def draw(self, win):
        if self.walkCount + 1 >= 27:  # calculate fram of walking image
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                # load left walk image by fram (3 fram per image)
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))
        # the copy from self.hitbox indicate the moving of it
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # draw hitbox

    def hit(self):
        self.x = 60
        self.y = 410
        self.walkCount = 0
        self.jumpCount = 0
        self.isJump = False
        self.jumpDirect = 1
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screen_width/2 - text.get_width()/2,
                        screen_height/2 - text.get_height()/2))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            if event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load(os.path.join('images', 'R1E.png')), pygame.image.load(os.path.join('images', 'R2E.png')), pygame.image.load(os.path.join('images', 'R3E.png')),
                 pygame.image.load(os.path.join('images', 'R4E.png')), pygame.image.load(os.path.join(
                     'images', 'R5E.png')), pygame.image.load(os.path.join('images', 'R6E.png')),
                 pygame.image.load(os.path.join('images', 'R7E.png')), pygame.image.load(os.path.join(
                     'images', 'R8E.png')), pygame.image.load(os.path.join('images', 'R9E.png')),
                 pygame.image.load(os.path.join('images', 'R10E.png')), pygame.image.load(os.path.join('images', 'R11E.png'))]
    walkLeft = [pygame.image.load(os.path.join('images', 'L1E.png')), pygame.image.load(os.path.join('images', 'L2E.png')), pygame.image.load(os.path.join('images', 'L3E.png')),
                pygame.image.load(os.path.join('images', 'L4E.png')), pygame.image.load(os.path.join(
                    'images', 'L5E.png')), pygame.image.load(os.path.join('images', 'L6E.png')),
                pygame.image.load(os.path.join('images', 'L7E.png')), pygame.image.load(os.path.join(
                    'images', 'L8E.png')), pygame.image.load(os.path.join('images', 'L9E.png')),
                pygame.image.load(os.path.join('images', 'L10E.png')), pygame.image.load(os.path.join('images', 'L11E.png'))]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 > 33:  # 3 fram per image for total 11 images
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0),
                             (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20,
                                                50 - ((50/10) * (10 - self.health)), 10))
            # the copy from self.hitbox indicate the moving of it
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # draw hitbox

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1  # reverse direction to left
                self.walkCount = 0  # reset image
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1  # reverse direction to right
                self.walkCount = 0  # reset image

    def hit(self):  # when collision happen
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

# draw the window


def redrawGameWindow():
    win.blit(bg, (0, 0))  # load backgro    und image
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (390, 10))
    man.draw(win)  # draw character
    goblin.draw(win)
    for bullet in bullets:  # draw bullets
        bullet.draw(win)
    pygame.display.update()  # publish the new picture to screen


# main loop
font = pygame.font.SysFont('comicsans', 30, True, True)
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True

while run:
    # pygame.time.delay(50) # alternate interval, also refresh rate between check input
    clock.tick(27)  # set to 27 fps

    # check if character collide with enemy
    if (man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and
            man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]):
        if (man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and
                man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]):
            man.hit()
            score -=5

    # limit shoot to 3 fram
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 6:
        shootLoop = 0

    for bullet in bullets:
        # check if bullet collide with enemy
        if (bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and
                bullet.y + bullet.radius > goblin.hitbox[1]):
            if (bullet.x + bullet.radius > goblin.hitbox[0] and
                    bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]):
                hitSound.play()
                goblin.hit()
                score += 1
                # delete the bullet upon confirm hit
                bullets.pop(bullets.index(bullet))
        # bullet keep moving within screen
        if bullet.x < screen_width and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            # delete the bullet from list when exit screen
            bullets.pop(bullets.index(bullet))

    for event in pygame.event.get():  # check input

        if event.type == pygame.QUIT:  # check if user tent to quit game
            run = False

    # check input
    keys = pygame.key.get_pressed()  # identify input of movement

    if keys[pygame.K_SPACE] and shootLoop == 0:
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
            bulletSound.play()
        shootLoop = 1

    # moving direction
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
    else:  # if we doing nothing
        man.standing = True
        man.walkCount = 0

    # jumping process
    if not(man.isJump):  # condition when opject is not jumping
        if keys[pygame.K_UP]:
            man.isJump = True
            # man.right = False
            # man.left = False
            man.walkCount = 0
            man.jumpDirect = 1
    else:
        if man.jumpCount >= -10:  # reverse up to down at top position
            man.jumpDirect = 1
            if man.jumpCount < 0:
                man.jumpDirect = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * man.jumpDirect
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            man.jumpDirect = 1

    redrawGameWindow()

pygame.quit()
