#======= IMPORTAÇÃO DE BIBLIOTECAS =======
import pygame, random, math, sys, os

from src.recorde import carregar_recorde, salvar_recorde
from src.menu import menu
from src.pause import pause_screen
from src.gameover import game_over_screen

from src.config import LARGURA, ALTURA, FPS
from src.assets import carregar_sprites

from src.hud import desenhar_hud
from src.entities import criar_inimigo, criar_jogador, criar_tiro
from src.systems import atualizar_tiros, atualizar_waves, colisao_tiros, atualizar_movimento_inimigos, checar_colisao_jogador
from src.render import desenhar_fundo, desenhar_inimigos, desenhar_nave, desenhar_tiros, desenhar_vidas_antigas

#======= FUNÇÃO PRINCIPAL DO JOGO =======
def executar_jogo():

    #======= INIT PYGAME =======
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Astro Runner Survival")
    relogio = pygame.time.Clock()

    #======= FONTES =======
    fonte = pygame.font.SysFont(None, 42)
    fonte_grande = pygame.font.SysFont(None, 90)

    #======= CARREGAMENTO DE SPRITES =======
    nave, inimigo_img, tiro_img = carregar_sprites()

    #======= BACKGROUND =======
    estrelas = [[random.randint(0,LARGURA), random.randint(0,ALTURA), random.randint(1,3)] for _ in range(150)]

    #======= RECORDE =======
    recorde = carregar_recorde()
    
    #======= LOOP PRINCIPAL DO JOGO =======
    while True:
        sair_partida = False

        #======= MENU =======
        menu(
            tela,
            relogio, fonte, fonte_grande,
            nave, estrelas, recorde
        )

        pygame.event.clear()

        #======= RESET DA PARTIDA =======
        jogador = criar_jogador()
        tiros=[]
        inimigos=[]

        pontuacao=0
        wave=1
        alvo_wave=5
        spawnados=0

        cooldown=0
        dano_timer=0

        jogando = True
        pausado = False
        sair_para_menu = False

        #======= LOOP DA PARTIDA =======
        while jogando:
            relogio.tick(FPS)
            mx, my = pygame.mouse.get_pos()

            #======= INPUT =======
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #======= ATIVA PAUSA (ESC) =======
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pausado = True

                #======= DISPARO (BOTÃO DIREITO DO MOUSE) =======
                if (
                    e.type == pygame.MOUSEBUTTONDOWN
                    and e.button == 3
                    and cooldown <= 0
                    and not pausado
                ):
                    #======= CALCULA DIREÇÃO DO TIRO =======
                    ang = math.atan2(
                        my - jogador["y"],
                        mx - jogador["x"]
                    )

                    #======= CRIA O TIRO =======
                    tiros.append({
                        "x": jogador["x"],
                        "y": jogador["y"],
                        "dx": math.cos(ang) * 12,
                        "dy": math.sin(ang) * 12,
                        "angulo": ang
                    })

                    cooldown = 12

            #======= PAUSA =======
            if pausado:
                result = pause_screen(
                    tela,
                    relogio, fonte, fonte_grande,
                    nave, estrelas
                )

                if result == "menu":
                    pygame.event.clear()
                    sair_partida = True
                    break

                pausado = False
                continue

            #======= MOVIMENTO DO JOGADOR =======
            jogador["x"] += (mx - jogador["x"]) * 0.12
            jogador["y"] += (my - jogador["y"]) * 0.12

            #======= COOLDOWN DOS TIROS =======
            if cooldown > 0:
                cooldown -= 1

            #======= TIMER DE INVENCIBILIDADE =======
            if dano_timer > 0:
                dano_timer -= 1

            #======= SPAWN DE INIMIGOS =======
            while spawnados < alvo_wave:
                #======= CRIA O INIMIGO =======
                inimigos.append(criar_inimigo(wave))
                spawnados += 1

            #======= SISTEMAS DE JOGO =======
            #------- atualiza movimento dos tiros -------
            atualizar_tiros(tiros)
            
            #------- move inimigo em direção ao jogador -------
            atualizar_movimento_inimigos(inimigos, jogador)

            #------- verifica colisão entre inimigo e jogador -------
            if checar_colisao_jogador(inimigos, jogador, dano_timer):
                jogador["vida"] -= 1
                dano_timer = 60

                if jogador["vida"] <= 0:
                    jogando = False

            #------- colisao tiros x inimigos -------
            pontuacao += colisao_tiros(tiros, inimigos)

            #------- controle de progressão das waves -------
            if atualizar_waves(spawnados, alvo_wave, inimigos):
                wave += 1
                alvo_wave += 3
                spawnados = 0

            #======= RECORDE =======
            if pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(recorde)

            #======= RENDERIZAÇÃO DAS CENAS =======
            tela.fill((5, 5, 15))

            desenhar_fundo(tela, estrelas)
            desenhar_nave(tela, nave, jogador, mx, my)
            desenhar_tiros(tela, tiros, tiro_img)
            desenhar_inimigos(tela, inimigos, inimigo_img)
            desenhar_vidas_antigas(tela, jogador)

            desenhar_hud(tela, jogador, wave, pontuacao, fonte)
            pygame.display.flip()

        #======= SAÍDA DA PARTIDA =======
        if sair_para_menu:
            jogando = False
            pausado = False
            continue

        if sair_partida:
            continue

        #======= GAME OVER =======
        if not sair_partida:
            result = game_over_screen(
                tela,
                relogio, fonte, fonte_grande,
                inimigo_img, pontuacao, recorde, estrelas
            )

            if result == "menu":
                pygame.event.clear()
                continue