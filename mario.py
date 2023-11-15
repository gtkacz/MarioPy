import pygame


class Mario(pygame.sprite.Sprite):
    curr_direction = 0
    is_jumpings = False
    is_injured = False

    vel_x = 0
    vel_y = 0
    acl_x = 0
    acl_y = 0
    prev_position = pygame.Rect((0, 0), (0, 0))

    obstacles = []
    playing_field = pygame.Rect((0, 0), (0, 0))

    spritesheet = pygame.image.load("./levels/Sprites/Mario.png")
    sequences = [(0, 1, False), (1, 1, False), (2, 1, False),
                 (3, 3, True), (6, 1, False), (7, 1, False)]

    def __init__(self, FPS, playing_field, obstacles):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.sonSaut = pygame.mixer.Sound("sounds/saut.wav")

        self.image = Mario.spritesheet.subsurface(pygame.Rect(0, 0, 16, 32))
        self.rect = pygame.Rect(0, 0, 16, 32)
        self.rect.bottom = 32

        self.next_num = 0
        self.img_next = 0
        self.flip = True

        self.time_dt = 0
        self.speed = int(round(160/FPS))

        self.playing_field = playing_field
        self.obstacles = obstacles

    def update(self, time):
        self.time_dt = self.time_dt + time

        self.prev_position = pygame.Rect(
            self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if self.curr_direction == 2:
            self.rect = self.rect.move(
                self.speed, -self.speed).clamp(self.playing_field)
            self.flip = True
        elif self.curr_direction == 3:
            self.rect = self.rect.move(self.speed, 0).clamp(self.playing_field)
            self.flip = True
        elif self.curr_direction == 4:
            self.rect = self.rect.move(
                self.speed, self.speed).clamp(self.playing_field)
            self.flip = True
        elif self.curr_direction == 5:
            self.rect = self.rect.move(0, self.speed).clamp(self.playing_field)
            self.flip = True
        elif self.curr_direction == 6:
            self.rect = self.rect.move(-self.speed,
                                       self.speed).clamp(self.playing_field)
            self.flip = False
        elif self.curr_direction == 7:
            self.rect = self.rect.move(-self.speed, 0).clamp(self.playing_field)
            self.flip = False
        elif self.curr_direction == 8:
            self.rect = self.rect.move(-self.speed, -
                                       self.speed).clamp(self.playing_field)
            self.flip = False
        elif self.curr_direction == 1:
            self.rect = self.rect.move(0, -self.speed).clamp(self.playing_field)
            self.flip = True

        self.rect = self.rect.move(
            self.vel_x, self.vel_y).clamp(self.playing_field)
        self.vel_x += self.acl_x
        self.vel_y += self.acl_y

        if self.rect.collidelist(self.obstacles) != -1:
            self.collision()

        if not self.get_isjumping():
            for i in range(0, 4):
                if self.rect.move(0, 1).collidelist(self.obstacles) == -1:
                    self.rect = self.rect.move(0, 1).clamp(self.playing_field)
                else:
                    break

        if self.time_dt >= 50:
            self.time_dt = 0
            n = Mario.sequences[self.next_num][0]+self.img_next
            self.image = Mario.spritesheet.subsurface(
                pygame.Rect(n % 64*16, n//64*32, 16, 32))
            if self.flip:
                self.image = pygame.transform.flip(self.image, True, False)

            self.img_next = self.img_next+1

            if self.img_next == Mario.sequences[self.next_num][1]:
                if Mario.sequences[self.next_num][2]:
                    self.img_next = 0
                else:
                    self.img_next = self.img_next-1

    def set_sequence(self, n):
        if self.next_num != n:
            self.img_next = 0
            self.next_num = n

    def move_right(self):
        self.curr_direction = 3
        self.set_sequence(3)

    def stopr(self):
        self.curr_direction = 0
        self.set_sequence(0)

    def jump(self):
        if not self.is_jumpings:
            self.is_jumpings = True
            self.vel_y = -12
            self.acl_y = 1.5
            self.set_sequence(4)

    def injured(self):
        if not self.is_injured:
            self.is_injured = True
            self.is_jumpings = True
            self.vel_y = -6
            self.acl_y = 0.5
            self.set_sequence(5)
            self.sonSaut.play()
            return True
        else:
            return False

    def move_left(self):
        self.curr_direction = 7
        self.set_sequence(3)

    def stopl(self):
        self.curr_direction = 0
        self.set_sequence(0)

    def collision(self):
        self.rect = pygame.Rect(self.prev_position.x, self.prev_position.y,
                                self.prev_position.width, self.prev_position.height)

        if self.is_jumpings:
            self.vel_x = 0
            self.acl_x = 0
            self.vel_y = 0
            self.acl_y = 0
            self.is_jumpings = False
            if self.curr_direction == 0:
                self.set_sequence(0)
            else:
                self.set_sequence(3)

        self.is_injured = False

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 32)

    def get_position(self):
        return self.rect

    def get_bottom(self):
        return pygame.Rect((self.rect.x, self.rect.y+32), (self.rect.width, 1))

    def get_direction(self):
        return self.curr_direction

    def get_isjumping(self):
        return self.is_jumpings
