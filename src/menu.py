import pygame, random, sys
from src.config import LARGURA, ALTURA, FPS

#======= TELA DE MENU =======
def menu(tela, relogio, fonte, fonte_grande, nave, estrelas, recorde):
        waiting = True

        #======= LOOP DO MENU =======
        while waiting:

            #------- input do menu -------
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    waiting = False
            else:

                #------- render base -------
                tela.fill((3, 5, 20))

                #======= BACKGROUND =======
                for estrela in estrelas:

                    estrela[1] += estrela[2] * 0.3

                    if estrela[1] > ALTURA:
                        estrela[1] = 0
                        estrela[0] = random.randint(0, LARGURA)

                    pygame.draw.circle(
                        tela,
                        (255, 255, 255),
                        (int(estrela[0]), int(estrela[1])),
                        estrela[2]
                    )

                #======= ANIMAÇÃO DA NAVE =======
                angulo_menu = pygame.time.get_ticks() * 0.05

                nave_menu = pygame.transform.rotozoom(
                    nave,
                    angulo_menu,
                    2
                )

                tela.blit(
                    nave_menu,
                    (
                        LARGURA // 2 - nave_menu.get_width() // 2,
                        120
                    )
                )

                #======= TÍTULO =======
                sombra = fonte_grande.render(
                    "ASTRO RUNNER",
                    True,
                    (20, 20, 20)
                )

                tela.blit(
                    sombra,
                    sombra.get_rect(
                        center=(LARGURA // 2 + 4, 264)
                    )
                )

                titulo = fonte_grande.render(
                    "ASTRO RUNNER",
                    True,
                    (80, 220, 255)
                )

                tela.blit(
                    titulo,
                    titulo.get_rect(
                        center=(LARGURA // 2, 260)
                    )
                )

                #======= CAIXA DO RECORDE =======
                pygame.draw.rect(
                    tela,
                    (20, 30, 60),
                    (LARGURA // 2 - 160, 320, 320, 60),
                    border_radius=12
                )

                txt_recorde = fonte.render(
                    f"RECORDE: {recorde}",
                    True,
                    (255, 255, 0)
                )

                tela.blit(
                    txt_recorde,
                    txt_recorde.get_rect(
                        center=(LARGURA // 2, 350)
                    )
                )

                #------- texto piscando -------
                if pygame.time.get_ticks() % 1000 < 500:

                    txt_inicio = fonte.render(
                        "PRESSIONE QUALQUER TECLA",
                        True,
                        (255, 255, 255)
                    )

                    tela.blit(
                        txt_inicio,
                        txt_inicio.get_rect(
                            center=(LARGURA // 2, 450)
                        )
                    )

                #======= CONTROLES =======
                fonte_pequena = pygame.font.SysFont(None, 28)

                controles = fonte_pequena.render(
                    "Mouse = mover | Botao direito = atirar | ESC = pausa",
                    True,
                    (180, 180, 180)
                )

                tela.blit(
                    controles,
                    controles.get_rect(
                        center=(LARGURA // 2, 620)
                    )
                )

                #======= UPDATE FINAL =======
                pygame.display.flip()
                relogio.tick(FPS)
                continue
            break