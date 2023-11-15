import math
import random

import pygame


class Boo(pygame.sprite.Sprite):
    obstacles = []
    playing_field = pygame.Rect((0, 0), (0, 0))

    spritesheet = pygame.image.load("./levels/Sprites/boo.png")
    sequences = [(0, 2, True, False), (2, 2, True, False),
                 (4, 2, True, False), (6, 4, False, True)]

    def __init__(self, FPS, playing_field, obstacles):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.image = Boo.spritesheet.subsurface(pygame.Rect(0, 0, 16, 16))
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.bottom = 16

        self.initialrect = pygame.Rect(0, 0, 16, 16)
        self.initialrect.bottom = 16

        self.curr_direction = 3
        self.dead = False

        self.next_num = 1
        self.img_next = 0
        self.flip = True

        self.time_dt = 0
        self.speed = int(round(120/FPS))

        self.playing_field = playing_field
        self.obstacles = obstacles

        self.incangle = 2
        self.angle = random.randint(0, 359)
        self.radius_x = 100
        self.radius_y = 50

    def update(self, time):
        self.time_dt = self.time_dt + time

        if self.time_dt >= 100:
            self.time_dt = 0

            self.angle += self.incangle
            self.angle = self.angle % 360

            incx = math.cos(self.angle*2*3.14/360)*self.radius_x
            incy = math.sin(self.angle*2*3.14/360)*self.radius_y

            self.rect = pygame.Rect(
                self.initialrect.x+incx, self.initialrect.y+incy, 16, 16)
            if self.angle > 0 and self.angle < 180:
                self.flip = True
            else:
                self.flip = False

            n = Boo.sequences[self.next_num][0]+self.img_next
            self.image = Boo.spritesheet.subsurface(
                pygame.Rect(n % 20*16, n//20*32, 16, 16))
            if self.flip:
                self.image = pygame.transform.flip(self.image, True, False)

            self.img_next = self.img_next+1

            if self.img_next == Boo.sequences[self.next_num][1]:
                if Boo.sequences[self.next_num][3]:
                    self.dead = True
                if Boo.sequences[self.next_num][2]:
                    self.img_next = 0
                else:
                    self.img_next = self.img_next-1

    def set_sequence(self, n):
        if self.next_num != n:
            self.img_next = 0
            self.next_num = n

    def kill(self):
        self.curr_direction = 0
        self.set_sequence(3)

    def has_died(self):
        return self.dead

    def has_collided(self):
        self.kill()

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.initialrect = pygame.Rect(x, y, 16, 16)

    def get_position(self):
        return self.rect

    def get_direction(self):
        return self.curr_direction
