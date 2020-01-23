# 2020/1/22 完成主体功能
# 2020/1/23 上午 新增GAME OVER显示及计分功能
# 2020/1/23 下午 重构代码，缩短主函数长度；添加重开一局、最高分记录功能

import pygame, os, random

WINDOW_W, WINDOW_H = 640, 480
FPS = 50
g = 9.8*100
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (200,100)
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

butorgcolor = (255,255,205)
butovercolor = (255,163,153)
butclickcolor = (255,71,71)

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
    def show(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 15)

def gameoverprinter():
    screen.fill((0,0,0))
    gameovertext = my_font.render("GAME OVER!", True, (255,255,255))
    screen.blit(gameovertext,(WINDOW_W/2-120,WINDOW_H/2))
    againbutt = Button("Again?",butorgcolor,WINDOW_W/2-120,WINDOW_H/2+60,100,30,0)
    againbutt.show()
    if againbutt.state == 1:
        return 1
    exitbutt = Button("Exit",butorgcolor,WINDOW_W/2-120,WINDOW_H/2+120,100,30,0)
    exitbutt.show()
    if exitbutt.state == 1:
        return -1
    return 0

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
    def show(self):
        pygame.draw.rect(screen, eachwall.color, ((self.x,0),(self.length,self.h)))
        pygame.draw.rect(screen, eachwall.color, ((self.x,self.h + self.interval),(self.length,WINDOW_H)))

class Scoreboard(object):
    color = (12,36,64)
    def __init__(self,name,score,x,y):
        self.name = name
        self.score = score
        self.x = x
        self.y = y
    def scoreup(self):
        self.score += 1
    def show(self):
        scoretextstr = str(self.name) + str(self.score)
        scoretext = my_font.render(scoretextstr,True,(255,255,255))
        screen.blit(scoretext,(self.x,self.y))

class Button(object):
    def __init__(self,name,color,x,y,w,h,state):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.state = state
    def isover(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousex >= self.x and mousex <= self.x + self.w and mousey >= self.y and mousey <= self.y + self.h:
            self.color = butovercolor
        else:
            self.color = butorgcolor
    def isclick(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousex >= self.x and mousex <= self.x + self.w and mousey >= self.y and mousey <= self.y + self.h:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                self.color = butclickcolor
                if self.state == 0:
                    self.state = 1
    def show(self):
        self.isover()
        self.isclick()
        pygame.draw.rect(screen, self.color, ((self.x,self.y),(self.w,self.h)))
        buttontext = my_font.render(self.name,True,(0,0,0))
        screen.blit(buttontext,(self.x,self.y))

if __name__ == '__main__':
    my_font = pygame.font.SysFont("microsoft Yahei", 40)
    bestscore = Scoreboard("Best: ",0,0,30)
    while True:
        bird = Bird(WINDOW_H/2,WINDOW_W/2,0,200,0,0)
        wall = Wall(WINDOW_W,random.randint(100,WINDOW_H-100))
        scoreboard = Scoreboard("Score: ",0,0,0)
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
                newwall = Wall(WINDOW_W,random.randint(100,WINDOW_H-100))
                walllist.append(newwall)
            switch = 0 # 0无，1重开，-1退出
            if bird.death == 0:
                if walllist[presentwallindex].x <= bird.x - 30:
                    scoreboard.scoreup()
                    presentwallindex += 1
                    if scoreboard.score > bestscore.score:
                        bestscore.score = scoreboard.score
                bird.show()
                for eachwall in walllist:
                    eachwall.show()
            else:
                switch = gameoverprinter()
            scoreboard.show()
            bestscore.show()
            pygame.display.update()
            time_passed = clock.tick(FPS)
            if switch == 1:
                break
            elif switch == -1:
                exit()
