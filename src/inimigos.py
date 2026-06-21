"""
Inimigos "normais" (as naves que perseguem o jogador) — spawn nas
bordas da tela, movimento em direção ao jogador, colisões com tiros
e com o próprio jogador, e os drops de vida que eles soltam.

Os bosses têm regras próprias e ficam no pacote bosses/.
"""

import math
import random

from . import config


def spawnar_onda(inimigos, spawnados, alvo_wave, wave):
    """Spawna inimigos pelas bordas da tela até atingir o alvo da wave
    atual. Retorna o novo total de spawnados."""
    while spawnados < alvo_wave:
        lado = random.randint(0, 3)
        if lado == 0:
            x, y = random.randint(0, config.LARGURA), -50
        elif lado == 1:
            x, y = config.LARGURA + 50, random.randint(0, config.ALTURA)
        elif lado == 2:
            x, y = random.randint(0, config.LARGURA), config.ALTURA + 50
        else:
            x, y = -50, random.randint(0, config.ALTURA)

        inimigos.append({"x": x, "y": y, "vel": 1.5 + wave * 0.2})
        spawnados += 1

    return spawnados


def spawnar_reforco(inimigos, quantidade=3, vel=3.0):
    """Usado pelo boss2 em rage: joga reforços nas bordas da tela."""
    for _ in range(quantidade):
        lado = random.randint(0, 3)
        if lado == 0:
            x, y = random.randint(0, config.LARGURA), -50
        elif lado == 1:
            x, y = config.LARGURA + 50, random.randint(0, config.ALTURA)
        elif lado == 2:
            x, y = random.randint(0, config.LARGURA), config.ALTURA + 50
        else:
            x, y = -50, random.randint(0, config.ALTURA)
        inimigos.append({"x": x, "y": y, "vel": vel})


def atualizar(inimigos, jogador, dano_timer, recursos):
    """Move os inimigos em direção ao jogador e aplica dano em colisão.
    Retorna (dano_timer atualizado, morreu)."""
    morreu = False
    for i in inimigos[:]:
        dx = jogador["x"] - i["x"]
        dy = jogador["y"] - i["y"]
        d = max(1, math.hypot(dx, dy))
        i["x"] += dx / d * i["vel"]
        i["y"] += dy / d * i["vel"]

        if d < 35 and dano_timer <= 0:
            jogador["vida"] -= 1
            dano_timer = 60
            recursos.tocar_som(recursos.som_explosao)
            if jogador["vida"] <= 0:
                morreu = True

    return dano_timer, morreu


def colidir_com_tiros(tiros, inimigos, drops, recursos):
    """Verifica acertos de tiros do jogador nos inimigos. Retorna os
    pontos ganhos nesta checagem."""
    pontos = 0
    for t in tiros[:]:
        for i in inimigos[:]:
            if math.hypot(t["x"] - i["x"], t["y"] - i["y"]) < 28:
                if t in tiros:
                    tiros.remove(t)
                if i in inimigos:
                    inimigos.remove(i)
                pontos += 10
                recursos.tocar_som(recursos.som_explosao)
                if random.randint(1, 14) == 1:
                    drops.append({"x": i["x"], "y": i["y"]})
                break
    return pontos


def coletar_drops(drops, jogador):
    """Cura/aumenta a vida máxima do jogador ao encostar num drop."""
    for d in drops[:]:
        if math.hypot(d["x"] - jogador["x"], d["y"] - jogador["y"]) < 30:
            jogador["vida_max"] += 1
            jogador["vida"] += 1
            drops.remove(d)


def desenhar(tela, recursos, inimigos):
    for i in inimigos:
        tela.blit(recursos.inimigo_img, (i["x"] - 24, i["y"] - 24))


def desenhar_drops(tela, recursos, drops):
    for d in drops:
        tela.blit(recursos.coracao_img, (d["x"] - 16, d["y"] - 16))
