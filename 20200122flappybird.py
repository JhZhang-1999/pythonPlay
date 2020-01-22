# 2020/1/22 start project

import pygame, os, random

WINDOW_W, WINDOW_H = 640, 480
FPS = 50
g = 9.8*100
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (200,100)
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

class Bird(object):
    color = (255,255,205)
    def __init__(self,x,y,vx,vy,state,death):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.state = state
        self.death = death
    def move(self,walllist):
        self.vy += g * 1/FPS
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            if self.state == 0:
                self.vy = -3 * 100
                self.state = 1
        else:
            self.state = 0
        self.x += self.vx * 1/FPS
        self.y += self.vy * 1/FPS
        self.outdeath()
        for eachwall in walllist:
            self.coldeath(eachwall)
    def outdeath(self):
        if self.x <= 10 or self.x >= WINDOW_W-10 or self.y <= 10 or self.y >= WINDOW_H-10:
            self.death = 1
    def coldeath(self,wall):
        if self.x <= wall.x + wall.length + 10 and self.x >= wall.x - 10:
            if self.y <= wall.h + 10:
                self.death = 1
            elif self.y >= wall.h + wall.interval - 10:
                self.death = 1

class Wall(object):
    color = (255,71,71)
    length = 50
    interval = 100
    def __init__(self,x,h):
        self.x = x
        self.h = h
    # x ~ x + length; 0 ~ h & h + interval ~ WINDOW_H; x starts from WINDOW_W
    def move(self):
        self.x -= 3

font = pygame.font.SysFont('microsoft Yahei',60)

if __name__ == '__main__':
    x = WINDOW_W/2
    y = WINDOW_H/2
    vx = 0
    vy = 2 * 100
    bird = Bird(x,y,vx,vy,0,0)
    wall = Wall(WINDOW_W,random.randint(100,WINDOW_H-100))
    walllist = []
    walllist.append(wall)
    while True:
        lastwallpos = walllist[len(walllist)-1].x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.fill((190,202,231))
        bird.move(walllist)
        for eachwall in walllist:
            eachwall.move()
        if lastwallpos <= WINDOW_W - 250:
            newwall = Wall(WINDOW_W,random.randint(80,WINDOW_H-80))
            walllist.append(newwall)
        if bird.death == 1:
            screen.fill((0,0,0))
            #text = font.render('Game Over!',False,(255,255,255))
            #screen.bilt(text,(100,100))
        else:
            pygame.draw.circle(screen, bird.color, (int(bird.x), int(bird.y)), 15)
            for eachwall in walllist:
                pygame.draw.rect(screen, eachwall.color, ((eachwall.x,0),(eachwall.length,eachwall.h)))
                pygame.draw.rect(screen, eachwall.color, ((eachwall.x,eachwall.h + eachwall.interval),(eachwall.length,WINDOW_H)))
        pygame.display.update()
        time_passed = clock.tick(FPS)
