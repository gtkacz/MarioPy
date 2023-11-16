import pygame
import pytmx

from src.boo import Boo
from src.digits import Digits
from src.gameobject import GameObject
from src.koopa import Koopa
from src.mario import Mario
from src.poisonivy import PoisonIvy
from src.score import Score
from src.stake import Stake
from src.water import Water


def main():
    def add_obj(layer, obj):
        layer = tm.get_layer_by_name(layer)

        for x, y, image in layer.tiles():
            obj = GameObject(FPS)
            obj.set_sequence(obj)
            obj.set_position(x*8, y*8-8)
            objs.append(obj)

    WIDTH = 640
    HEIGHT = 432
    FPS = 60
    MUSIC = True
    MAX_LIFE = 9
    TITLE = "Mario Py"

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT), pygame.DOUBLEBUF, vsync=1)
    pygame.display.set_caption(TITLE)

    tm = pytmx.load_pygame('static/levels/level1.tmx')
    tilewidth = tm.tilewidth
    tileheight = tm.tileheight
    playing_field = pygame.Rect(
        (0, 0), (tm.width*tilewidth, tm.height*tileheight))

    while True:
        position = 0
        last_x = 2
        counter = 0

        if MUSIC:
            pygame.mixer.music.load('static/soundtracks/01 - Super Mario Bros.mp3')

        obstacles = []
        obstacle_layer = tm.get_layer_by_name("obstacles")
        for object in obstacle_layer:
            obstacles.append(pygame.Rect(object.x, object.y,
                                         object.width, object.height))

        dead_zones = []
        deadzone = tm.get_layer_by_name("dead")
        for dead in deadzone:
            dead_zones.append(pygame.Rect(
                dead.x, dead.y, dead.width, dead.height))

        end_layers = []
        endl = tm.get_layer_by_name("end")
        for end in endl:
            end_layers.append(pygame.Rect(end.x, end.y, end.width, end.height))

        objs = []
        add_obj("yellow", GameObject.YELLOW)
        add_obj("silver", GameObject.SILVER)
        add_obj("questionbox", GameObject.QUESTIONBOX)
        add_obj("box", GameObject.BOX)
        add_obj("apple", GameObject.APPLE)
        add_obj("apple3", GameObject.APPLE3)
        add_obj("apple2", GameObject.APPLE2)
        add_obj("music", GameObject.MUSIC)

        watersprites = []
        layer = tm.get_layer_by_name("water")
        for x, y, image in layer.tiles():
            w = Water(FPS)
            w.set_position(x*8, y*8-40)
            watersprites.append(w)

        opps = []

        stake_layer = tm.get_layer_by_name("stake")
        for x, y, image in stake_layer.tiles():
            stake = Stake(FPS, playing_field, obstacles)
            stake.set_position(x*8, y*8-72)
            opps.append(stake)

        koopas_layer = tm.get_layer_by_name("koopas")
        for x, y, image in koopas_layer.tiles():
            koopa = Koopa(FPS, playing_field, obstacles)
            koopa.set_position(x*8, y*8-24)
            opps.append(koopa)

        boo_layer = tm.get_layer_by_name("boo")
        for x, y, image in boo_layer.tiles():
            boo = Boo(FPS, playing_field, obstacles)
            boo.set_position(x*8, y*8-8)
            opps.append(boo)

        ivy_layer = tm.get_layer_by_name("poisonivy")
        for x, y, image in ivy_layer.tiles():
            poisonivy = PoisonIvy(FPS, playing_field, obstacles)
            poisonivy.set_position(x*8, y*8-8)
            opps.append(poisonivy)

        mario = Mario(FPS, playing_field, obstacles)
        marioposition = tm.get_object_by_name("mario")
        mario.set_position(marioposition.x, marioposition.y)

        health = Digits()
        health.set_position(WIDTH-52-20, 14)
        health.set_digit(MAX_LIFE)

        score = Score()
        score.set_position(0, 14)
        score.set_score(0)

        pygame.mouse.set_visible(False)

        if MUSIC:
            pygame.mixer.music.play(loops=-1)

        home_img = pygame.image.load("static/splashscreens/principal.png").convert()
        (w, h) = pygame.display.get_surface().get_size()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, w, h))
        (iw, ih) = home_img.get_size()
        screen.blit(home_img, ((w-iw)/2, (h-ih)/2))

        clock = pygame.time.Clock()
        main_screen = True
        while main_screen:
            time = clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                    elif event.key == pygame.K_SPACE:
                        main_screen = False

            pygame.display.flip()

        header = pygame.image.load("static/splashscreens/mariopy.png").convert_alpha()

        levelfinished = False
        clock = pygame.time.Clock()
        while not levelfinished and health.get_digit() > 0:
            time = clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                    elif event.key == pygame.K_LEFT:
                        mario.move_left()
                    elif event.key == pygame.K_RIGHT:
                        mario.move_right()
                    elif event.key == pygame.K_SPACE:
                        mario.jump()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        mario.stopl()
                    elif event.key == pygame.K_RIGHT:
                        mario.stopr()

            mario.update(time)

            for w in watersprites:
                w.update(time)

            for opp in opps:
                opp.update(time)

            for obj in objs:
                obj.update(time)

            if mario.rect.collidelist(dead_zones) != -1:
                health.set_digit(0)

            if mario.rect.collidelist(end_layers) != -1:
                levelfinished = True

            collided_obj = pygame.sprite.spritecollideany(mario, objs)
            if collided_obj:
                collided_obj.collision()
                score.increment_score(collided_obj.fetch_reward())
                objs.remove(collided_obj)

            collision_opp = pygame.sprite.spritecollideany(
                mario, opps, pygame.sprite.collide_mask)
            if collision_opp:
                if mario.injured():
                    collision_opp.has_collided()
                    health.decrease_digit()
                    if health.get_digit() == 1:
                        if MUSIC:
                            pygame.mixer.music.load(
                                'static/soundtracks/03 - Hurry - Super Mario Bros.mp3')
                            pygame.mixer.music.play(loops=-1)

            for opp in opps:
                if opp.has_died():
                    opps.remove(opp)

            health.update(time)
            score.update(time)

            counter += 1

            mariopositionx = mario.get_position().x
            if (mariopositionx-position < 200):
                vel_x = -last_x
            elif (mariopositionx-position > WIDTH-200):
                vel_x = last_x
            else:
                vel_x = 0

            position = position + vel_x

            if position < 0:
                position = 0
            if position > playing_field.width-WIDTH:
                position = playing_field.width-WIDTH

            mario_pos = mario.get_position()
            if mario_pos.x < position:
                mario.set_position(position, mario_pos.y)
            if mario_pos.x+mario_pos.width >= position+WIDTH:
                mario.set_position(
                    position+WIDTH-mario_pos.width, mario_pos.y)

            buffer = pygame.Surface(
                (playing_field.width, playing_field.height))

            layer = tm.get_layer_by_name("fond")
            for x, y, image in layer.tiles():
                buffer.blit(image, (x*8+position/2, y*8))

            layer = tm.get_layer_by_name("trees")
            for x, y, image in layer.tiles():
                buffer.blit(image, (x*8+position/4, y*8))

            layer = tm.get_layer_by_name("clouds")
            for x, y, image in layer.tiles():
                buffer.blit(image, (x*8+position/2-counter/16, y*8))

            layer = tm.get_layer_by_name("plateau")
            for x, y, image in layer.tiles():
                buffer.blit(image, (x*8, y*8))

            for obj in objs:
                buffer.blit(obj.image, obj.rect)

            for opp in opps:
                buffer.blit(opp.image, opp.rect)

            buffer.blit(mario.image, mario.rect)

            for w in watersprites:
                buffer.blit(w.image, w.rect)

            layer = tm.get_layer_by_name("plateaufront")
            for x, y, image in layer.tiles():
                buffer.blit(image, (x*8, y*8))

            pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, 81))
            screen.blit(header, (180, 14))
            screen.blit(health.image, health.rect)
            screen.blit(score.image, score.rect)

            screen.blit(buffer, (-position, 80))

            pygame.display.flip()

        if levelfinished:
            winner = pygame.image.load(
                "static/splashscreens/winner.png").convert_alpha()
            (winnerWidth, winnerHeight) = winner.get_size()
            screen.blit(winner, pygame.Rect((WIDTH-winnerWidth)/2, 80 +
                        (HEIGHT-winnerHeight)/2, winnerWidth, winnerHeight))
            if MUSIC:
                pygame.mixer.music.load('static/soundtracks/04 - Area Clear.mp3')
                pygame.mixer.music.play()
        else:
            gameover = pygame.image.load(
                "static/splashscreens/game over.png").convert_alpha()
            (finalw, finalh) = gameover.get_size()
            screen.blit(gameover, pygame.Rect((WIDTH-finalw)/2,
                        80+(HEIGHT-finalh)/2, finalw, finalh))
            if MUSIC:
                pygame.mixer.music.load('static/soundtracks/16 - Game Over.mp3')
                pygame.mixer.music.play()

        pygame.display.flip()

        clock = pygame.time.Clock()
        main_screen = True
        while main_screen:
            time = clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit
                    elif event.key == pygame.K_SPACE:
                        main_screen = False


if __name__ == "__main__":
    main()
