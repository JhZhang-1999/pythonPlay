# learning pygame
import pygame, os, random

# 参考：https://www.jianshu.com/p/17a8ff70e00f

WINDOW_W, WINDOW_H = 640, 480
FPS = 50
g = 9.8*100
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (200,100)
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("hello, world!")
clock = pygame.time.Clock()

if __name__ == '__main__':
    x = random.randint(10,WINDOW_W-10)
    y = random.randint(10,WINDOW_H-10)
    vx = random.randint(-10*100,10*100)
    vy = random.randint(-10*100,10*100)
    while True:
        # 接收到退出事件后退出程序
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        # 小球下一时刻的速度、位置计算
        vy += g * 1/FPS
        x += vx * 1/FPS
        y += vy * 1/FPS
        if y >= WINDOW_H-20 or y <= 20:
            # 到达地面则是其竖直速度反向
            vy = -vy
        if x >= WINDOW_W-20 or x <= 20:
            vx = -vx
        # 背景色设定
        screen.fill((12,36,64))
        # 根据球的坐标画圆
        pygame.draw.circle(screen, (190,202,231), (int(x), int(y)), 10)
        # 刷新画面
        pygame.display.update()
        # 设置FPS
        time_passed = clock.tick(FPS)
