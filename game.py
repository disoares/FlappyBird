import pygame
from obj import Obj, Pipe, Coin, Bird, Text
import random


class Game:

    def __init__(self):

        pygame.font.init()

        self.all_sprites = pygame.sprite.Group()
        self.coins_group = pygame.sprite.Group()
        self.pipes_group = pygame.sprite.Group()

        self.background = Obj("assets/sky.png", 0, 0, self.all_sprites)
        self.background2 = Obj("assets/sky.png", 360, 0, self.all_sprites)
        self.ground = Obj("assets/ground.png", 0, 480, self.all_sprites)
        self.ground2 = Obj("assets/ground.png", 360, 480, self.all_sprites)

        self.bird = Bird("assets/bird1.png", 50, 320, self.all_sprites)

        self.score = Text(100, "0")

        self.change_scene = False

        self.ticks = 0
        self.timer = 0

        self.max_score = 0
        self.check_score()

    def draw(self, window):
        self.all_sprites.draw(window)
        self.score.draw(window, 150, 50)

    def update(self):
        self.move_bg()
        self.move_ground()
        if self.bird.play:
            self.spawn_pipes()
            self.bird.colliding_coins(self.coins_group)
            self.bird.colliding_pipes(self.pipes_group)
            self.all_sprites.update()
            self.score.text_update(str(self.bird.pts))
        else:
            self.save_score()
            self.game_over()

    def move_bg(self):

        self.background.rect[0] -= 2
        self.background2.rect[0] -= 2

        if self.background.rect[0] <= -360:
            self.background.rect[0] = 0
        if self.background2.rect[0] <= 0:
            self.background2.rect[0] = 360

    def move_ground(self):

        self.ground.rect[0] -= 3
        self.ground2.rect[0] -= 3

        if self.ground.rect[0] <= -360:
            self.ground.rect[0] = 0
        if self.ground2.rect[0] <= 0:
            self.ground2.rect[0] = 360

    def spawn_pipes(self):
        self.ticks += 1

        if self.ticks >= random.randrange(120, 150):
            self.ticks = 0
            pipe = Pipe("assets/pipe1.png", 360, random.randrange(300, 450), self.all_sprites, self.pipes_group)
            pipe2 = Pipe("assets/pipe2.png", 360, pipe.rect[1] - 550, self.all_sprites, self.pipes_group)
            coin = Coin("assets/0.png", 388, pipe.rect[1] - 120, self.all_sprites, self.coins_group)

    def game_over(self):
        self.timer += 1

        if self.timer >= 30:
            self.change_scene = True

    def save_score(self):
        if self.bird.pts > self.max_score:
            self.max_score = self.bird.pts

            file = open("save.txt", "w")
            file.write(str(self.max_score))
            file.close()

    def check_score(self):
        file = open("save.txt", "r")
        self.max_score = int(file.read())
        file.close()