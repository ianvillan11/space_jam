import pygame

ancho_ventana = 1100
alto_ventana = 700
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Space Jam")
imagen_galaxy = pygame.image.load("juego/3lXVAy.png")
imagen_galaxy = pygame.transform.scale(imagen_galaxy, (ancho_ventana, alto_ventana))