import pygame
from src.config import LARGURA, ALTURA, FPS

#======= HUD DO JOGO =======
def desenhar_hud(tela, jogador, wave, pontuacao, fonte, percentual, vida_flash):

    #======= PAINEL BASE =======
    hud_surface = pygame.Surface((200, 110), pygame.SRCALPHA)
    hud_surface.fill((20, 30, 60, 140))

    pygame.draw.rect(
        hud_surface,
        (80, 120, 255, 80),
        hud_surface.get_rect(),
        1,
        border_radius=12
    )
    tela.blit(hud_surface, (10, 10))

    hud_x = 10
    hud_y = 10
    hud_largura = 200
    hud_altura = 110

    #======= SISTEMA DE VIDAS =======
    vida_total = 3
    espaco = 20

    #------- centraliza as vidas no painel -------
    inicio_x = hud_x + hud_largura // 2 - (vida_total - 1) * espaco // 2
    y_vidas = hud_y + hud_altura - 15

    #------- desenha cada vida como círculo -------
    for v in range(3):
        pos = (inicio_x + v * espaco, y_vidas)
        #------- vidas normais -------
        if v < jogador["vida"]:
            pygame.draw.circle(tela, (255, 0, 0), pos, 8)
        #------- faz as vidas perdidas piscarem -------
        elif v == jogador["vida"] and vida_flash > 0:
            if (vida_flash // 4) % 2 == 0:
                pygame.draw.circle(tela, (255, 120, 120), pos, 8)

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

    #======= BARRA DE WAVE =======
    #------- inicialização -------
    if not hasattr(desenhar_hud, "barra_animada"):
        desenhar_hud.barra_animada = 0

    alvo = percentual
    #------- animação suave -------
    desenhar_hud.barra_animada += (alvo - desenhar_hud.barra_animada) * 0.1

    #------- fundo translucido -------
    barra = pygame.Surface((260, 14), pygame.SRCALPHA)
    barra.fill((50, 50, 50, 120))  # alpha = transparência
    tela.blit(barra, ((LARGURA // 2) - 130, 25))

    #------- preenchimento animado -------
    pygame.draw.rect(
        tela,
        (0, 255, 120),
        ((LARGURA // 2) - 130, 25, int(260 * desenhar_hud.barra_animada), 14)
    )