import pygame
from clases import *
import random 
import sqlite3
from base_de_datos import *
from constantes import *
import sys
from colores import *
 
pygame.init() #inicio pygame
pygame.mixer.init()

#pongo un titulo al juego
pygame.display.set_caption("Space Jam")

#defino todas las imagenes con sus respectivas escalas de tamañao(que se ajusten al ancho y alto de mi ventana)
imagen_juego = pygame.image.load("fondo_menuuuu.jpg").convert_alpha()
imagen_juego = pygame.transform.scale(imagen_juego, (ancho_ventana,alto_ventana)) 
imagen_menu = pygame.image.load("juego/3lXVAy.png")
imagen_menu = pygame.transform.scale(imagen_menu, (ancho_ventana, alto_ventana))
imagen_ranking = pygame.image.load("fondo_ranking.jpg").convert_alpha()
imagen_ranking = pygame.transform.scale(imagen_ranking, (ancho_ventana,alto_ventana)) 

#colores que usare para los botones de texto
RED = (61, 145, 64)
BANANA = (227, 207, 87)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

#variables que necesito inicializar fuera del while para el juego en accion
vidas = 3
puntos = 0
texto_ingresado = ""

#declaro la posicion inicial de mi nave
posicion_nave = pygame.Rect(40, 300, 0, 0)

#inicializo la bibloteca integrada para trabajar con fuentes de texto de pygame
pygame.font.init()
fuente = pygame.font.SysFont("Arial", 24)

#creo mi controlador de fps
fps = pygame.time.Clock()

enemigos = [] #aca voy a almacenar mis enemigos 
proyectiles = pygame.sprite.Group() # 
disparos_enemigos = pygame.sprite.Group()

#declaro mi variable personaje 1 con mi clase jugador
personaje1 = Jugador()


#declaro la posicion de mis botones
boton_jugar = pygame.Rect(400, 200, 200, 50)
boton_salir = pygame.Rect(400, 300, 200, 50)
boton_ranking = pygame.Rect(400, 400, 200, 50)
boton_volver_menu = pygame.Rect(400,400,200,50)



def puntuaciones():
    while True:
        #muestro la imagen del ranking al momento de perder
        pantalla.blit(imagen_ranking, imagen_ranking.get_rect()) 

        #fuente que utilizo para mostrar los puntajes
        font_puntuaciones = pygame.font.SysFont("cambria", 100)

        #muestro en la pantalla el mensaje "top 10"
        mejores_score = font_puntuaciones.render("Top 10", True , BLANCO)

        #lo bliteo para que aparezca en pantalla
        pantalla.blit(mejores_score, (230, 10))

        #
        font = pygame.font.SysFont(None, 50)
        y = 170
        posicion_juego = 1

        resultados = leer_tabla_puntuaciones()

        for nombre, puntacion in resultados:
            texto = font.render(f"{posicion_juego}. {nombre} - {puntacion}", True, BLANCO)
            pantalla.blit(texto, (50, y))
            y += 50
            posicion_juego += 1

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYUP and evento.key == pygame.K_ESCAPE:
                mostrar_menu()

        pygame.display.flip()

def mostrar_menu():
    fuente_menu = pygame.font.Font(None, 90)
    texto_menu = fuente_menu.render("Space Jam", True, (255, 255, 255))
    posicion_texto_menu = texto_menu.get_rect()

    pygame.mixer.music.load("juego/musica_del_juego.mp3") #cargo la musica
    pygame.mixer.music.play(5) #play recibe como parametro 5 que sera las veces que se reproducira la musica    

    
    
    while True:

        pantalla.blit(imagen_menu,(0,0))

        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    iniciar_juego()
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
                elif boton_ranking.collidepoint(evento.pos):
                    crear_tabla_puntuaciones()
                    puntuaciones()
                    

        posicion_texto_menu.x = 370
        posicion_texto_menu.y = 70

    
        pantalla.blit(texto_menu, posicion_texto_menu)
        pygame.draw.rect(pantalla, ROJO, boton_jugar)
        texto_boton_jugar = fuente.render("Jugar", True, BLANCO)
        posicion_texto_jugar = texto_boton_jugar.get_rect()
        posicion_texto_jugar.center = boton_jugar.center
        pantalla.blit(texto_boton_jugar, posicion_texto_jugar)

        pygame.draw.rect(pantalla, ROJO, boton_ranking)
        texto_boton_ranking = fuente.render("Ver Ranking", True, BLANCO)
        posicion_texto_ranking = texto_boton_ranking.get_rect()
        posicion_texto_ranking.center = boton_ranking.center
        pantalla.blit(texto_boton_ranking, posicion_texto_ranking)

        pygame.draw.rect(pantalla, ROJO, boton_salir)
        texto_boton_salir = fuente.render("Salir", True, BLANCO)
        posicion_texto_salir = texto_boton_salir.get_rect()
        posicion_texto_salir.center = boton_salir.center
        pantalla.blit(texto_boton_salir, posicion_texto_salir)


        pygame.display.flip()

def mostrar_game_over():
    fuente_game_over = pygame.font.Font(None, 90)
    texto_game_over = fuente_game_over.render("Game Over", True, (255, 255, 255))
    posicion_texto_game_over = texto_game_over.get_rect()
    posicion_texto_game_over.x = 370
    posicion_texto_game_over.y = 70

    texto_ingrese_su_nombre = fuente_game_over.render("Ingrese Su Nombre",True ,(255,255,255))
    posicion_texto_ingrese_su_nombre = texto_ingrese_su_nombre.get_rect()
    posicion_texto_ingrese_su_nombre.x = 300
    posicion_texto_ingrese_su_nombre.y =500

    font = pygame.font.SysFont("Cambria", 40)
    texto_ingresado = ""
    nombre_ingresado = False 
    rect_texto = pygame.Rect(350,600,140,60)
    en_poscion = False


    while True:

        pantalla.blit(imagen_juego,(0,0))

        pantalla.blit(texto_game_over,posicion_texto_game_over)

        pantalla.blit(texto_ingrese_su_nombre,posicion_texto_ingrese_su_nombre)
        

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(evento.pos):
                    iniciar_juego()
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
                elif boton_volver_menu.collidepoint(evento.pos):
                    crear_tabla_puntuaciones()
                    modificar_tabla_puntuaciones(texto_ingresado,puntos)
                    mostrar_menu()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                    if rect_texto.collidepoint(evento.pos):
                        en_poscion = True
                    else:
                        en_poscion = False

            if evento.type == pygame.KEYDOWN:
                if en_poscion and not nombre_ingresado:  # Solo permitir entrada de texto si no se ha ingresado un nombre
                    if evento.key == pygame.K_BACKSPACE:
                        texto_ingresado = texto_ingresado[0:-1]
                    elif evento.key == pygame.K_RETURN:  # Comprobar si se presiona la tecla Enter
                        nombre_ingresado = True  # Establecer la bandera en True para indicar que se ha ingresado un nombre
                    else:
                        texto_ingresado += evento.unicode
        

        if en_poscion and not nombre_ingresado:
            color_actual = (BANANA)
        else:
            color_actual = (BANANA)

        pygame.draw.rect(pantalla,color_actual, rect_texto)

        superficie_texto = font.render(texto_ingresado, True,(255,255,255))
        pantalla.blit(superficie_texto,rect_texto)

        rect_texto.w = max(400,superficie_texto.get_width() + 10)
        

        pygame.draw.rect(pantalla, ROJO, boton_jugar)
        texto_boton_jugar = fuente.render("Volver a Jugar", True, BLANCO)
        posicion_texto_jugar = texto_boton_jugar.get_rect()
        posicion_texto_jugar.center = boton_jugar.center
        pantalla.blit(texto_boton_jugar, posicion_texto_jugar)

        pygame.draw.rect(pantalla, ROJO, boton_salir)
        texto_boton_salir = fuente.render("Salir", True, BLANCO)
        posicion_texto_salir = texto_boton_salir.get_rect()
        posicion_texto_salir.center = boton_salir.center
        pantalla.blit(texto_boton_salir, posicion_texto_salir)

        pygame.draw.rect(pantalla, ROJO, boton_volver_menu)
        texto_volver_menu = fuente.render("volver al menu", True, BLANCO)
        posicion_volver = texto_volver_menu.get_rect()
        posicion_volver.center = boton_volver_menu.center
        pantalla.blit(texto_volver_menu, posicion_volver)

        


        pygame.display.flip() 



def iniciar_juego():
    global vidas, puntos, enemigos, proyectiles
    vidas = 3
    puntos = 0
    enemigo = Enemigos()
    enemigos.clear()
    proyectiles.empty()
    disparos_enemigos.empty()

    tiempo_entre_disparos = 2000  # Disparar cada 2 segundos
    ultimo_disparo = pygame.time.get_ticks()

    pygame.mixer.music.load("juego/musica_del_juego.mp3") #cargo la musica
    pygame.mixer.music.play(5) #play recibe como parametro 5 que sera las veces que se reproducira la musica


    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    proyectil = Proyectil(personaje1.rect.centerx, personaje1.rect.top)
                    proyectiles.add(proyectil)

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - ultimo_disparo > tiempo_entre_disparos:
            for enemigo in enemigos:
                enemigo.disparar()

            ultimo_disparo = tiempo_actual

        personaje1.movimiento()

        for enemigo in enemigos:
            if enemigo.rect.colliderect(personaje1.rect):
                vidas -= 1
                enemigo.kill()

        if vidas < 1:
            pygame.mixer.music.load("juego/videogame-death-sound-43894.mp3") #cargo la musica
            pygame.mixer.music.play()
            mostrar_game_over()
            font = pygame.font.SysFont(None,100)
            surface = font.render(f"{texto_ingresado}",True, BLANCO)
            pantalla.blit(surface,(0,0))
            crear_tabla_puntuaciones()
            modificar_tabla_puntuaciones(texto_ingresado , puntos)

        if len(enemigos) < 4:
            enemigo = Enemigos()
            enemigos.append(enemigo)

        pantalla.blit(imagen_juego, (0, 0))
        personaje1.draw()

        proyectil = proyectiles

        for enemigo in enemigos:
            enemigo.update()
            pantalla.blit(enemigo.imagen, enemigo.rect)

            if pygame.sprite.spritecollideany(enemigo, proyectiles):
                enemigo.kill()
                puntos += 100
                texto_impacto = fuente.render("+100", True, (255, 255, 255))
                texto_impacto_rect = texto_impacto.get_rect()
                pantalla.blit(texto_impacto, texto_impacto_rect)

        for disparo in disparos_enemigos:
            disparo.update()
            pantalla.blit(disparo.imagen, disparo.rect)
            if disparo.rect.colliderect(personaje1.rect):
                vidas -= 1
                disparo.kill()

        if len(disparos_enemigos) < 3:
            for enemigo in enemigos:
                if random.random() < 0.01:  # Probabilidad de disparar por enemigo (1%)
                    disparo = DisparoEnemigo(enemigo.rect.centerx, enemigo.rect.bottom)
                    disparos_enemigos.add(disparo)

        texto_vidas = fuente.render("Vidas: " + str(vidas), True, (255, 255, 255))
        pantalla.blit(texto_vidas, (10, 10))

        texto_puntos = fuente.render("Puntos: " + str(puntos), True, (255, 255, 255))
        pantalla.blit(texto_puntos, (10, 40))

        proyectiles.update()
        proyectiles.draw(pantalla)


        pygame.display.flip()
        fps.tick(60)
mostrar_menu()