from pygame import*
from const import*
from game_sprite import GameSprite
from bullet import Bullet


class Player(GameSprite):
    def __init__(self, img, x, y, size, speed=9, hp=5):
        super().__init__(img, x, y, size)
        self.speed = speed
        self.hp = hp
        self.missed = 0
        self.points = 0
        self.bullets = sprite.Group()

    def update(self, left, right):
        keys_pressed = key.get_pressed()
        if keys_pressed[left] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[right] and self.rect.x < WIN_W - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(BULLET_IMG, self.rect.centerx, self.rect.y, (BULLET_W, BULLET_H))
        self.bullets.add(bullet)