import tomllib
from typing import NoReturn, Optional, Self

import pygame

from util.sprite.spritesheet import Spritesheet


class Game:
    def __init__(self, static_path: str = 'static') -> Self:
        self.static_path = static_path
        self.score = 0
        self.game_paused = False
        self.game_over = False
        self.load_cfg(f'{self.static_path}/cfg/cfg.toml')
        self.dino_state = 'standing'

    def load_cfg(self, cfg_path: str):
        with open(cfg_path, 'rb') as f:
            cfgs = tomllib.load(f)

        self.TITLE = cfgs['meta']['title']

        self.WIDTH = cfgs['screen']['dimensions']['width']
        self.HEIGHT = cfgs['screen']['dimensions']['height']
        self.SCREEN_SIZE = (self.WIDTH, self.HEIGHT)

        self.BG_COLOR = cfgs['screen']['bg_color']
        self.FPS = cfgs['screen']['fps']

        self.HIGH_SCORE = cfgs['game']['high_score']

    def update(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.game_paused = True

                        case pygame.K_SPACE | pygame.K_UP:
                            self.dino_state = 'jumping'

        match self.dino_state:
            case 'running_1':
                self.dino_state = 'running_2'

            case 'running_2':
                self.dino_state = 'running_1'

    def draw(self):
        self.SCREEN.fill(self.BG_COLOR)
        
        # Draw dino
        dino_data = self.spritesheet.data['dino'][self.dino_state]
        x, y, w, h = dino_data['x'], dino_data['y'], dino_data['width'], dino_data['height']
        dino_sprite = self.spritesheet.get_sprite(x, y, w, h)
        self.SCREEN.blit(dino_sprite, (0, self.HEIGHT // 2))

    def run(self):
        pygame.init()
        self.spritesheet = Spritesheet(f'{self.static_path}/img/spritesheet.png')
        pygame.display.set_caption(self.TITLE)

        self.SCREEN = pygame.display.set_mode(self.SCREEN_SIZE)
        self.CLOCK = pygame.time.Clock()

        while True:
            self.update()
            self.draw()

            pygame.display.flip()
            self.CLOCK.tick(self.FPS)

def main():
    Game().run()

if __name__ == '__main__':
    main()