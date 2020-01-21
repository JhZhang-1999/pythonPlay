# 2020/1/21 17:22 update: 将上一版本的代码用oop重构，增加生成新球的按钮功能，但存在bug即长按会不停生成。
# 2020/1/21 20:16 update: 确定生成新球的方式为屏幕中每球带动2个裂变的方式，并修复按按钮bug，按一次生成一次新球。

import pygame, os, random

# 参考：https://www.jianshu.com/p/17a8ff70e00f

WINDOW_W, WINDOW_H = 640, 480
FPS = 50
g = 9.8*100
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (200,100)
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()

ballcolor = (190,202,231)
butorgcolor = (255,255,205)
butovercolor = (255,163,153)
butclickcolor = (255,71,71)

class Ball(object):
    count = 0
    def __init__(self,number,color,x,y,vx,vy):
        self.__number = number
        self.color = color
        Ball.count += 1
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def move(self):
        self.vy += g * 1/FPS
        self.x += self.vx * 1/FPS
        self.y += self.vy * 1/FPS
        if self.y >= WINDOW_H-20 or self.y <= 20:
            self.vy = -self.vy
        if self.x >= WINDOW_W-20 or self.x <= 20:
            self.vx = -self.vx
    def collision(self,otherball):
        if abs(self.x-otherball.x) <= 19 and abs(self.y-otherball.y) <= 19:
            self.vx = -self.vx
            self.vy = -self.vy
            otherball.vx = -otherball.vx
            otherball.vy = -otherball.vy

class Button(object):
    def __init__(self,name,color,position,state):
        self.name = name
        self.color = color
        self.position = position # position = x,y,w,h
        self.state = state
    def isover(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousex >= 580 and mousex <= 620 and mousey >= 30 and mousey <= 50:
            self.color = butovercolor
        else:
            self.color = butorgcolor
    def isclick(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousex >= 580 and mousex <= 620 and mousey >= 30 and mousey <= 50:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                self.color = butclickcolor
                if self.state == False:
                    self.state = True
                    return True
                else:
                    return False
        if self.state == True:
            self.state = False
        return False

def initball():
    x = random.randint(10,WINDOW_W-10)
    y = random.randint(10,WINDOW_H-10)
    vx = random.randint(-10*100,10*100)
    vy = random.randint(-10*100,10*100)
    return x,y,vx,vy

if __name__ == '__main__':
    x,y,vx,vy = initball()
    ball1 = Ball(1,ballcolor,x,y,vx,vy)
    balllist = []
    balllist.append(ball1)
    button1 = Button("addball",butorgcolor,[580,30,40,20],False)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.fill((12,36,64))
        for eachball in balllist:
            eachball.move()
            for otherball in balllist:
                eachball.collision(otherball)
        button1.isover()
        if button1.isclick() == True:
            length = len(balllist)
            for i in range(length):
                for ctr in range(2):
                    t1, t2, vx, vy = initball()
                    newball = Ball(Ball.count,ballcolor,balllist[i].x,balllist[i].y,vx,vy)
                    balllist.append(newball)
        for eachball in balllist:
            pygame.draw.circle(screen, eachball.color, (int(eachball.x), int(eachball.y)), 10)
        pygame.draw.rect(screen, button1.color, ((button1.position[0],button1.position[1]),(button1.position[2],button1.position[3])))
        pygame.display.update()
        time_passed = clock.tick(FPS)
