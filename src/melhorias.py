"""
Tela de escolha de melhoria (upgrade), exibida na wave 9.
Aplica o upgrade escolhido direto no dicionário do jogador.
"""

import sys

import pygame

from . import config, interface


def tela_upgrade(tela, relogio, recursos, fontes, estrelas, jogador):
    opcoes = [
        ("+2 Tiros", "tiros"),
        ("+2 Coracoes", "vida"),
    ]
    selecionado = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_LEFT, pygame.K_a):
                    selecionado = (selecionado - 1) % len(opcoes)
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    selecionado = (selecionado + 1) % len(opcoes)
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    tipo = opcoes[selecionado][1]
                    if tipo == "tiros":
                        jogador["tiros_extra"] += 2
                    else:
                        jogador["vida_max"] += 2
                        jogador["vida"] += 2
                    return

        overlay = pygame.Surface((config.LARGURA, config.ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        interface.desenhar_fundo(tela, estrelas)
        tela.blit(overlay, (0, 0))

        titulo = fontes.media.render("Escolha um upgrade!", True, config.BRANCO)
        tela.blit(titulo, (config.LARGURA // 2 - titulo.get_width() // 2, 150))

        largura_card, altura_card = 320, 220
        espaco = 60
        inicio_x = config.LARGURA // 2 - (largura_card * 2 + espaco) // 2
        for i, (texto, tipo) in enumerate(opcoes):
            rect = pygame.Rect(inicio_x + i * (largura_card + espaco), 260, largura_card, altura_card)
            cor_borda = config.ROXO if i == selecionado else config.CINZA_CLARO
            cor_fundo = (40, 30, 60) if i == selecionado else (25, 25, 35)
            pygame.draw.rect(tela, cor_fundo, rect, border_radius=14)
            pygame.draw.rect(tela, cor_borda, rect, width=4, border_radius=14)

            if tipo == "tiros":
                tela.blit(recursos.tiro_img, (rect.centerx - 30, rect.top + 40))
                tela.blit(recursos.tiro_img, (rect.centerx + 12, rect.top + 40))
            else:
                tela.blit(recursos.coracao_img, (rect.centerx - 40, rect.top + 50))
                tela.blit(recursos.coracao_img, (rect.centerx + 8, rect.top + 50))

            txt = fontes.normal.render(texto, True, config.BRANCO)
            tela.blit(txt, (rect.centerx - txt.get_width() // 2, rect.bottom - 60))

        dica = fontes.pequena.render(
            "Use A/D ou Setas para escolher e ENTER para confirmar", True, config.CINZA_CLARO
        )
        tela.blit(dica, (config.LARGURA // 2 - dica.get_width() // 2, config.ALTURA - 60))

        pygame.display.flip()
        relogio.tick(config.FPS)
