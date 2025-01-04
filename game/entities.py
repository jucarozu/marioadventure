"""Módulo que contiene las clases de las entidades del juego."""

import pygame as pg
import random as rd

from settings import *

class Player(pg.sprite.Sprite):
    """Representa al jugador."""

    def __init__(self):
        """Inicializa al jugador."""

        super().__init__()

        self.image = pg.image.load("./game/res/images/player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        """Actualiza la posición del jugador."""

        self.rect.x += self.speed_x

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        """Dispara una bala."""

        return Bullet(self.rect.centerx, self.rect.top)

class Enemy(pg.sprite.Sprite):
    """Representa a un enemigo."""

    def __init__(self):
        """Inicializa al enemigo."""

        super().__init__()

        self.image = pg.image.load("./game/res/images/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = rd.randrange(WIDTH - self.rect.width)
        self.rect.y = rd.randrange(-100, -40)
        self.speed_y = rd.randrange(1, 5)

    def update(self):
        """Actualiza la posición del enemigo."""

        self.rect.y += self.speed_y

        if self.rect.top > HEIGHT + 10:
            self.rect.x = rd.randrange(WIDTH - self.rect.width)
            self.rect.y = rd.randrange(-100, -40)
            self.speed_y = rd.randrange(1, 5)

class Bullet(pg.sprite.Sprite):
    """Representa una bala."""

    def __init__(self, x, y):
        """Inicializa la bala."""

        super().__init__()

        self.image = pg.image.load("./game/res/images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        """Actualiza la posición de la bala."""

        self.rect.y += self.speed_y
        
        if self.rect.bottom < 0:
            self.kill()