import pygame as pg
import os, sys, random, math, time
from pygame.locals import *

import neat
import pickle


pg.init()
fpsClock = pg.time.Clock()
SIZE_X, SIZE_Y = 800, 600
surface = pg.display.set_mode((SIZE_X, SIZE_Y))
font = pg.font.Font(None, 36)
pg.display.set_caption("Survive")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)



class Bird(pg.sprite.Sprite):
    def __init__(self, speed = 15):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([20, 20])
        self.image.fill(BLACK)

        self.speed = speed
        self.status = "Is a bird."

        self.rect = self.image.get_rect()

    def moving(self, direction):
        if direction == "W":
            self.rect.y += -self.speed
        elif direction == "S":
            self.rect.y += self.speed
        elif direction == "D":
            self.rect.x += self.speed
        elif direction == "A":
            self.rect.x += -self.speed

        # wall check
        if self.rect.right> SIZE_X:
            self.rect.x = SIZE_X -self.image.get_width()
        if self.rect.left < 0:
            self.rect.x = 0
        if self.rect.bottom > SIZE_Y:
            self.rect.y = SIZE_Y - self.image.get_height()
        if self.rect.top < 0:
            self.rect.y = 0


class Box(pg.sprite.Sprite):
    def __init__(self, speed = [10, 10]):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface([40, 40])
        self.image.fill(RED)

        self.speed = speed
        self.status = "Is a box."

        self.rect = self.image.get_rect()

    def moving(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # wall check, speed = direction is reversed on the dimension
        if (self.rect.right >= SIZE_X and self.speed[0] > 0) or (self.rect.left <= 0 and self.speed[0] < 0):
            self.speed[0] = -self.speed[0]
        if (self.rect.bottom >= SIZE_Y and self.speed[1] > 0) or (self.rect.top <= 0 and self.speed[1] < 0):
            self.speed[1] = -self.speed[1]

def main(genomes, config):

    counter = 0

    sprite_list = pg.sprite.Group()
    bird_list = pg.sprite.Group()
    box_list = pg.sprite.Group()

    nets = []
    ge = []

    #birds = []

    for genome_id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)

        bird = Bird()
        bird.rect.x = random.randrange(50, SIZE_X)
        bird.rect.y = 500
        bird_list.add(bird)
        sprite_list.add(bird)

        g.fitness = 0
        ge.append(g)

    for i in range(10):
        box = Box()
        box.rect.x = random.randrange(SIZE_X)
        box.rect.y = random.randrange(100)
        box.speed = [random.choice([-11, -10, -9 -8, 8, 9, 10, 11]),
                     random.choice([-11, -10, -9 -8, 8, 9, 10, 11])]
        box_list.add(box)
        sprite_list.add(box)

    START = time.time()
    while True and len(bird_list) > 0:
        surface.fill(WHITE)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()


        keys = pg.key.get_pressed()  #checking pressed keys

        bird.moving(keys)

        # for a in box_list:
        #     print(a.rect.x)
        #     print("##########")

        for x, bi in enumerate(bird_list):
            #bi.moving()
            ge[x].fitness += 0.01

            out = [bi.rect.x, bi.rect.y]
            out.extend([i.rect.x for i in box_list])
            out.extend([i.rect.y for i in box_list])
            #print("out", out)
            output = nets[x].activate(out)

            if output[0] > 0.5:
                bi.moving("W")
            if output[1] > 0.5:
                bi.moving("S")
            if output[2] > 0.5:
                bi.moving("D")
            if output[3] > 0.5:
                bi.moving("A")

        for box in box_list:
            box.moving()

        # detect if boxes hit by bird
        to_kill = []
        for b in box_list:
            for x, bi in enumerate(bird_list):
                if pg.sprite.collide_rect(b, bi):
                    ge[x].fitness -= 1

                    to_kill.append(x)

                    # nets.pop(x)
                    # ge.pop(x)
                    pg.sprite.Sprite.kill(bi)

        new_ge = []
        for i in ge:
            if ge.index(i) not  in to_kill:
                new_ge.append(i)


                END = time.time()

                #time.sleep(1)

                # GAME OVER STATE
                #game_over(START, END)

        counter += 1
        if counter == 200:
            for g in ge:
                g.fitness += 5
            counter = 0

        sprite_list.draw(surface)

        pg.display.update()
        fpsClock.tick(30)

def game_over(START, END):
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()

        if keys[K_RETURN] or keys[K_SPACE]:
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
        fpsClock.tick(60)

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,100)
    print('\nBest genome:\n{!s}'.format(winner))
    pickle.dump(winner, f"{time.time()}.pickle")


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "conf_NEAT_survive.txt")
    run(config_path)