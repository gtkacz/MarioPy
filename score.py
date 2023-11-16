import pygame


class Score(pygame.sprite.Sprite):
    spritesheet = pygame.image.load("./static/levels/Sprites/digits.png")

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.spritesheet.convert_alpha()

        self.image = pygame.Surface((52*3, 52))

        self.rect = pygame.Rect(0, 0, 52, 52)
        self.rect.bottom = 52

        self.score = 0
        self.counter = 0

        self.time_dt = 0

    def update(self, time):
        unite = self.counter % 10
        dizaine = (self.counter//10) % 10
        centaine = (self.counter//100) % 10

        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 52*3, 52))
        digit = Score.spritesheet.subsurface(
            pygame.Rect(centaine*52, 0, 52, 52))
        self.image.blit(digit, (0, 0))
        digit = Score.spritesheet.subsurface(
            pygame.Rect(dizaine*52, 0, 52, 52))
        self.image.blit(digit, (52, 0))
        digit = Score.spritesheet.subsurface(pygame.Rect(unite*52, 0, 52, 52))
        self.image.blit(digit, (104, 0))

        self.time_dt = self.time_dt + time
        if self.time_dt >= 100:
            self.time_dt = 0

            if (self.counter < self.score):
                self.counter = self.counter + 1

    def set_position(self, x, y):
        self.rect = pygame.Rect(x, y, 52*3, 52)

    def get_position(self):
        return self.rect

    def set_score(self, number):
        self.score = number

    def get_score(self):
        return self.score

    def increment_score(self, val):
        self.score += val
        return self.score

    def subtract_score(self, val):
        self.score -= val
        return self.score
