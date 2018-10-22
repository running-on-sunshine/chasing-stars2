import pygame, sys, time, random
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up window
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Chasing Stars: A Collecting Game!')

# set up font + text color
font = pygame.font.SysFont(None, 48)
TEXTCOLOR = (0, 0, 0)

# set up images
# == BACKGROUND ==
background = pygame.image.load("backgrounds/snow-scene.png").convert()
backgroundScale = pygame.transform.scale(background, (800, 600))
# == PLAYER ==
player = pygame.Rect(300, 10, 40, 40)
playerImg = pygame.image.load('characters/walk2.png')
playerGrowImg = pygame.transform.scale(playerImg, (40, 40))
# == STAR ==
starImg = pygame.image.load('items/star.png')
starImgSize = pygame.transform.scale(starImg, (60, 60))

# set up sounds
starCollectSound = pygame.mixer.Sound('sounds/coin.wav')

# set up keyboard variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# run the game loop
while True:
    starCounter = 0
    newStar = 20
    stars = []
    for i in range(20):
        stars.append(pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20))
    
    score = 0

    while True:
        # check for the QUIT event 
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_LEFT:
                    moveLeft = True
                if event.key == pygame.K_RIGHT:
                    moveRight = True
                if event.key == pygame.K_UP:
                    moveUp = True
                if event.key == pygame.K_DOWN:
                    moveDown = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moveLeft = False
                if event.key == pygame.K_RIGHT:
                    moveRight = False
                if event.key == pygame.K_UP:
                    moveUp = False
                if event.key == pygame.K_DOWN:
                    moveDown = False

        starCounter += 1
        if starCounter >= newStar:
            # add new star
            starCounter = 0
            stars.append(pygame.Rect(random.randint(0, WIDTH - 20),
            random.randint(0, HEIGHT - 20), 20, 20))

        # draw the background onto the screen
        SCREEN.blit(backgroundScale, (0,0))

        # draw the score
        drawText("Score: %s" % (score), font, SCREEN, 10, 0)

        # move the player
        if moveDown and player.bottom < HEIGHT:
            player.top += MOVESPEED
        if moveUp and player.top > 0:
            player.top -= MOVESPEED
        if moveLeft and player.left > 0:
            player.left -= MOVESPEED
        if moveRight and player.right < WIDTH:
            player.right += MOVESPEED

        # draw player block onto screen
        SCREEN.blit(playerGrowImg, player)

        # check if player block has collided with any star blocks
        for star in stars [:]:
            if player.colliderect(star):
                stars.remove(star)
                # === PLAYER GROWS IN SIZE WITH EVERY STAR COLLECTION ===
                player = pygame.Rect(player.left, player.top, player.width + 2, player.height + 2)
                playerGrowImg = pygame.transform.scale(playerImg, (player.width, player.height))
                score += 1 # increase score
                starCollectSound.play()

        # draw the stars
        for star in stars:
            SCREEN.blit(starImgSize, star)

        # draw the window onto the screen
        pygame.display.update()
        mainClock.tick(40)