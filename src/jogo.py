"""
Loop principal do jogo: junta jogador, inimigos, bosses, projéteis e
interface (menus/HUD), que agora vivem em módulos próprios.
"""

import sys

import pygame

from . import config
from . import persistencia
from . import recursos as modulo_recursos
from . import interface
from . import jogador as modulo_jogador
from . import inimigos as modulo_inimigos
from . import projeteis
from . import melhorias
from .bosses import boss1, boss2


def executar_jogo():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        pass

    tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
    pygame.display.set_caption("Astro Runner Survival")
    relogio = pygame.time.Clock()

    recursos = modulo_recursos.Recursos()
    fontes = modulo_recursos.Fontes()

    estrelas = interface.criar_estrelas()
    recorde = persistencia.carregar_recorde()

    pygame.mouse.set_visible(False)

    while True:
        interface.menu_principal(tela, relogio, recursos, fontes, recorde)

        jogador = modulo_jogador.criar_jogador()
        tiros = []
        tiros_inimigos = []
        inimigos = []
        drops = []
        pontuacao = 0
        wave = 1
        alvo_wave = 5
        spawnados = 0
        cooldown = 0
        dano_timer = 0
        upgrade_dado = False
        boss = None
        boss_derrotado = False
        boss2_obj = None
        boss2_derrotado = False
        boss2_anim_feita = False

        recursos.tocar_musica(recursos.musica_jogo, volume=0.6)

        rodando_partida = True
        morreu = False

        while rodando_partida:
            relogio.tick(config.FPS)

            mx, my = pygame.mouse.get_pos()
            teclas = pygame.key.get_pressed()
            modulo_jogador.mover(jogador, teclas)

            pausar = False
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pausar = True

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and cooldown <= 0:
                    tiros.extend(modulo_jogador.atirar(jogador, mx, my))
                    recursos.tocar_som(recursos.som_tiro)
                    cooldown = 12

            if pausar:
                resultado = interface.menu_pausa(tela, relogio, recursos, fontes)
                if resultado == "menu":
                    rodando_partida = False
                    continue

            if cooldown > 0:
                cooldown -= 1
            if dano_timer > 0:
                dano_timer -= 1

            # ── Spawn inimigos normais ───────────────────────────────────────
            sem_boss_ativo = (boss is None) and (boss2_obj is None)
            nao_e_wave_boss1 = not (wave == 10 and not boss_derrotado)
            nao_e_wave_boss2 = not (wave == 20 and not boss2_derrotado)

            if sem_boss_ativo and nao_e_wave_boss1 and nao_e_wave_boss2:
                spawnados = modulo_inimigos.spawnar_onda(inimigos, spawnados, alvo_wave, wave)

            # ── Boss 1 (wave 10) ──────────────────────────────────────────────
            if wave == 10 and boss is None and not boss_derrotado:
                boss = boss1.criar()
                inimigos.clear()
                spawnados = alvo_wave
                recursos.tocar_musica(recursos.musica_boss, volume=1)

            # ── Boss 2 (wave 20) ──────────────────────────────────────────────
            if wave == 20 and boss2_obj is None and not boss2_derrotado:
                if not boss2_anim_feita:
                    inimigos.clear()
                    tiros_inimigos.clear()
                    spawnados = alvo_wave
                    boss2.animacao_transformacao(tela, relogio, recursos, estrelas)
                    boss2_anim_feita = True

                boss2_obj = boss2.criar()
                inimigos.clear()
                spawnados = alvo_wave

            # ── Tiros do jogador ──────────────────────────────────────────────
            modulo_jogador.atualizar_tiros(tiros)

            # ── Inimigos normais ──────────────────────────────────────────────
            dano_timer, morreu_colisao = modulo_inimigos.atualizar(inimigos, jogador, dano_timer, recursos)
            if morreu_colisao:
                morreu = True

            pontuacao += modulo_inimigos.colidir_com_tiros(tiros, inimigos, drops, recursos)

            # ── Boss 1 — lógica ───────────────────────────────────────────────
            if boss is not None:
                pontos, derrotado = boss1.atualizar(boss, jogador, tiros, tiros_inimigos, recursos)
                pontuacao += pontos
                if derrotado:
                    boss = None
                    boss_derrotado = True
                    recursos.tocar_musica(recursos.musica_jogo, volume=0.6)

            # ── Boss 2 — lógica ───────────────────────────────────────────────
            if boss2_obj is not None:
                pontos, derrotado = boss2.atualizar(
                    boss2_obj, jogador, tiros, tiros_inimigos, inimigos, recursos
                )
                pontuacao += pontos
                if derrotado:
                    boss2_obj = None
                    boss2_derrotado = True
                    inimigos.clear()
                    recursos.tocar_musica(recursos.musica_jogo, volume=0.6)

            # ── Tiros inimigos ────────────────────────────────────────────────
            dano_timer, morreu_tiro = projeteis.atualizar(tiros_inimigos, jogador, dano_timer, recursos)
            if morreu_tiro:
                morreu = True

            # ── Drops de vida ─────────────────────────────────────────────────
            modulo_inimigos.coletar_drops(drops, jogador)

            # ── Avanço de wave ────────────────────────────────────────────────
            sem_boss_ativo = (boss is None) and (boss2_obj is None)
            nao_e_wave_boss1 = not (wave == 10 and not boss_derrotado)
            nao_e_wave_boss2 = not (wave == 20 and not boss2_derrotado)

            if sem_boss_ativo and nao_e_wave_boss1 and nao_e_wave_boss2:
                if spawnados >= alvo_wave and len(inimigos) == 0:
                    wave += 1
                    alvo_wave += 3
                    spawnados = 0

                    if wave == 9 and not upgrade_dado:
                        melhorias.tela_upgrade(tela, relogio, recursos, fontes, estrelas, jogador)
                        upgrade_dado = True

            if pontuacao > recorde:
                recorde = pontuacao
                persistencia.salvar_recorde(recorde)

            if morreu:
                rodando_partida = False
                continue

            # ── RENDER ────────────────────────────────────────────────────────
            interface.desenhar_fundo(tela, estrelas)

            modulo_jogador.desenhar(tela, recursos, jogador, mx, my)
            modulo_jogador.desenhar_tiros(tela, recursos, tiros)
            projeteis.desenhar(tela, tiros_inimigos)
            modulo_inimigos.desenhar(tela, recursos, inimigos)
            modulo_inimigos.desenhar_drops(tela, recursos, drops)

            if boss is not None:
                boss1.desenhar(tela, recursos, fontes, boss)
            if boss2_obj is not None:
                boss2.desenhar(tela, recursos, fontes, boss2_obj)

            interface.desenhar_hud(tela, recursos, fontes, jogador, wave, pontuacao)
            interface.desenhar_mira(tela, recursos)

            pygame.display.flip()

        if morreu:
            recursos.tocar_musica(recursos.musica_menu, volume=0.6)
            interface.tela_game_over(tela, relogio, fontes, pontuacao, recorde)
