import pygame


class Stake(pygame.sprite.Sprite):
    spritesheet = pygame.image.load("./static/levels/Sprites/stake.png")
    NBIMAGES = 19
    TEMPSPAUSE = 5000

    def __init__(self, FPS, playing_field, obstacles):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.image = Stake.spritesheet.subsurface(pygame.Rect(0, 0, 16, 80))
        self.rect = pygame.Rect(0, 0, 16, 80)
        self.rect.bottom = 80

        self.img_next = 0
        self.inc = 0

        self.time_dt = 0
        self.time_dt_next = 0
        self.FPS = FPS

    def update(self, time):
        self.time_dt = self.time_dt + time
        self.time_dt_next = self.time_dt_next + time

        if (self.time_dt_next > self.TEMPSPAUSE):
            self.time_dt_next = 0
            self.inc = 1

        if self.time_dt >= 50:
            self.time_dt = 0

            self.image = Stake.spritesheet.subsurface(
                pygame.Rect(self.img_next*16, 0, 16, 80))

            self.img_next = self.img_next+self.inc
            if (self.img_next < 0):
                self.img_next = 0
                self.inc = 0
            elif (self.img_next >= self.NBIMAGES):
                self.img_next = self.NBIMAGES-1
                self.inc = -self.inc

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 16)

    def get_position(self):
        return self.rect

    def has_collided(self):
        return

    def has_died(self):
        return False
