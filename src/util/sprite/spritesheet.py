import json
from typing import Self

import pygame


class Spritesheet:
    def __init__(self, filename: str, color_key: tuple[int, int, int] = (255, 255, 255)) -> Self:
        self.color_key = color_key
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = filename.replace('png', 'json')

        with open(self.meta_data) as f:
            self.data = json.load(f)

    def get_sprite(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey(self.color_key)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        return sprite

    def parse_sprite(self, name: str) -> pygame.Surface:
        sprite = self.data[name]
        x, y, w, h = sprite['x'], sprite['y'], sprite['width'], sprite['height']

        return self.get_sprite(x, y, w, h)
