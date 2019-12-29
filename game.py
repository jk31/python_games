import pygame as pg
import os, sys, random, math
from pygame.locals import *

pg.init()
fpsClock = pg.time.Clock()
surface = pg.display.set_mode((800, 600))
surfsize = surface.get_size()
pg.display.set_caption("Game")


class Obj():
    def __init__(self, x, y, img, height, width):
        self.x = x
        self.y = y
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


bird = Obj(50, 50, "black.png", 60, 60)
box = Obj(400, 200, "red.png", 80, 80)

while True:
    surface.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        #elif event.type == MOUSEMOTION:
            #print("ok")

    keys = pg.key.get_pressed()  #checking pressed keys
    if keys[pg.K_UP] or keys[pg.K_w]:
        bird.y += -3
        print(bird)
    if keys[pg.K_DOWN] or keys[pg.K_s]:
        bird.y += 3
        print(bird)
    if (keys[pg.K_LEFT] or keys[pg.K_a]):
        bird.x += -3
        print(bird)
    if (keys[pg.K_RIGHT] or keys[pg.K_d]):
        bird.x += 3
        print(bird)

    box.x += 1
    box.y += 1

    box.draw()
    bird.draw()

    if bird.rect.colliderect(box.rect):
        print("HIT")

    pg.display.update()
    fpsClock.tick(30)
