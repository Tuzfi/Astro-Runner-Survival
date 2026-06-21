"""
Tudo relacionado à nave do jogador: criação do estado inicial,
movimento (WASD), disparo e desenho na tela.
"""

import math

import pygame

from . import config


def criar_jogador():
    return {
        "x": config.LARGURA / 2,
        "y": config.ALTURA / 2,
        "vida": 3,
        "vida_max": 3,
        "tiros_extra": 0,
    }


def mover(jogador, teclas, vel=5.5):
    mover_x, mover_y = 0, 0
    if teclas[pygame.K_w]:
        mover_y -= 1
    if teclas[pygame.K_s]:
        mover_y += 1
    if teclas[pygame.K_a]:
        mover_x -= 1
    if teclas[pygame.K_d]:
        mover_x += 1

    if mover_x != 0 or mover_y != 0:
        norm = math.hypot(mover_x, mover_y)
        jogador["x"] += (mover_x / norm) * vel
        jogador["y"] += (mover_y / norm) * vel

    jogador["x"] = max(20, min(config.LARGURA - 20, jogador["x"]))
    jogador["y"] = max(20, min(config.ALTURA - 20, jogador["y"]))


def atirar(jogador, mx, my):
    """Retorna a lista de novos tiros a partir da posição/mira atual."""
    ang = math.atan2(my - jogador["y"], mx - jogador["x"])
    quantidade_tiros = 1 + jogador["tiros_extra"]
    espalhamento = 0.12

    if quantidade_tiros == 1:
        angulos = [ang]
    else:
        angulos = [
            ang + (i - (quantidade_tiros - 1) / 2) * espalhamento
            for i in range(quantidade_tiros)
        ]

    return [
        {"x": jogador["x"], "y": jogador["y"], "dx": math.cos(a) * 12, "dy": math.sin(a) * 12}
        for a in angulos
    ]


def atualizar_tiros(tiros):
    """Move os tiros do jogador e remove os que saíram da tela."""
    for t in tiros[:]:
        t["x"] += t["dx"]
        t["y"] += t["dy"]
        if t["x"] < 0 or t["x"] > config.LARGURA or t["y"] < 0 or t["y"] > config.ALTURA:
            tiros.remove(t)


def desenhar(tela, recursos, jogador, mx, my):
    angulo = -math.degrees(math.atan2(my - jogador["y"], mx - jogador["x"]))
    nave_rot = pygame.transform.rotate(recursos.nave_img, angulo - 90)
    tela.blit(
        nave_rot,
        (jogador["x"] - nave_rot.get_width() / 2, jogador["y"] - nave_rot.get_height() / 2),
    )


def desenhar_tiros(tela, recursos, tiros):
    for t in tiros:
        ang_tiro = -math.degrees(math.atan2(t["dy"], t["dx"]))
        tiro_rot = pygame.transform.rotate(recursos.tiro_img, ang_tiro - 90)
        tela.blit(
            tiro_rot,
            (t["x"] - tiro_rot.get_width() / 2, t["y"] - tiro_rot.get_height() / 2),
        )
