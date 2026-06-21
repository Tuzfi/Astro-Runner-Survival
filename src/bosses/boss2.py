"""
Boss 2 — aparece na wave 20, em duas fases:

  fase1: nave que atira em spread triplo. Ao perder toda a vida,
         dispara a animação de transformação e vira o "boss final".
  final: muito mais agressivo — órbita errática, dash em direção ao
         jogador, tiro circular e, com pouca vida, invoca reforços
         (rage).
"""

import math
import random
import sys

import pygame

from .. import config, interface
from .. import inimigos as modulo_inimigos


def criar():
    return {
        "x": config.LARGURA / 2,
        "y": -250,
        "vida_fase1": 120,
        "vida_fase1_max": 120,
        "vida_final": 200,
        "vida_final_max": 200,
        "fase": "fase1",
        "cooldown_tiro": 45,
        "vel": 1.8,
        # atributos usados apenas na fase final
        "angulo_orbita": 0.0,
        "dash_timer": 0,
        "dash_dx": 0,
        "dash_dy": 0,
        "rage_timer": 0,
    }


def _atualizar_fase1(boss2, jogador, tiros, tiros_inimigos, recursos):
    ticks = pygame.time.get_ticks()

    # Entrada: desce até y=180
    if boss2["y"] < 180:
        boss2["y"] += boss2["vel"]
    else:
        # Movimento senoidal duplo (mais errático que o boss1)
        boss2["x"] += math.sin(ticks * 0.0015) * 2.8
        boss2["y"] = 180 + math.sin(ticks * 0.0008) * 40

    boss2["x"] = max(120, min(config.LARGURA - 120, boss2["x"]))

    # Tiro triplo em spread
    if boss2["cooldown_tiro"] <= 0:
        ang = math.atan2(jogador["y"] - boss2["y"], jogador["x"] - boss2["x"])
        for delta in [-0.25, 0, 0.25]:
            a = ang + delta
            tiros_inimigos.append(
                {"x": boss2["x"], "y": boss2["y"], "dx": math.cos(a) * 9, "dy": math.sin(a) * 9}
            )
        boss2["cooldown_tiro"] = 45
        recursos.tocar_som(recursos.som_tiro)
    else:
        boss2["cooldown_tiro"] -= 1

    # Tiros do jogador acertam a fase 1
    pontos = 0
    for t in tiros[:]:
        if math.hypot(t["x"] - boss2["x"], t["y"] - boss2["y"]) < 90:
            if t in tiros:
                tiros.remove(t)
            boss2["vida_fase1"] -= 1
            recursos.tocar_som(recursos.som_explosao)
            if boss2["vida_fase1"] <= 0:
                # Transição para boss final
                boss2["fase"] = "final"
                boss2["y"] = 220
                boss2["cooldown_tiro"] = 80
                boss2["dash_timer"] = 0
                boss2["rage_timer"] = 0
                pontos += 500
            break

    return pontos


def _atualizar_final(boss2, jogador, tiros, tiros_inimigos, inimigos, recursos):
    boss2["angulo_orbita"] += 0.018
    raio_x, raio_y = 380, 120
    centro_x, centro_y = config.LARGURA / 2, 260
    boss2["x"] = centro_x + math.cos(boss2["angulo_orbita"]) * raio_x
    boss2["y"] = centro_y + math.sin(boss2["angulo_orbita"] * 1.7) * raio_y

    # Dash em direção ao jogador periodicamente
    boss2["dash_timer"] -= 1
    if boss2["dash_timer"] <= 0:
        ang_dash = math.atan2(jogador["y"] - boss2["y"], jogador["x"] - boss2["x"])
        boss2["dash_dx"] = math.cos(ang_dash) * 14
        boss2["dash_dy"] = math.sin(ang_dash) * 14
        boss2["x"] += boss2["dash_dx"] * 8  # impulso do dash
        boss2["y"] += boss2["dash_dy"] * 8
        boss2["x"] = max(80, min(config.LARGURA - 80, boss2["x"]))
        boss2["y"] = max(80, min(config.ALTURA // 2, boss2["y"]))
        boss2["dash_timer"] = random.randint(220, 340)

    # Tiro múltiplo em padrão circular
    if boss2["cooldown_tiro"] <= 0:
        vida_pct = boss2["vida_final"] / boss2["vida_final_max"]
        n_tiros = 5 if vida_pct > 0.5 else 8  # mais tiros com pouca vida
        for k in range(n_tiros):
            a = (2 * math.pi / n_tiros) * k + boss2["angulo_orbita"]
            vel_t = 9 if vida_pct > 0.5 else 11
            tiros_inimigos.append(
                {"x": boss2["x"], "y": boss2["y"], "dx": math.cos(a) * vel_t, "dy": math.sin(a) * vel_t}
            )
        # Tiro direto ao jogador
        ang_j = math.atan2(jogador["y"] - boss2["y"], jogador["x"] - boss2["x"])
        tiros_inimigos.append(
            {"x": boss2["x"], "y": boss2["y"], "dx": math.cos(ang_j) * 13, "dy": math.sin(ang_j) * 13}
        )
        boss2["cooldown_tiro"] = 55 if vida_pct > 0.5 else 35
        recursos.tocar_som(recursos.som_tiro)
    else:
        boss2["cooldown_tiro"] -= 1

    # Rage: abaixo de 30% de vida, invoca reforços
    boss2["rage_timer"] -= 1
    vida_pct = boss2["vida_final"] / boss2["vida_final_max"]
    if vida_pct < 0.30 and boss2["rage_timer"] <= 0 and len(inimigos) < 6:
        modulo_inimigos.spawnar_reforco(inimigos, quantidade=3, vel=3.0)
        boss2["rage_timer"] = 180

    # Tiros do jogador acertam o boss final
    pontos = 0
    derrotado = False
    for t in tiros[:]:
        if math.hypot(t["x"] - boss2["x"], t["y"] - boss2["y"]) < 100:
            if t in tiros:
                tiros.remove(t)
            boss2["vida_final"] -= 1
            recursos.tocar_som(recursos.som_explosao)
            if boss2["vida_final"] <= 0:
                pontos += 2000
                derrotado = True
            break

    return pontos, derrotado


def atualizar(boss2, jogador, tiros, tiros_inimigos, inimigos, recursos):
    """Atualiza a fase atual do boss2.
    Retorna (pontos_ganhos, derrotado)."""
    if boss2["fase"] == "fase1":
        pontos = _atualizar_fase1(boss2, jogador, tiros, tiros_inimigos, recursos)
        return pontos, False

    pontos, derrotado = _atualizar_final(boss2, jogador, tiros, tiros_inimigos, inimigos, recursos)
    return pontos, derrotado


def desenhar(tela, recursos, fontes, boss2):
    barra_largura = 600
    cx = config.LARGURA // 2

    if boss2["fase"] == "fase1":
        sprite = recursos.boss2s1_img
        vida_pct = boss2["vida_fase1"] / boss2["vida_fase1_max"]
        cor_barra = (200, 60, 200)
        label = "BOSS II"
    else:
        sprite = recursos.boss2final_img
        vida_pct = boss2["vida_final"] / boss2["vida_final_max"]
        # aura vermelha piscando no boss final
        if int(pygame.time.get_ticks() / 200) % 2 == 0:
            aura = pygame.Surface((sprite.get_width() + 20, sprite.get_height() + 20), pygame.SRCALPHA)
            aura.fill((255, 0, 0, 40))
            tela.blit(aura, (boss2["x"] - sprite.get_width() // 2 - 10, boss2["y"] - sprite.get_height() // 2 - 10))
        cor_barra = (220, 20, 20)
        label = " BOSS II FINAL "

    tela.blit(sprite, (int(boss2["x"] - sprite.get_width() // 2), int(boss2["y"] - sprite.get_height() // 2)))

    pygame.draw.rect(tela, (60, 0, 0), (cx - barra_largura // 2, 30, barra_largura, 22))
    pygame.draw.rect(tela, cor_barra, (cx - barra_largura // 2, 30, int(barra_largura * vida_pct), 22))
    pygame.draw.rect(tela, config.BRANCO, (cx - barra_largura // 2, 30, barra_largura, 22), 2)

    nome_b2 = fontes.pequena.render(label, True, config.BRANCO)
    tela.blit(nome_b2, (cx - nome_b2.get_width() // 2, 8))


def animacao_transformacao(tela, relogio, recursos, estrelas):
    """
    Animação épica de transformação do Boss 2:
      Fase 1 (0-3s):   Tela treme, boss alterna entre sprite1 e sprite2 rapidamente.
                       A música Slayer começa junto com o tremor.
      Fase 2 (3-3.5s): Flash de explosão cobrindo a tela.
      Fase 3 (3.5s+):  Boss2Final aparece exatamente em ~0:27 da música.
    A música começa no segundo 0 e o boss final aparece exatamente em 0:27.
    Total da animação: 27 segundos contados pela música.
    Para não travar o jogo 27s, usamos 3.5s de animação visual e
    adiantamos a música para que ao terminar a animação estejamos em 0:27.
    Offset de início da música = 0:27 - 3.5s = 23.5s → começa em 23.5s.
    """
    DURACAO_ANIM = 3.5
    MUSIC_OFFSET = 23.5
    SHAKE_DURACAO = 3.0
    FLASH_START = 3.0
    FLASH_DURACAO = 0.5

    # start != 0 garante que tocar_musica() não ignore a troca mesmo que
    # esta já fosse (por acaso) a música "atual".
    recursos.tocar_musica(recursos.musica_boss2final, loop=-1, volume=1.0, start=MUSIC_OFFSET)

    t_inicio = pygame.time.get_ticks()
    cx = config.LARGURA // 2
    cy = 200

    while True:
        agora = pygame.time.get_ticks()
        elapsed = (agora - t_inicio) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Tremor de tela
        if elapsed < SHAKE_DURACAO:
            intensidade = int(18 * (1 - elapsed / SHAKE_DURACAO)) + 4
            shake_x = random.randint(-intensidade, intensidade)
            shake_y = random.randint(-intensidade, intensidade)
        else:
            shake_x, shake_y = 0, 0

        interface.desenhar_fundo(tela, estrelas)

        if shake_x != 0 or shake_y != 0:
            snap = tela.copy()
            tela.fill(config.FUNDO)
            tela.blit(snap, (shake_x, shake_y))

        # Sprite alternando
        if elapsed < FLASH_START:
            frame_idx = int(elapsed * 20) % 2
            sprite_boss = recursos.boss2s1_img if frame_idx == 0 else recursos.boss2s2_img
            tela.blit(sprite_boss, (cx - sprite_boss.get_width() // 2, cy - sprite_boss.get_height() // 2))

        # Flash de explosão
        if elapsed >= FLASH_START:
            prog = (elapsed - FLASH_START) / FLASH_DURACAO
            if prog < 1.0:
                alpha = int(255 * (1 - prog))
                flash = pygame.Surface((config.LARGURA, config.ALTURA), pygame.SRCALPHA)
                flash.fill((255, 200, 80, alpha))
                tela.blit(flash, (0, 0))
            else:
                return

        pygame.display.flip()
        relogio.tick(config.FPS)
