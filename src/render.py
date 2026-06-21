import pygame, random, math
from src.config import LARGURA, ALTURA

#======= BACKGROUND =======
def desenhar_fundo(tela, estrelas):
    tela.fill((5, 5, 15))

    for e in estrelas:
        #------- movimento das estrelas (profundidade) -------
        e[1] += e[2] * (0.4 + e[2] * 0.3)

        #------- se a estrela saiu da tela, reaparece no topo -------
        if e[1] > ALTURA:
            e[1] = 0
            e[0] = random.randint(0, LARGURA)

        #------- desenha estrela -------
        pygame.draw.circle(
            tela,
            (255, 255, 255),
            (int(e[0]), int(e[1])),
            e[2]
        )

#======= DESENHO DA NAVE =======
def desenhar_nave(tela, nave, jogador, mx, my):

    #------- calcula ângulo entre nave e mouse -------
    angulo = -math.degrees(
        math.atan2(my - jogador["y"], mx - jogador["x"])
    )

    #------- rotaciona sprite da nave -------
    nave_rot = pygame.transform.rotate(nave, angulo - 90)

    #------- desenha centralizado na posição do jogador -------
    tela.blit(
        nave_rot,
        (
            jogador["x"] - nave_rot.get_width() / 2,
            jogador["y"] - nave_rot.get_height() / 2
        )
    )

#======= DESENHO DOS TIROS =======
def desenhar_tiros(tela, tiros, tiro_img):

    #------- rotaciona sprite do tiro para direção correta -------
    for t in tiros:
        tiro_rot = pygame.transform.rotate(
            tiro_img,
            -math.degrees(t["angulo"]) - 90
        )

        #------- desenha centralizado na posição do tiro -------
        tela.blit(
            tiro_rot,
            (
                t["x"] - tiro_rot.get_width() / 2,
                t["y"] - tiro_rot.get_height() / 2
            )
        )

#======= DESENHO DOS INIMIGOS =======
def desenhar_inimigos(tela, inimigos, inimigo_img):
    for i in inimigos:
        tela.blit(inimigo_img, (i["x"] - 24, i["y"] - 24))

#======= HUD DE VIDAS ANTIGA =======
def desenhar_vidas_antigas(tela, jogador):

    #------- desenha uma bolinha vermelha para cada vida -------
    for v in range(jogador["vida"]):
        pygame.draw.circle(
            tela,
            (255, 0, 0),
            (30 + v * 35, 30),
            12
        )