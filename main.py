import pygame
import sys
import math
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((800, 600))

# Background
bg = pygame.image.load('background.png')
pygame.display.set_icon(bg)

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('arcade-game.png')
playerX = 370
playerY = 500
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
noe = 6

for i in range(noe):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Bullet
# Ready - you can't see the bullet on the screen
# Fire - bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2.25
bullet_state = "ready"

# Collision
def coll(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow((enemyY - bulletY), 2))
    if dist < 27:
        return True
    else:
        return False

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (180, 250))

def show(x, y):
    scoree = font.render('Score :' + str(score), True, (255, 255, 255))
    screen.blit(scoree, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_b(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Game loop
running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    buls = mixer.Sound('laser.wav')
                    buls.play()
                    bulletX = playerX
                    fire_b(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(noe):
        if enemyY[i] > 440:
            for j in range(noe):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = coll(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            culs = mixer.Sound('explosion.wav')
            culs.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_b(playerX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show(textx, texty)

    pygame.display.update()

pygame.quit()
mixer.quit()
sys.exit()
