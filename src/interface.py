"""
Tudo de interface que não é gameplay direto: o fundo estrelado, os
botões/menus (principal, pausa, game over) e o HUD (vida, wave,
pontuação) durante a partida.
"""

import random
import sys

import pygame

from . import config


# ── Fundo estrelado ─────────────────────────────────────────────────────────
def criar_estrelas(quantidade=150):
    return [
        [random.randint(0, config.LARGURA), random.randint(0, config.ALTURA), random.randint(1, 3)]
        for _ in range(quantidade)
    ]


def desenhar_fundo(tela, estrelas):
    tela.fill(config.FUNDO)
    for e in estrelas:
        pygame.draw.circle(tela, config.BRANCO, (int(e[0]), int(e[1])), e[2])
        e[1] += 0.3
        if e[1] > config.ALTURA:
            e[1] = 0
            e[0] = random.randint(0, config.LARGURA)


# ── Botões ───────────────────────────────────────────────────────────────────
def desenhar_botao_sprite(tela, img, cx, cy, selecionado):
    """Desenha um sprite de botão centralizado. Adiciona brilho/escala se selecionado."""
    if selecionado:
        w = int(img.get_width() * 1.08)
        h = int(img.get_height() * 1.08)
        img_draw = pygame.transform.scale(img, (w, h))
        brilho = img_draw.copy()
        brilho.fill((80, 0, 180, 60), special_flags=pygame.BLEND_RGBA_ADD)
        img_draw.blit(brilho, (0, 0))
    else:
        img_draw = img
    tela.blit(img_draw, (cx - img_draw.get_width() // 2, cy - img_draw.get_height() // 2))


def desenhar_botao(tela, fontes, rect, texto, selecionado):
    cor_borda = config.ROXO if selecionado else config.CINZA_CLARO
    cor_fundo = (40, 30, 60) if selecionado else (25, 25, 35)
    pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
    pygame.draw.rect(tela, cor_borda, rect, width=3, border_radius=10)
    txt = fontes.normal.render(texto, True, config.BRANCO)
    tela.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))


def desenhar_mira(tela, recursos):
    mx, my = pygame.mouse.get_pos()
    tela.blit(recursos.mira_img, (mx - recursos.mira_img.get_width() // 2, my - recursos.mira_img.get_height() // 2))


# ── Menus ────────────────────────────────────────────────────────────────────
def menu_principal(tela, relogio, recursos, fontes, recorde):
    """Tela inicial do jogo com sprites. Retorna quando o jogador escolhe Jogar."""
    recursos.tocar_musica(recursos.musica_menu, volume=0.6)
    opcoes = ["Jogar", "Sair"]
    selecionado = 0

    sprites_botoes = [recursos.jogar_img, recursos.sair_img]
    cx = config.LARGURA // 2
    btn_y = [420, 530]

    estrelas = criar_estrelas()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_DOWN, pygame.K_s):
                    selecionado = (selecionado + 1) % len(opcoes)
                elif e.key in (pygame.K_UP, pygame.K_w):
                    selecionado = (selecionado - 1) % len(opcoes)
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if opcoes[selecionado] == "Jogar":
                        return
                    else:
                        pygame.quit()
                        sys.exit()
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = pygame.mouse.get_pos()
                for i, y in enumerate(btn_y):
                    img = sprites_botoes[i]
                    rx = cx - img.get_width() // 2
                    ry = y - img.get_height() // 2
                    if rx <= mx <= rx + img.get_width() and ry <= my <= ry + img.get_height():
                        if i == 0:
                            return
                        else:
                            pygame.quit()
                            sys.exit()
            if e.type == pygame.MOUSEMOTION:
                mx2, my2 = pygame.mouse.get_pos()
                for i, y in enumerate(btn_y):
                    img = sprites_botoes[i]
                    rx = cx - img.get_width() // 2
                    ry = y - img.get_height() // 2
                    if rx <= mx2 <= rx + img.get_width() and ry <= my2 <= ry + img.get_height():
                        selecionado = i

        desenhar_fundo(tela, estrelas)

        tela.blit(recursos.logo_img, (cx - recursos.logo_img.get_width() // 2, 80))

        rec_txt = fontes.normal.render(f"Recorde: {recorde}", True, config.BRANCO)
        tela.blit(rec_txt, (cx - rec_txt.get_width() // 2, 310))

        for i, (img, y) in enumerate(zip(sprites_botoes, btn_y)):
            desenhar_botao_sprite(tela, img, cx, y, i == selecionado)

        dica = fontes.pequena.render(
            "WASD para mover | Mouse para apontar | Botao esquerdo para atirar | ESC pausa",
            True, config.CINZA_CLARO,
        )
        tela.blit(dica, (config.LARGURA // 2 - dica.get_width() // 2, config.ALTURA - 50))

        desenhar_mira(tela, recursos)

        pygame.display.flip()
        relogio.tick(config.FPS)


def menu_pausa(tela, relogio, recursos, fontes):
    """Mostra o menu de pausa com sprites. Retorna 'continuar' ou 'menu'."""
    opcoes_txt = ["Continuar", "Voltar ao Menu", "Sair do Jogo"]
    sprites_pausa = [recursos.continuar_img, recursos.voltarmenu_img, None]  # None = botão texto
    selecionado = 0
    overlay = pygame.Surface((config.LARGURA, config.ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))

    pygame.mixer.music.pause()

    cx = config.LARGURA // 2
    btn_y = [340, 450, 560]

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()
                    return "continuar"
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    selecionado = (selecionado + 1) % len(opcoes_txt)
                elif e.key in (pygame.K_UP, pygame.K_w):
                    selecionado = (selecionado - 1) % len(opcoes_txt)
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                    escolha = opcoes_txt[selecionado]
                    if escolha == "Continuar":
                        pygame.mixer.music.unpause()
                        return "continuar"
                    elif escolha == "Voltar ao Menu":
                        return "menu"
                    else:
                        pygame.quit()
                        sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = pygame.mouse.get_pos()
                for i, y in enumerate(btn_y):
                    img = sprites_pausa[i]
                    if img:
                        rx = cx - img.get_width() // 2
                        ry = y - img.get_height() // 2
                        if rx <= mx <= rx + img.get_width() and ry <= my <= ry + img.get_height():
                            selecionado = i
                            if i == 0:
                                pygame.mixer.music.unpause()
                                return "continuar"
                            elif i == 1:
                                return "menu"
                    else:
                        rect = pygame.Rect(cx - 160, y - 30, 320, 60)
                        if rect.collidepoint(mx, my):
                            pygame.quit()
                            sys.exit()
            if e.type == pygame.MOUSEMOTION:
                mx2, my2 = pygame.mouse.get_pos()
                for i, y in enumerate(btn_y):
                    img = sprites_pausa[i]
                    if img:
                        rx = cx - img.get_width() // 2
                        ry = y - img.get_height() // 2
                        if rx <= mx2 <= rx + img.get_width() and ry <= my2 <= ry + img.get_height():
                            selecionado = i
                    else:
                        rect = pygame.Rect(cx - 160, y - 30, 320, 60)
                        if rect.collidepoint(mx2, my2):
                            selecionado = i

        tela.blit(overlay, (0, 0))

        titulo = fontes.grande.render("PAUSADO", True, config.BRANCO)
        tela.blit(titulo, (cx - titulo.get_width() // 2, 200))

        for i, y in enumerate(btn_y):
            img = sprites_pausa[i]
            if img:
                desenhar_botao_sprite(tela, img, cx, y, i == selecionado)
            else:
                rect = pygame.Rect(cx - 160, y - 30, 320, 60)
                desenhar_botao(tela, fontes, rect, opcoes_txt[i], i == selecionado)

        desenhar_mira(tela, recursos)

        pygame.display.flip()
        relogio.tick(config.FPS)


def tela_game_over(tela, relogio, fontes, pontuacao, recorde):
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                return

        tela.fill((0, 0, 0))
        tela.blit(fontes.grande.render("GAME OVER", True, config.VERMELHO), (config.LARGURA // 2 - 220, 220))
        txt1 = fontes.normal.render(f"Pontuacao: {pontuacao}", True, config.BRANCO)
        tela.blit(txt1, (config.LARGURA // 2 - txt1.get_width() // 2, 340))
        txt2 = fontes.normal.render(f"Recorde: {recorde}", True, config.BRANCO)
        tela.blit(txt2, (config.LARGURA // 2 - txt2.get_width() // 2, 390))
        txt3 = fontes.normal.render("Pressione qualquer tecla para voltar ao menu", True, config.BRANCO)
        tela.blit(txt3, (config.LARGURA // 2 - txt3.get_width() // 2, 470))
        pygame.display.flip()
        relogio.tick(config.FPS)


# ── HUD durante a partida ──────────────────────────────────────────────────
def desenhar_hud(tela, recursos, fontes, jogador, wave, pontuacao):
    for v in range(jogador["vida_max"]):
        pos_x = 30 + v * 36
        if v < jogador["vida"]:
            tela.blit(recursos.coracao_img, (pos_x, 20))
        else:
            cinza_coracao = recursos.coracao_img.copy()
            cinza_coracao.fill((70, 70, 70, 180), special_flags=pygame.BLEND_RGBA_MULT)
            tela.blit(cinza_coracao, (pos_x, 20))

    tela.blit(fontes.normal.render(f"Wave {wave}", True, config.BRANCO), (10, 65))
    tela.blit(fontes.normal.render(f"Pontos {pontuacao}", True, config.BRANCO), (10, 105))

    if jogador["tiros_extra"] > 0:
        tela.blit(
            fontes.pequena.render(f"Tiros extras: {jogador['tiros_extra']}", True, config.VERDE),
            (10, 150),
        )
