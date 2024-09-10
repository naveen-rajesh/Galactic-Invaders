import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))

background=pygame.image.load('./galaxy.png')
pygame.display.set_caption('Galactic Wars')
icon=pygame.image.load('./launch.png')


shuttle=pygame.image.load('./spaceship.png')
shuttleX = 370
shuttleY = 480
shuttleX_change = 0

enemy=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_enemy=6
for i in range(no_enemy):
    enemy.append(pygame.image.load('./ufo.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(30)

bullet=pygame.image.load('./bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

f=open("high_score.txt","r")
for x in f:
    currentscore=int(x.strip())
f.close()

score_value= 0
font=pygame.font.Font('freesansbold.ttf',36)
testX=10
testY=10
over=pygame.font.Font('freesansbold.ttf',84)

def show_score(x,y):
    score = font.render("High Score : " + str(currentscore), True, (235, 35, 48))
    screen.blit(score, (x-10, y-10))
    score=font.render("Score : "+ str(score_value),True,(235,35,48))
    screen.blit(score,(x+20,y+20))
def game_over():
    over_text = font.render("GAME OVER!!", True, (255, 255, 255))
    screen.blit(over_text, (280,250))
def player(x,y):
    screen.blit(shuttle, (x,y))

def opponent(x,y,i):
    screen.blit(enemy[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x+16,y+10))

def isCollision(w,x,y,z):
    distance = math.sqrt(math.pow(w-y,2) + math.pow(x-z,2))
    if distance < 27:
        return True
    else:
        return False

run=True
while run:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            print("Event polled")
            run=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shuttleX_change = -0.5
            if event.key == pygame.K_RIGHT:
                shuttleX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    b_sound=mixer.Sound('bullet.mp3')
                    b_sound.play()
                    bulletX = shuttleX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                shuttleX_change = 0

    shuttleX += shuttleX_change

    if shuttleX <=0:
        shuttleX = 0
    elif shuttleX >=736:
        shuttleX = 736

    for i in range(no_enemy):
            if enemyY[i]>450:
                for j in range(no_enemy):
                    enemyY[j]=2000
                game_over()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <=0:
                enemyX_change[i] = 0.3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >=736:
                enemyX_change[i] = -0.3
                enemyY[i] += enemyY_change[i]
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                e_sound = mixer.Sound('jump-15984.mp3')
                e_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            opponent(enemyX[i], enemyY[i],i)
    if score_value>currentscore:
        f1=open("high_score.txt","w")
        f1.write(str(score_value))
        f1.close()
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(shuttleX,shuttleY)
    show_score(testX,testY)
    pygame.display.update()
