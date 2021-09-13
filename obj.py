import pygame


class Obj(pygame.sprite.Sprite):

    def __init__(self, img, x, y, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y


class Pipe(Obj):

    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)

    def update(self, *args):
        self.move()

    def move(self):
        self.rect[0] -= 2

        if self.rect[0] <= -100:
            self.kill()


class Coin(Obj):

    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)

        self.ticks = 0

    def update(self, *args):
        self.move()
        self.anim()

    def move(self):
        self.rect[0] -= 2

        if self.rect[0] <= -100:
            self.kill()

    def anim(self):
        self.ticks = (self.ticks + 1) % 6
        self.image = pygame.image.load(f"assets/{self.ticks}.png")


class Bird(Obj):

    def __init__(self, img, x, y, *groups):
        super().__init__(img, x, y, *groups)

        self.ticks = 0
        self.speed = 4
        self.gravity = 1

        self.pts = 0

        self.play = True

    def update(self, *args):

        self.anim()
        self.move()

    def anim(self):

        self.ticks = (self.ticks + 1) % 4
        self.image = pygame.image.load(f"assets/bird{self.ticks}.png")

    def move(self):

        key = pygame.key.get_pressed()

        self.speed += self.gravity
        self.rect[1] += self.speed

        if self.speed >= 10:
            self.speed = 10

        if key[pygame.K_SPACE]:
            self.speed -= 5

        if self.rect[1] >= 440:
            self.rect[1] = 440
        elif self.rect[1] <= 0:
            self.rect[1] = 0
            self.speed = 4

    def colliding_pipes(self, group):

        col = pygame.sprite.spritecollide(self, group, False)

        if col:
            self.play = False

    def colliding_coins(self, group):

        col = pygame.sprite.spritecollide(self, group, True)

        if col:
            self.pts += 1


class Text:

    def __init__(self, size, text):
        self.font = pygame.font.Font("assets/font/font.ttf", size)
        self.render = self.font.render(text, True, (255, 255, 255))

    def draw(self, window, x, y):
        window.blit(self.render, (x, y))

    def text_update(self, text):
        self.render = self.font.render(text, True, (255, 255, 255))
