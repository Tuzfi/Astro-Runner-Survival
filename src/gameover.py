import pygame, random, sys, math
from src.config import LARGURA, ALTURA, FPS

#======= TELA DE GAME OVER =======
def game_over_screen(tela, relogio, fonte,
                     fonte_grande, inimigo_img, pontuacao, recorde, estrelas):

    #======= LOOP DA TELA =======
    while True:
        #======= INPUT =======
        for e in pygame.event.get():
            #------- fechamento do jogo -------
            if e.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            #------- qualquer tecla volta ao menu -------
            if e.type==pygame.KEYDOWN:
                return "menu"
        else:
            #======= FUNDO =======
            tela.fill((3, 5, 20))

            #======= BACKGROUND =======
            for estrela in estrelas:

                #------- movimento lento -------
                estrela[1] += estrela[2] * 0.15

                #------- reset quando sai da tela -------
                if estrela[1] > ALTURA:
                    estrela[1] = 0
                    estrela[0] = random.randint(0, LARGURA)

                #------- desenha estrela -------
                pygame.draw.circle(
                    tela,
                    (255,255,255),
                    (int(estrela[0]), int(estrela[1])),
                    estrela[2]
                )

            #======= ANIMAÇÃO DO INIMIGO =======
            #------- movimento de flutuação -------
            offset_y = math.sin(
                pygame.time.get_ticks() * 0.0025
            ) * 15

            #------- cria versão maior do inimigo -------
            inimigo_menu = pygame.transform.scale(
                inimigo_img,
                (120, 120)
            )

            #------- desenha inimigo -------
            tela.blit(
                inimigo_menu,
                inimigo_menu.get_rect(
                    center=(
                        LARGURA // 2,
                        130 + offset_y
                    )
                )
            )

            #======= TÍTULO GAME OVER =======
            sombra = fonte_grande.render(
                "GAME OVER",
                True,
                (20,20,20)
            )

            tela.blit(
                sombra,
                sombra.get_rect(
                    center=(LARGURA//2 + 4, 224)
                )
            )

            #------- texto game over -------
            game_over = fonte_grande.render(
                "GAME OVER",
                True,
                (255,60,60)
            )

            tela.blit(
                game_over,
                game_over.get_rect(
                    center=(LARGURA//2, 220)
                )
            )

            #======= PAINEL CENTRAL =======
            pygame.draw.rect(
                tela,
                (20,30,60),
                (LARGURA//2 - 220, 290, 440, 190),
                border_radius=15
            )

            #------- borda vermelha -------
            pygame.draw.rect(
                tela,
                (255,60,60),
                (LARGURA//2 - 220, 290, 440, 190),
                2,
                border_radius=15
            )

            #------- pontuação -------
            pontos = fonte.render(
                f"Pontuacao: {pontuacao}",
                True,
                (255,255,255)
            )

            #------- recorde -------
            recorde_txt = fonte.render(
                f"Recorde: {recorde}",
                True,
                (255,255,0)
            )

            tela.blit(
                pontos,
                pontos.get_rect(
                    center=(LARGURA//2, 355)
                )
            )

            tela.blit(
                recorde_txt,
                recorde_txt.get_rect(
                    center=(LARGURA//2, 415)
                )
            )

            #------- texto piscando -------
            if pygame.time.get_ticks() % 1000 < 500:

                continuar = fonte.render(
                    "PRESSIONE QUALQUER TECLA",
                    True,
                    (255,255,255)
                )

                tela.blit(
                    continuar,
                    continuar.get_rect(
                        center=(LARGURA//2, 560)
                    )
                )

            #======= ATUALIZA TELA =======
            pygame.display.flip()
            relogio.tick(FPS)