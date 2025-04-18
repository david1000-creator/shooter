from pygame import*
from game_sprite import*
from random import randint
from const import WIN_H, WIN_W


class Enemy(GameSprite):
    def __init__(self, img, x, y, size, speed=3):
        super().__init__(img, x, y, size)
        self.speed = speed
        self.rect.x = randint(0, WIN_W - size[0])
        self.rect.y = randint(0, WIN_H * 0.1)

    def update(self, player, skippable=False):
        if self.rect.y >= WIN_H:
            if not skippable:
                player.missed += 1
            self.rect.x = randint(0, WIN_W - self.rect.width)
            self.rect.y = randint(0, WIN_H * 0.1)
        self.rect.y += self.speed