import pygame as pg
import os, sys, random, math
from pygame.locals import *

pg.init()
fpsClock = pg.time.Clock()
SIZE_X, SIZE_Y = 800, 600
surface = pg.display.set_mode((SIZE_X, SIZE_Y))
surfsize = surface.get_size()
pg.display.set_caption("Game")


class Obj():
    def __init__(self, x, y, speed, img, height, width):
        self.x = x
        self.y = y
        self.speed = speed
        self.height = height
        self.width = width
        self.img = pg.transform.scale(pg.image.load(img), (self.height, self.width))
        self.size = self.img.get_size()
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def draw(self):
        self.rect = self.img.get_rect(center=(self.x, self.y))
        surface.blit(self.img, self.rect)

    def __repr__(self):
        return f"{self.x}, {self.y}"


class Bird(Obj):
    def __init__(self, x, y, speed, img, height, width):
        super().__init__(x, y, speed, img, height, width)
        self.status = "Is a bird."

    def moving(self, keys):
        if (keys[pg.K_w] and keys[pg.K_d]):
            self.y += -self.speed[1]
            self.x += self.speed[0]
        elif (keys[pg.K_s] and keys[pg.K_d]):
            self.y += self.speed[1]
            self.x += self.speed[0]
        elif (keys[pg.K_s] and keys[pg.K_a]):
            self.y += self.speed[1]
            self.x += -self.speed[0]
        elif (keys[pg.K_w] and keys[pg.K_a]):
            self.y += -self.speed[1]
            self.x += -self.speed[0]
        elif keys[pg.K_w]:
            self.y += -self.speed[1]
        elif keys[pg.K_s]:
            self.y += self.speed[1]
        elif keys[pg.K_d]:
            self.x += self.speed[0]
        elif keys[pg.K_a]:
            self.x += -self.speed[0]

        # wall check
        if self.x+(self.width/2) > SIZE_X:
            self.x = SIZE_X
        if self.x < 0:
            self.x = 0
        if self.y > SIZE_Y:
            self.y = SIZE_Y
        if self.y < 0:
            self.y = 0


class Box(Obj):
    def __init__(self, x, y, speed, img, height, width):
        super().__init__(x, y, speed, img, height, width)
        self.status = "Is a box."

    def moving(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

        # wall check, speed = direction is reversed on the dimension
        if (self.rect.right >= SIZE_X and self.speed[0] > 0) or (self.rect.left <= 0 and self.speed[0] < 0):
            self.speed[0] = -self.speed[0]
        if (self.rect.bottom >= SIZE_Y and self.speed[1] > 0) or (self.rect.top <= 0 and self.speed[1] < 0):
            self.speed[1] = -self.speed[1]


# create objects manually
bird = Bird(50, 50, [10, 10], "black.png", 60, 60)
box = Box(250, 200, [6, 6], "red.png", 80, 80)

while True:
    surface.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        #elif event.type == MOUSEMOTION:
            #print("ok")
    keys = pg.key.get_pressed()  #checking pressed keys

    bird.moving(keys)

    # redraw objects
    box.draw()
    bird.draw()

    box.moving()
    # detect if boxes hit
    if bird.rect.colliderect(box.rect):
        print("HIT")

    pg.display.update()
    fpsClock.tick(30)
