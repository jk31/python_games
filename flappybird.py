import pygame as pg
import os, sys, random, math, time
from pygame.locals import *

pg.init()
fpsClock = pg.time.Clock()
SIZE_X, SIZE_Y = 800, 500
surface = pg.display.set_mode((SIZE_X, SIZE_Y))
font = pg.font.Font(None, 36)
pg.display.set_caption("Flappy Bird")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Bird(pg.sprite.Sprite):
    def __init__(self, speed = [5, 5]):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([30, 30])
        self.image.fill(BLACK)

        self.speed = speed
        self.status = "Is a bird."

        self.rect = self.image.get_rect()

    def moving(self, keys):
        if keys[pg.K_SPACE]:
            self.rect.bottom -= 10

    def gravity(self):
        self.rect.bottom += 5

class Box(pg.sprite.Sprite):
    def __init__(self, height, speed = 5):
        pg.sprite.Sprite.__init__(self)

        self.height = height
        self.image = pg.Surface([40, self.height])
        self.image.fill(RED)

        self.speed = speed
        self.status = "Is a box."

        self.rect = self.image.get_rect()

    def moving(self):
        self.rect.x -= self.speed

def main():

    counter = 0
    sprite_list = pg.sprite.Group()
    box_list = pg.sprite.Group()

    def box_creator(hole):
        box = Box(height=hole)
        box.rect.x = SIZE_X
        box.rect.y = 0
        box_list.add(box)
        sprite_list.add(box)

        box = Box(height=SIZE_Y - 100 - hole)
        box.rect.x = SIZE_X
        box.rect.y = SIZE_Y - box.height
        box_list.add(box)
        sprite_list.add(box)

    # create objects manually
    bird = Bird()
    bird.rect.x = 100
    bird.rect.y = SIZE_Y/2
    sprite_list.add(bird)


    START = time.time()
    while True:

        # create boxes after intervals
        counter += 1
        if counter == 60:
            box_creator(random.randrange(100, 300))
            counter = 0

        surface.fill(WHITE)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()


        keys = pg.key.get_pressed()  #checking pressed keys
        bird.moving(keys)

        for box in box_list:
            box.moving()
            if box.rect.right < 0:
                box_list.remove(box)

        bird.gravity()
        sprite_list.draw(surface)


        # detect if boxes hit by bird
        if pg.sprite.spritecollideany(bird, box_list) or (bird.rect.bottom >= SIZE_Y) or (bird.rect.top <= 0):
            print("HIT", time.time())
            END = time.time()

            #time.sleep(1)

            # GAME OVER STATE
            game_over(START, END)

        pg.display.update()
        fpsClock.tick(30)

def game_over(START, END):
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()

        if keys[K_RETURN]:
            print("restart")
            main()

        surface.fill((0, 0, 0))
        msg = f"Game Over - Survived {round(END - START, 2)} seconds"
        text = font.render(msg, True, WHITE)
        text_rect = text.get_rect()
        text_x = surface.get_width() / 2 - text_rect.width / 2
        text_y = surface.get_height() / 2 - text_rect.height / 2

        surface.blit(text, [text_x, text_y])

        pg.display.update()
        fpsClock.tick(30)

if __name__ == '__main__':
    main()