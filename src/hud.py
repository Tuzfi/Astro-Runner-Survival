import pygame

#======= HUD DO JOGO =======
def desenhar_hud(tela, jogador, wave, pontuacao, fonte):

    #======= PAINEL BASE =======
    pygame.draw.rect(
        tela,
        (20, 30, 60),
        (10, 10, 200, 110),
        border_radius=12
    )

    hud_x = 10
    hud_y = 10
    hud_largura = 200
    hud_altura = 110

    #======= SISTEMA DE VIDAS =======
    vida_total = jogador["vida"]
    espaco = 20

    #------- centraliza as vidas no painel -------
    inicio_x = hud_x + hud_largura // 2 - (vida_total - 1) * espaco // 2
    y_vidas = hud_y + hud_altura - 15

    #------- desenha cada vida como círculo -------
    for v in range(vida_total):
        pygame.draw.circle(
            tela,
            (255, 0, 0),
            (inicio_x + v * espaco, y_vidas),
            8
        )

    #======= TEXTO: WAVE =======
    wave_txt = fonte.render(
        f"Wave {wave}",
        True,
        (255, 255, 255)
    )

    #======= TEXTO: PONTUAÇÃO =======
    pontos_txt = fonte.render(
        f"Pontos {pontuacao}",
        True,
        (255, 255, 255)
    )

    #======= RENDER FINAL =======
    tela.blit(wave_txt, (25, 25))
    tela.blit(pontos_txt, (25, 65))