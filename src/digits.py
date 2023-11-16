import pygame


class Digits(pygame.sprite.Sprite):
    spritesheet = pygame.image.load("./static/levels/Sprites/digits.png")

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.image = Digits.spritesheet.subsurface(pygame.Rect(0, 0, 52, 52))
        self.rect = pygame.Rect(0, 0, 52, 52)
        self.rect.bottom = 52
        self.img_next = 0

    def update(self, time):
        index = self.img_next
        if (index < 0):
            index = 0
        if (index > 9):
            index = 9
        self.image = Digits.spritesheet.subsurface(
            pygame.Rect(index*52, 0, 52, 52))

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 16, 16)

    def get_position(self):
        return self.rect

    def set_digit(self, number):
        self.img_next = number

    def get_digit(self):
        return self.img_next

    def increment_digit(self):
        self.img_next += 1
        return self.img_next

    def decrease_digit(self):
        self.img_next -= 1
        return self.img_next
