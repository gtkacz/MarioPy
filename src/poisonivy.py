import pygame


class PoisonIvy(pygame.sprite.Sprite):
    YELLOW = 0
    SILVER = 1
    QUESTIONBOX = 2
    BOX = 3
    APPLE = 4
    APPLE2 = 5
    APPLE3 = 6
    FLOWER = 7
    MUSIC = 8

    spritesheet = pygame.image.load("./static/levels/Sprites/AnimatedTiles.png")
    sequences = [(0, 4, True), (4, 4, True), (8, 4, True), (12, 4, True),
                 (16, 3, True), (19, 3, True), (22, 3, True), (29, 2, True), (31, 3, True)]

    def __init__(self, FPS, playing_field, obstacles):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.image = PoisonIvy.spritesheet.subsurface(
            pygame.Rect(0, 0, 16, 16))
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.bottom = 16

        self.next_num = 7
        self.img_next = 0

        self.time_dt = 0

    def update(self, time):
        self.time_dt = self.time_dt + time

        if self.time_dt >= 500:
            self.time_dt = 0

            n = PoisonIvy.sequences[self.next_num][0]+self.img_next
            self.image = PoisonIvy.spritesheet.subsurface(
                pygame.Rect(n % 40*16, n//40*16, 16, 16))

            self.img_next = self.img_next+1

            if self.img_next == PoisonIvy.sequences[self.next_num][1]:
                if PoisonIvy.sequences[self.next_num][2]:
                    self.img_next = 0
                else:
                    self.img_next = self.img_next-1

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 16)

    def get_position(self):
        return self.rect

    def has_collided(self):
        return

    def has_died(self):
        return False
