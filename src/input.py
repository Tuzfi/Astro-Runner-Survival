import pygame, math
from src.entities import criar_tiro

#======= SISTEMA DE INPUT =======
def processar_input(event, estado):

    #======= TECLADO =======
    if event.type == pygame.KEYDOWN:
        #------- ESC ativa pausa -------
        if event.key == pygame.K_ESCAPE:
            estado["pausado"] = True

    #======= MOUSE =======
    if (
        event.type == pygame.MOUSEBUTTONDOWN
        and event.button == 3
        and estado["cooldown"] <= 0
        and not estado["pausado"]
    ):
        #------- posição atual do mouse -------
        mx, my = pygame.mouse.get_pos()

        #------- cria tiro pela função "criar_tiro" dentro de "entities.py" -------
        estado["tiros"].append(
            criar_tiro(estado["jogador"], mx, my)
        )

        #------- aplica cooldown de disparo -------
        estado["cooldown"] = 12