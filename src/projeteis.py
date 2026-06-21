"""
Projéteis inimigos — os tiros disparados pelos bosses contra o
jogador. Movimento, colisão com o jogador e desenho.
"""

import math

import pygame

from . import config


def atualizar(tiros_inimigos, jogador, dano_timer, recursos, dano=2):
    """Move os tiros, remove os que saíram da tela e aplica dano ao
    jogador em caso de acerto. Retorna (dano_timer atualizado, morreu)."""
    morreu = False
    for t in tiros_inimigos[:]:
        t["x"] += t["dx"]
        t["y"] += t["dy"]

        if t["x"] < 0 or t["x"] > config.LARGURA or t["y"] < 0 or t["y"] > config.ALTURA:
            tiros_inimigos.remove(t)
            continue

        if math.hypot(t["x"] - jogador["x"], t["y"] - jogador["y"]) < 16 and dano_timer <= 0:
            jogador["vida"] -= dano
            dano_timer = 60
            recursos.tocar_som(recursos.som_explosao)
            tiros_inimigos.remove(t)
            if jogador["vida"] <= 0:
                morreu = True

    return dano_timer, morreu


def desenhar(tela, tiros_inimigos):
    for t in tiros_inimigos:
        pygame.draw.circle(tela, (255, 80, 80), (int(t["x"]), int(t["y"])), 6)
