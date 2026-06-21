"""
Boss 1 — aparece na wave 10. Desce até uma altura fixa, balança de
lado a lado e atira em direção ao jogador.
"""

import math

import pygame

from .. import config


def criar():
    return {
        "x": config.LARGURA / 2,
        "y": -200,
        "vida": 75,
        "vida_max": 75,
        "cooldown_tiro": 60,
        "vel": 1.2,
    }


def atualizar(boss, jogador, tiros, tiros_inimigos, recursos):
    """Move o boss, dispara e checa acertos dos tiros do jogador.
    Retorna (pontos_ganhos, derrotado)."""
    if boss["y"] < 150:
        boss["y"] += boss["vel"]
    else:
        boss["x"] += math.sin(pygame.time.get_ticks() * 0.001) * 2

    boss["x"] = max(100, min(config.LARGURA - 100, boss["x"]))

    if boss["cooldown_tiro"] <= 0:
        ang = math.atan2(jogador["y"] - boss["y"], jogador["x"] - boss["x"])
        tiros_inimigos.append(
            {"x": boss["x"], "y": boss["y"], "dx": math.cos(ang) * 8, "dy": math.sin(ang) * 8}
        )
        boss["cooldown_tiro"] = 55
        recursos.tocar_som(recursos.som_tiro)
    else:
        boss["cooldown_tiro"] -= 1

    pontos = 0
    derrotado = False
    for t in tiros[:]:
        if math.hypot(t["x"] - boss["x"], t["y"] - boss["y"]) < 70:
            if t in tiros:
                tiros.remove(t)
            boss["vida"] -= 1
            recursos.tocar_som(recursos.som_explosao)
            if boss["vida"] <= 0:
                pontos += 1000
                derrotado = True
            break

    return pontos, derrotado


def desenhar(tela, recursos, fontes, boss):
    tela.blit(recursos.boss_img, (boss["x"] - 80, boss["y"] - 80))

    barra_largura = 400
    vida_pct = boss["vida"] / boss["vida_max"]
    cx = config.LARGURA // 2
    pygame.draw.rect(tela, (60, 0, 0), (cx - barra_largura // 2, 30, barra_largura, 18))
    pygame.draw.rect(
        tela, (220, 30, 30), (cx - barra_largura // 2, 30, int(barra_largura * vida_pct), 18)
    )
    pygame.draw.rect(tela, config.BRANCO, (cx - barra_largura // 2, 30, barra_largura, 18), 2)

    nome_boss = fontes.pequena.render("BOSS", True, config.BRANCO)
    tela.blit(nome_boss, (cx - nome_boss.get_width() // 2, 8))
