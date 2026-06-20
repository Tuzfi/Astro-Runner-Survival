#======= IMPORTAÇÃO DE BIBLIOTECAS =======
import pygame, random, math, sys, os

#======= CONFIGURAÇÕES GERAIS =======
LARGURA, ALTURA = 1280, 720
FPS = 60

#======= SISTEMA DE RECORDE =======
def carregar_recorde():
    try:
        with open("recorde.txt","r",encoding="utf-8") as f:
            return int(f.read())
    except:
        return 0

def salvar_recorde(valor):
    with open("recorde.txt","w",encoding="utf-8") as f:
        f.write(str(valor))

#======= FUNÇÃO PRINCIPAL DO JOGO =======
def executar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Astro Runner Survival")
    relogio = pygame.time.Clock()

    #======= FONTES =======
    fonte = pygame.font.SysFont(None, 42)
    fonte_grande = pygame.font.SysFont(None, 90)

    #======= CARREGAMENTO DE SPRITES =======
    nave = pygame.image.load("assets/Voando.png").convert_alpha()
    nave = pygame.transform.scale(nave,(64,64))

    inimigo_img = pygame.image.load("assets/Inimigo.png").convert_alpha()
    inimigo_img = pygame.transform.scale(inimigo_img,(48,48))

    tiro_img = pygame.image.load("assets/Tiro.png").convert_alpha()
    tiro_img = pygame.transform.scale(tiro_img,(6,20))

    #======= FUNDO ESTRELADO =======
    estrelas = [[random.randint(0,LARGURA), random.randint(0,ALTURA), random.randint(1,3)] for _ in range(150)]

    recorde = carregar_recorde()
    
    #======= LOOP PRINCIPAL DO PROGRAMA =======
    while True:

        #======= MENU =======
        while True:
            #======= EVENTOS DO MENU =======
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    break
            else:

                #======= FUNDO =======
                tela.fill((3, 5, 20))

                #======= ANIMAÇÃO DAS ESTRELAS =======
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

                #======= NAVE GIRANDO =======
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

                #======= SOMBRA DO TÍTULO =======
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

                #======= TÍTULO PRINCIPAL =======
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

                #======= TEXTO DO RECORDE =======
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

                #======= TEXTO PISCANDO =======
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

                pygame.display.flip()
                relogio.tick(FPS)
                continue
            break

        #======= INICIALIZAÇÃO DE NOVA PARTIDA =======
        jogador={"x":LARGURA/2,"y":ALTURA/2,"vida":3}
        tiros=[]
        inimigos=[]
        pontuacao=0
        wave=1
        alvo_wave=5
        spawnados=0
        cooldown=0
        dano_timer=0

        #======= CONTROLE DE ESTADOS =======
        jogando = True
        pausado = False
        sair_para_menu = False

        #======= LOOP PRINCIPAL DA PARTIDA =======
        while jogando:
            relogio.tick(FPS)

            mx, my = pygame.mouse.get_pos()

            #======= LEITURA DE EVENTOS =======
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #======= TECLADO =======
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pausado = True

                #======= DISPARO =======
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

            #======= SISTEMA DE PAUSA =======
            if pausado:
                while pausado:

                    #======= EVENTOS DA PAUSA =======
                    for e in pygame.event.get():

                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if e.type == pygame.KEYDOWN:

                            #------- ESC -> Continua o jogo -------
                            if e.key == pygame.K_ESCAPE:
                                pausado = False

                            #------- Q -> Volta ao menu -------
                            elif e.key == pygame.K_q:
                                pausado = False
                                sair_para_menu = True
                                jogando = False

                    #======= FUNDO =======
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

                    #======= NAVE GIRANDO =======
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

                    #======= SOMBRA =======
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

                    #======= TÍTULO =======
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

                    pygame.display.flip()
                    relogio.tick(FPS)

                continue

            #======= MOVIMENTO SUAVIZADO DA NAVE =======
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
                lado = random.randint(0, 3)

                if lado == 0:
                    x, y = random.randint(0, LARGURA), -50
                elif lado == 1:
                    x, y = LARGURA + 50, random.randint(0, ALTURA)
                elif lado == 2:
                    x, y = random.randint(0, LARGURA), ALTURA + 50
                else:
                    x, y = -50, random.randint(0, ALTURA)

                #======= CRIA O INIMIGO =======
                inimigos.append({
                    "x": x,
                    "y": y,
                    "vel": 1.5 + wave * 0.2
                })

                spawnados += 1

            #======= MOVIMENTO DOS TIROS =======
            for t in tiros[:]:
                t["x"] += t["dx"]
                t["y"] += t["dy"]

                if (
                    t["x"] < 0
                    or t["x"] > LARGURA
                    or t["y"] < 0
                    or t["y"] > ALTURA
                ):
                    tiros.remove(t)

            #======= IA DOS INIMIGOS =======
            for i in inimigos[:]:
                dx = jogador["x"] - i["x"]
                dy = jogador["y"] - i["y"]

                d = max(1, math.hypot(dx, dy))

                #======= MOVIMENTO DE PERSEGUIÇÃO =======
                i["x"] += dx / d * i["vel"]
                i["y"] += dy / d * i["vel"]

                #======= COLISÃO COM O JOGADOR =======
                if d < 35 and dano_timer <= 0:
                    #------- perde vida -------
                    jogador["vida"] -= 1
                    #------- ativa invencibilidade -------
                    dano_timer = 60

                    #------- game over -------
                    if jogador["vida"] <= 0:
                        jogando = False

            #======= COLISÃO TIRO X INIMIGO =======
            for t in tiros[:]:
                for i in inimigos[:]:
                    #------- distância entre os dois -------
                    if math.hypot(
                        t["x"] - i["x"],
                        t["y"] - i["y"]
                    ) < 28:

                        #------- remove o tiro -------
                        if t in tiros:
                            tiros.remove(t)

                        #------- remove inimigo -------
                        if i in inimigos:
                            inimigos.remove(i)

                        #------- ganha pontos -------
                        pontuacao += 10
                        break

            #======= SISTEMA DE WAVES =======
            if spawnados >= alvo_wave and len(inimigos) == 0:
                wave += 1
                alvo_wave += 3
                spawnados = 0

            #======= SISTEMA DE RECORDE =======
            if pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(recorde)

            tela.fill((5, 5, 15))

            #======= DESENHO DAS ESTRELAS =======
            for e in estrelas:

                e[1] += e[2] * (0.4 + e[2] * 0.3)

                if e[1] > ALTURA:
                    e[1] = 0
                    e[0] = random.randint(0, LARGURA)

                pygame.draw.circle(
                    tela,
                    (255, 255, 255),
                    (int(e[0]), int(e[1])),
                    e[2]
                )

            #======= CALCULA ROTAÇÃO DA NAVE =======
            angulo = -math.degrees(
                math.atan2(
                    my - jogador["y"],
                    mx - jogador["x"]
                )
            )

            #======= ROTACIONA A SPRITE DA NAVE =======
            nave_rot = pygame.transform.rotate(
                nave,
                angulo - 90
            )

            #======= DESENHA A NAVE =======
            tela.blit(
                nave_rot,
                (
                    jogador["x"] - nave_rot.get_width() / 2,
                    jogador["y"] - nave_rot.get_height() / 2
                )
            )

            #======= DESENHO DOS TIROS =======
            for t in tiros:
                #------- rotaciona os tiros na direção do disparo -------
                tiro_rot = pygame.transform.rotate(
                    tiro_img,
                    -math.degrees(t["angulo"]) - 90
                )

                tela.blit(
                    tiro_rot,
                    (
                        t["x"] - tiro_rot.get_width()/2,
                        t["y"] - tiro_rot.get_height()/2
                    )
                )

            #======= DESENHO DOS INIMIGOS =======
            for i in inimigos:
                tela.blit(
                    inimigo_img,
                    (i["x"] - 24, i["y"] - 24)
                )

            #======= SISTEMA ANTIGO DE VIDAS =======
            #------- este bloco desenha as vidas no canto, a config de HUD organiza -------
            for v in range(jogador["vida"]):
                pygame.draw.circle(
                    tela,
                    (255, 0, 0),
                    (30 + v * 35, 30),
                    12
                )

            #======= FUNDO DA HUD =======
            pygame.draw.rect(
                tela,
                (20, 30, 60),
                (10, 10, 200, 110),
                border_radius=12
            )

            #======= CONFIGURAÇÃO DA HUD =======
            hud_x = 10
            hud_y = 10
            hud_largura = 200
            hud_altura = 110

            vida_total = jogador["vida"]
            espaco = 20

            #======= CENTRALIZA AS VIDAS =======
            inicio_x = hud_x + hud_largura // 2 - (vida_total - 1) * espaco // 2
            y_vidas = hud_y + hud_altura - 15

            #======= DESENHA AS VIDAS =======
            for v in range(vida_total):
                pygame.draw.circle(
                    tela,
                    (255, 0, 0),
                    (inicio_x + v * espaco, y_vidas),
                    8
                )

            #======= TEXTO DA WAVE =======
            wave_txt = fonte.render(
                f"Wave {wave}",
                True,
                (255, 255, 255)
            )

            #======= TEXTO DOS PONTOS =======
            pontos_txt = fonte.render(
                f"Pontos {pontuacao}",
                True,
                (255, 255, 255)
            )

            #======= DESENHA TEXTO DA HUD =======
            tela.blit(wave_txt, (25, 25))
            tela.blit(pontos_txt, (25, 65))

            #======= ATUALIZA A TELA =======
            pygame.display.flip()

        #======= VOLTAR AO MENU =======
        #======= SE O JOGADOR ESCOLHER 'Q' DURANTE A PAUSA =======
        if sair_para_menu:
            jogando = False
            pausado = False
            continue

        #======= TELA DE GAME OVER =======
        while True:
            #======= EVENTOS =======
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type==pygame.KEYDOWN:
                    break
            else:
                #======= FUNDO =======
                tela.fill((3, 5, 20))

                #======= ESTRELAS ANIMADAS =======
                for estrela in estrelas:

                    #------- movimento lento -------
                    estrela[1] += estrela[2] * 0.15

                    if estrela[1] > ALTURA:
                        estrela[1] = 0
                        estrela[0] = random.randint(0, LARGURA)

                    pygame.draw.circle(
                        tela,
                        (255,255,255),
                        (int(estrela[0]), int(estrela[1])),
                        estrela[2]
                    )

                #======= ANIMAÇÃO DO INIMIGO =======

                #======= MOVIMENTO DE FLUTUAÇÃO =======
                offset_y = math.sin(
                    pygame.time.get_ticks() * 0.0025
                ) * 15

                #======= CRIA VERSÃO MAIOR DA SPRITE DO INIMIGO =======
                inimigo_menu = pygame.transform.scale(
                    inimigo_img,
                    (120, 120)
                )

                #======= DESENHA O INIMIGO =======
                tela.blit(
                    inimigo_menu,
                    inimigo_menu.get_rect(
                        center=(
                            LARGURA // 2,
                            130 + offset_y
                        )
                    )
                )

                #======= SOMBRA DO TÍTULO =======
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

                #======= TEXTO GAME OVER =======
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

                #======= BORDA VERMELHA =======
                pygame.draw.rect(
                    tela,
                    (255,60,60),
                    (LARGURA//2 - 220, 290, 440, 190),
                    2,
                    border_radius=15
                )

                #======= TEXTO DA PONTUAÇÃO =======
                pontos = fonte.render(
                    f"Pontuacao: {pontuacao}",
                    True,
                    (255,255,255)
                )

                #======= TEXTO DO RECORDE =======
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

                #======= TEXTO PISCANDO =======
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
                continue
            break