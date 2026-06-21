import pygame, random, sys
from src.config import LARGURA, ALTURA, FPS

#======= TELA DE PAUSA =======
def pause_screen(tela, relogio, fonte, fonte_grande, nave, estrelas):
    pausado = True

    #======= LOOP DA TELA DE PAUSA =======
    while pausado:

        #------- input -------
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #------- teclado -------
            if e.type == pygame.KEYDOWN:

                #------- ESC -> Continua o jogo -------
                if e.key == pygame.K_ESCAPE:
                    return "continuar"

                #------- Q -> Volta ao menu -------
                elif e.key == pygame.K_q:
                    return "menu"

        #======= BACKGROUND =======
        tela.fill((3, 5, 20))

        #======= ESTRELAS ANIMADAS =======
        for estrela in estrelas:

            estrela[1] += estrela[2] * 0.15

            if estrela[1] > ALTURA:
                estrela[1] = 0
                estrela[0] = random.randint(0, LARGURA)

            pygame.draw.circle(
                tela,
                (255, 255, 255),
                (int(estrela[0]), int(estrela[1])),
                estrela[2]
            )

        #======= NAVE ANIMADA =======
        angulo_pause = pygame.time.get_ticks() * 0.03

        nave_pause = pygame.transform.rotozoom(
            nave,
            angulo_pause,
            2
        )

        tela.blit(
            nave_pause,
            (
                LARGURA // 2 - nave_pause.get_width() // 2,
                100
            )
        )

        #======= TÍTULO: PAUSADO =======
        sombra = fonte_grande.render(
            "PAUSADO",
            True,
            (20, 20, 20)
        )

        tela.blit(
            sombra,
            sombra.get_rect(
                center=(LARGURA // 2 + 4, 244)
            )
        )

        titulo = fonte_grande.render(
            "PAUSADO",
            True,
            (255, 220, 0)
        )

        tela.blit(
            titulo,
            titulo.get_rect(
                center=(LARGURA // 2, 240)
            )
        )

        #======= PAINEL CENTRAL =======
        pygame.draw.rect(
            tela,
            (20, 30, 60),
            (LARGURA // 2 - 220, 300, 440, 170),
            border_radius=15
        )

        #======= OPÇÕES =======
        txt_continuar = fonte.render(
            "ESC - Continuar",
            True,
            (255, 255, 255)
        )

        txt_menu = fonte.render(
            "Q - Voltar ao menu",
            True,
            (255, 255, 255)
        )

        tela.blit(
            txt_continuar,
            txt_continuar.get_rect(
                center=(LARGURA // 2, 350)
            )
        )

        tela.blit(
            txt_menu,
            txt_menu.get_rect(
                center=(LARGURA // 2, 410)
            )
        )

        #======= TEXTO PISCANDO =======
        if pygame.time.get_ticks() % 1000 < 500:

            aviso = fonte.render(
                "JOGO PAUSADO",
                True,
                (180, 180, 180)
            )

            tela.blit(
                aviso,
                aviso.get_rect(
                    center=(LARGURA // 2, 540)
                )
            )

        #======= UPDATE DA TELA =======
        pygame.display.flip()
        relogio.tick(FPS)