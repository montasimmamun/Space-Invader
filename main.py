#    ------------------------------------------------------------------------------------------
#    Author    : Mohammad Montasim -Al- Mamun Shuvo
#    Copyright : Copyright 2020, Mohammad Montasim -Al- Mamun Shuvo
#    Email     : montasimmamun@gmail.com
#    Github    : https://github.com/montasimmamun/

#    Game Name : Space Invader
#    Date      : Created on 10/08/2020
#    Version   : 1.0.1
#    ------------------------------------------------------------------------------------------


import math
import os
import random
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

#   set game window size
screen_width = 800
screen_height = 600

# Game control variables
running = True

# Colors
gameName = (255, 0, 77)
enterToPlay = (0, 181, 184)
quitGame = (254, 225, 26)
scoreHighScore = (254, 225, 26)
gameOver = (255, 0, 77)
enterToContinue = (90, 39, 193)
qToQuit = (39, 159, 0)

gray=(119,118,110)
black=(0,0,0)
red=(255,0,0)
green=(0,200,0)
blue=(0,0,200)
bright_red=(255,0,0)
bright_green=(0,255,0)
bright_blue=(0,0,255)

#   set game fps
fps = 60
#   set clock for fps
clock = pygame.time.Clock()

#   scores
hiScore = 0
score = 0

#   set game window size to 800 x 600
game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("car game")
clock = pygame.time.Clock()
carimg = pygame.image.load('images/welcome_image.png')
backgroundpic = pygame.image.load("images/welcome_image.png")
yellow_strip = pygame.image.load("images/welcome_image.png")
strip = pygame.image.load("images/welcome_image.png")
intro_background=pygame.image.load("images/welcome_image.png")
instruction_background=pygame.image.load("images/welcome_image.png")
car_width = 56
pause = False

#   bullet definition
bullet_state = "ready"


#   display text to screen
def text_screen(text, color, x, y):
    #   set game font
    font = pygame.font.SysFont(None, 30)
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


#   update game display & fps
def DisplayUpdate():
    #   display above changes
    pygame.display.update()
    #   set fps to game
    clock.tick(fps)


# check if HiScore.txt file already exists
def CheckHighScoreFile():
    if (not os.path.exists("HiScore.txt")):
        with open("HiScore.txt", "w") as f:
            f.write("0")
            f.close()


#   write high score to HiScore.txt
def WriteHighScore():
    with open("Hi Score.txt", "w", encoding='utf-8') as f:
        f.write(str(hiScore))
        f.close()


#   event handling
def GameEvent():
    for event in pygame.event.get():
        #   if cross is pressed exit game window
        if event.type == pygame.QUIT:
            global running
            running = False

        #   if any key from keyboard is pressed set action
        if event.type == pygame.KEYDOWN:
            #   if enter key is pressed start game
            if event.key == pygame.K_RETURN:
                GameLoop()

            #   if q/Q key is pressed exit game window
            if event.key == pygame.K_q:
                #   game quit function
                quit()
                pygame.QUIT()


#   welcome screen
def Welcome():
    #   set welcome screen sound
    pygame.mixer.music.load('sounds/game.mp3')
    #   play welcome sound
    pygame.mixer.music.play()

    global running
    while running:
        #   set welcome image
        welcome_image = pygame.image.load("images/welcome_image.png")
        #   convert welcome image for display
        welcome_image = pygame.transform.scale(welcome_image, (screen_width, screen_height)).convert_alpha()
        #   display welcome image
        game_window.blit(welcome_image, (0, 0))

        #   display game option
        text_screen("Snake Game By Montasim", gameName, 290, 30)
        text_screen("Press Enter To Play", enterToPlay, 310, 542)
        text_screen("Press Q to Quit", quitGame, 325, 576)


        #   call event function
        GameEvent()

        #   update game display
        DisplayUpdate()


def GameLoop():
    # create the screen
    screen = pygame.display.set_mode((800, 600))

    # Background
    background = pygame.image.load('images/background.png')

    # Sound
    mixer.music.load("sounds/background.mp3")
    mixer.music.play(-1)

    # Caption and Icon
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)

    # Player
    playerImg = pygame.image.load('images/player.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 4

    CheckHighScoreFile()

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('images/enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(3)
        enemyY_change.append(30)

    # Bullet
    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    bulletImg = pygame.image.load('images/bullet.png')
    bulletX = 0
    bulletY = 480
    bulletY_change = 10

    # Score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    testY = 10

    # Game Over
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    # Game Loop
    global running
    while running:

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            global bullet_state
            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("sounds/laser.wav")
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                    GameOver()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("sounds/explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"

                score_value += 10

                global hiScore
                #   show high score
                with open("HiScore.txt", "r", encoding='utf-8') as f:
                    hiScore = f.read()
                    f.close()

                #   change hiScore
                if score_value > int(hiScore):
                    hiScore = score_value

                    #   write high score
                    with open("HiScore.txt", "w", encoding='utf-8') as f:
                        f.write(str(hiScore))
                        f.close()

                global score
                score = score_value
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)

        DisplayUpdate()


#   game over screen
def GameOver():
    #   set game over screen sound
    pygame.mixer.music.load('sounds/gameover.mp3')
    #   play game over screen sound
    pygame.mixer.music.play()

    global running
    while running:
        #   set welcome image
        welcome_image = pygame.image.load("images/gameover.png")
        #   convert welcome image for display
        welcome_image = pygame.transform.scale(welcome_image, (screen_width, screen_height)).convert_alpha()
        #   display welcome image
        game_window.blit(welcome_image, (0, 0))

        #   show high score
        with open("HiScore.txt", "r", encoding='utf-8') as f:
            hiScore = f.read()
            f.close()

        #   display game option
        text_screen("Score: " + str(score) + ", High Score: " + str(hiScore), gameName, 290, 60)
        text_screen("Enter To Play Again", enterToPlay, 300, 512)
        text_screen("Press Q to Quit", quitGame, 315, 546)

        #   call event function
        GameEvent()

        #   update game screen
        DisplayUpdate()


Welcome()
