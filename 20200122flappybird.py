# 2020/1/22 完成主体功能
# 2020/1/23 新增GAME OVER显示及计分功能

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

class Scoreboard(object):
    color = (12,36,64)
    def __init__(self,score):
        self.score = score
    def scoreup(self):
        self.score += 1

if __name__ == '__main__':
    my_font = pygame.font.SysFont("microsoft Yahei", 40)
    bird = Bird(WINDOW_H/2,WINDOW_W/2,0,200,0,0)
    wall = Wall(WINDOW_W,random.randint(100,WINDOW_H-100))
    scoreboard = Scoreboard(0)
    walllist = []
    walllist.append(wall)
    presentwallindex = len(walllist)-1
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
            gameovertext = my_font.render("GAME OVER!", True, (255,255,255))
            screen.blit(gameovertext,(WINDOW_W/2-120,WINDOW_H/2))
        else:
            if walllist[presentwallindex].x <= bird.x - 30:
                scoreboard.scoreup()
                presentwallindex += 1
            pygame.draw.circle(screen, bird.color, (int(bird.x), int(bird.y)), 15)
            for eachwall in walllist:
                pygame.draw.rect(screen, eachwall.color, ((eachwall.x,0),(eachwall.length,eachwall.h)))
                pygame.draw.rect(screen, eachwall.color, ((eachwall.x,eachwall.h + eachwall.interval),(eachwall.length,WINDOW_H)))
        scoretextstr = "Score: " + str(scoreboard.score)
        scoretext = my_font.render(scoretextstr,True,(255,255,255))
        screen.blit(scoretext,(0,0))
        pygame.display.update()
        time_passed = clock.tick(FPS)
