import pygame


class Koopa(pygame.sprite.Sprite):
    curr_direction = 3

    prev_position = pygame.Rect((0, 0), (0, 0))

    obstacles = []
    playing_field = pygame.Rect((0, 0), (0, 0))

    spritesheet = pygame.image.load("./static/levels/Sprites/Turtle.png")
    sequences = [(0, 1, False, False), (1, 2, True, False), (3, 4, False, True),
                 (7, 2, True, False), (9, 2, True, False), (10, 1, False, False)]

    dead = False

    color = 0

    def __init__(self, FPS, playing_field, obstacles):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.image = Koopa.spritesheet.subsurface(pygame.Rect(0, 0, 16, 32))
        self.rect = pygame.Rect(0, 0, 16, 32)
        self.rect.bottom = 32

        self.next_num = 1
        self.img_next = 0
        self.flip = True

        self.time_dt = 0
        self.speed = int(round(120/FPS))

        self.playing_field = playing_field
        self.obstacles = obstacles

    def update(self, time):
        self.time_dt = self.time_dt + time

        if self.time_dt >= 100:
            self.time_dt = 0

            self.prev_position = pygame.Rect(
                self.rect.x, self.rect.y, self.rect.width, self.rect.height)

            if self.curr_direction == 2:  # en haut a droite
                self.rect = self.rect.move(
                    self.speed, -self.speed).clamp(self.playing_field)
                self.flip = False
            elif self.curr_direction == 3:  # a droite
                self.rect = self.rect.move(
                    self.speed, 0).clamp(self.playing_field)
                self.flip = False
            elif self.curr_direction == 4:  # en bas a droite
                self.rect = self.rect.move(
                    self.speed, self.speed).clamp(self.playing_field)
                self.flip = False
            elif self.curr_direction == 5:  # en bas
                self.rect = self.rect.move(
                    0, self.speed).clamp(self.playing_field)
                self.flip = False
            elif self.curr_direction == 6:  # en bas a gauche
                self.rect = self.rect.move(-self.speed,
                                           self.speed).clamp(self.playing_field)
                self.flip = True
            elif self.curr_direction == 7:  # a gauche
                self.rect = self.rect.move(-self.speed,
                                           0).clamp(self.playing_field)
                self.flip = True
            elif self.curr_direction == 8:  # en haut a gauche
                self.rect = self.rect.move(-self.speed, -
                                           self.speed).clamp(self.playing_field)
                self.flip = True
            elif self.curr_direction == 1:  # en haut
                self.rect = self.rect.move(
                    0, -self.speed).clamp(self.playing_field)
                self.flip = True

            if self.rect.collidelist(self.obstacles) != -1:
                self.collision()

            if self.rect.move(0, 2).collidelist(self.obstacles) == -1:
                self.rect = self.rect.move(0, 2).clamp(self.playing_field)
            elif self.rect.move(0, 1).collidelist(self.obstacles) == -1:
                self.rect = self.rect.move(0, 1).clamp(self.playing_field)

            n = Koopa.sequences[self.next_num][0]+self.img_next
            self.image = Koopa.spritesheet.subsurface(
                pygame.Rect(n % 20*16, self.color*32+n//20*32, 16, 32))
            if self.flip:
                self.image = pygame.transform.flip(self.image, True, False)

            self.img_next = self.img_next+1

            if self.img_next == Koopa.sequences[self.next_num][1]:
                if Koopa.sequences[self.next_num][3]:
                    self.dead = True
                if Koopa.sequences[self.next_num][2]:
                    self.img_next = 0
                else:
                    self.img_next = self.img_next-1

    def set_sequence(self, n):
        if self.next_num != n:
            self.img_next = 0
            self.next_num = n

    def move_right(self):
        self.curr_direction = 3
        self.set_sequence(1)

    def stopr(self):
        self.curr_direction = 0
        self.set_sequence(0)

    def move_left(self):
        self.curr_direction = 7
        self.set_sequence(1)

    def stopl(self):
        self.curr_direction = 0
        self.set_sequence(0)

    def kill(self):
        self.curr_direction = 0
        self.set_sequence(2)

    def has_died(self):
        return self.dead

    def has_collided(self):
        self.changeDirection()

    def collision(self):
        self.rect = pygame.Rect(self.prev_position.x, self.prev_position.y,
                                self.prev_position.width, self.prev_position.height)
        self.changeDirection()

    def changeDirection(self):
        if self.curr_direction == 3:
            self.curr_direction = 7
        elif self.curr_direction == 7:
            self.curr_direction = 3

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 32)

    def get_position(self):
        return self.rect

    def get_bottom(self):
        return pygame.Rect((self.rect.x, self.rect.y+32), (self.rect.width, 1))

    def get_direction(self):
        return self.curr_direction

    def setColor(self, color):
        self.color = color
