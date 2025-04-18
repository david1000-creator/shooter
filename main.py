from pygame import *
from const import*
from game_sprite import GameSprite
from player import Player
from enemy import Enemy
# вынесем размер окна в константы для удобства
# W - width, ширина
# H - height, высота
def start():
    rocket = Player(ROCKET_IMG, (WIN_W - ROCKET_W) / 2, WIN_H - ROCKET_H, (ROCKET_W, ROCKET_H))

    ufos = sprite.Group()
    for i in range(UFOS):
        ufo = Enemy(UFO_IMG, WIN_W - 100, 250, (UFO_W, UFO_H))
        ufos.add(ufo)

    rocks = sprite.Group()
    for i in range(ROCKS):
        rock = Enemy(ROCK_IMG, WIN_W - 100, 250, (ROCK_SIZE, ROCK_SIZE))
        rocks.add(rock)
    return rocket, ufos, rocks

# создание окна размером 700 на 500
window = display.set_mode((WIN_W, WIN_H))
# создание таймера
clock = time.Clock()
mixer.init()
mixer.music.load('src/core.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.5)
death = mixer.Sound('src/death.mp3')
win = mixer.Sound('src/win.mp3')

shot = mixer.Sound('src/shot.mp3')
shot.set_volume(0.4)
font.init()
title_font = font.SysFont('comic sans', 71)
lost = title_font.render('Лошара', True, RED)
won = title_font.render('Молодец :)', True, GREEN)

label_font = font.SysFont('comic sans', 29)
points_txt = label_font.render('Убито:', True, WHITE)
missed_txt = label_font.render('Пропущено:', True, WHITE)


# название окна
display.set_caption("shooter")

# задать картинку фона такого же размера, как размер окна
background = GameSprite(BG_IMG, 0, 0,  (WIN_W, WIN_H))
rocket, ufos, rocks = start()
# игровой цикл
game = True
finish = False
while game:
    if not finish:
        background.draw(window)
        points = label_font.render(str(rocket.points), True, WHITE)
        missed = label_font.render(str(rocket.missed), True, WHITE)

        window.blit(points_txt, (10, 10))
        window.blit(points, (101, 10))
        window.blit(missed_txt, (10, 50))
        window.blit(missed, (186, 50))

        rocket.draw(window)
        ufos.draw(window)
        rocket.bullets.draw(window)
        rocks.draw(window)
        rocket.update(K_a, K_d)
        ufos.update(rocket)
        rocket.bullets.update()
        rocks.update(rocket, True)

        if sprite.spritecollide(rocket, ufos, True):
            death.play()
            rocket.hp -= 1
            ufo = Enemy(UFO_IMG, WIN_W - 100, 250, (UFO_W, UFO_H))
            ufos.add(ufo)

        if rocket.hp <= 0 or rocket.missed >= MAX_MISSED or sprite.spritecollide(rocket, rocks, False):
            death.play()
            window.blit(lost, (250, 200))
            finish = True

        for s in sprite.groupcollide(rocket.bullets, ufos, True, True):
            rocket.points += 1
            ufo = Enemy(UFO_IMG, WIN_W - 100, 250, (UFO_W, UFO_H))
            ufos.add(ufo)

        if rocket.points >= KILL_COUNT:
            win.play()
            window.blit(won, (150, 200))
            finish = True
    else:
        for bullet in rocket.bullets:
            bullet.kill()
        rocket.kill()
        for ufo in ufos:
            ufo.kill()
        for rock in rocks:
            rock.kill()
        time.delay(2500)
        rocket, ufos, rocks = start()
        finish = False
    # слушать события и обрабатывать
    for e in event.get():
        # выйти, если нажат "крестик"
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            shot.play()
            rocket.shoot()
    # обновить экран, чтобы отобрзить все изменения
    display.update()
    clock.tick(FPS)