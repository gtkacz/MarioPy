import pygame


class Water(pygame.sprite.Sprite):
    MUSIC = 8
    FLOWER = 7
    APPLE3 = 6
    APPLE2 = 5
    APPLE = 4
    BOX = 3
    QUESTIONBOX = 2
    SILVER = 1
    YELLOW = 0

    spritesheet = pygame.image.load("./static/levels/Sprites/water.png")

    sequences = [(0, 4, True)]

    def __init__(self, FPS):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.image = Water.spritesheet.subsurface(pygame.Rect(0, 0, 16, 48))
        self.rect = pygame.Rect(0, 0, 16, 48)
        self.rect.bottom = 48

        self.next_num = 0
        self.img_next = 0

        self.time_dt = 0
        self.speed = int(round(200/FPS))

    def update(self, time):
        self.time_dt = self.time_dt + time

        if self.time_dt >= 200:
            self.time_dt = 0

            n = Water.sequences[self.next_num][0]+self.img_next
            self.image = Water.spritesheet.subsurface(
                pygame.Rect(n % 40*16, n//40*48, 16, 48))

            self.img_next = self.img_next+1

            if self.img_next == Water.sequences[self.next_num][1]:
                if Water.sequences[self.next_num][2]:
                    self.img_next = 0
                else:
                    self.img_next = self.img_next-1

    def set_sequence(self, n):
        if self.next_num != n:
            self.img_next = 0
            self.next_num = n

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 48)

    def get_position(self):
        return self.rect
