import pygame
import random
from constantes import *

pygame.mixer.init()

class Jugador:
    def __init__(self):
        self.imagen = pygame.image.load("navecitaaaaaaa.png")
        self.rect = self.imagen.get_rect()
        self.rect.y = 600
        self.rect.x = 240
        self.centerx = self.rect.centerx
        self.top = self.rect.top

    def draw(self):
        pantalla.blit(self.imagen, self.rect)

    def movimiento(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if self.rect.right > ancho_ventana:
            self.rect.right = ancho_ventana
        if self.rect.left < 0:
            self.rect.left = 0

class Enemigos:
    def __init__(self):
        self.imagen = pygame.image.load("arcade.enemies.final.png").convert_alpha()
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randrange(ancho_ventana - self.rect.width)
        self.rect.y = random.randrange(-50, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
        self.textos = []
        self.disparos_enemigos = []

        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > alto_ventana + 10 or self.rect.left < -25 or self.rect.right > ancho_ventana + 25:
            self.rect.x = random.randrange(ancho_ventana - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)
        if self.rect.left < 0 or self.rect.right > ancho_ventana:
            self.speedx = -self.speedx

        if self.rect.top > alto_ventana + 10:
            self.rect.x = random.randrange(ancho_ventana - self.rect.width)
            self.rect.y = random.randrange(-100, -40)


    def kill(self):
        self.rect.x = random.randrange(ancho_ventana - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)

    def disparar(self):
        disparo = DisparoEnemigo(self.rect.centerx, self.rect.bottom)
        self.disparos_enemigos.append(disparo)

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("02.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill() #utilizo el .kill para eliminar en pantalla un tipo de sprite(en este caso los enemigos)

class DisparoEnemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagen = pygame.image.load("01.png").convert_alpha()
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > alto_ventana:
            self.kill() #lo mismo de antes pero para eliminar al enemigo