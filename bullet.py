from game_sprite import*


class Bullet(GameSprite):
    def __init__(self, img, x, y, size, speed=3):
        super().__init__(img, x, y, size)
        self.speed = speed

    def update(self):
        if self.rect.y <= 0:
            self.kill()
        self.rect.y -= self.speed
