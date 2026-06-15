
import pygame, random, math, sys, os

LARGURA, ALTURA = 1280, 720
FPS = 60

def carregar_recorde():
    try:
        with open("recorde.txt","r",encoding="utf-8") as f:
            return int(f.read())
    except:
        return 0

def salvar_recorde(valor):
    with open("recorde.txt","w",encoding="utf-8") as f:
        f.write(str(valor))

def executar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Astro Runner Survival")
    relogio = pygame.time.Clock()

    fonte = pygame.font.SysFont(None, 42)
    fonte_grande = pygame.font.SysFont(None, 90)

    nave = pygame.image.load("assets/Voando.png").convert_alpha()
    nave = pygame.transform.scale(nave,(64,64))

    inimigo_img = pygame.image.load("assets/Inimigo.png").convert_alpha()
    inimigo_img = pygame.transform.scale(inimigo_img,(48,48))

    tiro_img = pygame.image.load("assets/Tiro.png").convert_alpha()
    tiro_img = pygame.transform.scale(tiro_img,(6,20))

    estrelas = [[random.randint(0,LARGURA), random.randint(0,ALTURA), random.randint(1,3)] for _ in range(150)]

    recorde = carregar_recorde()

    while True:
        # menu
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    break
            else:
                tela.fill((5,5,15))
                t=fonte_grande.render("ASTRO RUNNER",True,(255,255,255))
                tela.blit(t,(LARGURA//2-t.get_width()//2,180))
                tela.blit(fonte.render(f"Recorde: {recorde}",True,(255,255,255)),(500,320))
                tela.blit(fonte.render("Pressione qualquer tecla",True,(255,255,255)),(450,380))
                pygame.display.flip()
                relogio.tick(FPS)
                continue
            break

        jogador={"x":LARGURA/2,"y":ALTURA/2,"vida":3}
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

        while jogando:
            relogio.tick(FPS)

            mx, my = pygame.mouse.get_pos()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pausado = True

                if (
                    e.type == pygame.MOUSEBUTTONDOWN
                    and e.button == 3
                    and cooldown <= 0
                    and not pausado
                ):
                    ang = math.atan2(
                        my - jogador["y"],
                        mx - jogador["x"]
                    )

                    tiros.append({
                        "x": jogador["x"],
                        "y": jogador["y"],
                        "dx": math.cos(ang) * 12,
                        "dy": math.sin(ang) * 12,
                        "angulo": ang
                    })

                    cooldown = 12

            if pausado:
                while pausado:

                    for e in pygame.event.get():

                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if e.type == pygame.KEYDOWN:

                            if e.key == pygame.K_ESCAPE:
                                pausado = False

                            elif e.key == pygame.K_q:
                                pausado = False
                                jogando = False

                    tela.fill((5, 5, 15))

                    titulo = fonte_grande.render(
                        "PAUSADO",
                        True,
                        (255, 255, 0)
                    )

                    tela.blit(
                        titulo,
                        (
                            LARGURA // 2 - titulo.get_width() // 2,
                            180
                        )
                    )

                    tela.blit(
                        fonte.render(
                            "ESC - Continuar",
                            True,
                            (255, 255, 255)
                        ),
                        (500, 330)
                    )

                    tela.blit(
                        fonte.render(
                            "Q - Voltar ao menu",
                            True,
                            (255, 255, 255)
                        ),
                        (485, 390)
                    )

                    pygame.display.flip()
                    relogio.tick(FPS)

                continue

            jogador["x"] += (mx - jogador["x"]) * 0.12
            jogador["y"] += (my - jogador["y"]) * 0.12

            if cooldown > 0:
                cooldown -= 1

            if dano_timer > 0:
                dano_timer -= 1

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

                inimigos.append({
                    "x": x,
                    "y": y,
                    "vel": 1.5 + wave * 0.2
                })

                spawnados += 1

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

            for i in inimigos[:]:
                dx = jogador["x"] - i["x"]
                dy = jogador["y"] - i["y"]

                d = max(1, math.hypot(dx, dy))

                i["x"] += dx / d * i["vel"]
                i["y"] += dy / d * i["vel"]

                if d < 35 and dano_timer <= 0:
                    jogador["vida"] -= 1
                    dano_timer = 60

                    if jogador["vida"] <= 0:
                        jogando = False

            for t in tiros[:]:
                for i in inimigos[:]:
                    if math.hypot(
                        t["x"] - i["x"],
                        t["y"] - i["y"]
                    ) < 28:

                        if t in tiros:
                            tiros.remove(t)

                        if i in inimigos:
                            inimigos.remove(i)

                        pontuacao += 10
                        break

            if spawnados >= alvo_wave and len(inimigos) == 0:
                wave += 1
                alvo_wave += 3
                spawnados = 0

            if pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(recorde)

            tela.fill((5, 5, 15))

            for e in estrelas:
                pygame.draw.circle(
                    tela,
                    (255, 255, 255),
                    (int(e[0]), int(e[1])),
                    e[2]
                )

            angulo = -math.degrees(
                math.atan2(
                    my - jogador["y"],
                    mx - jogador["x"]
                )
            )

            nave_rot = pygame.transform.rotate(
                nave,
                angulo - 90
            )

            tela.blit(
                nave_rot,
                (
                    jogador["x"] - nave_rot.get_width() / 2,
                    jogador["y"] - nave_rot.get_height() / 2
                )
            )

            for t in tiros:
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

            for i in inimigos:
                tela.blit(
                    inimigo_img,
                    (i["x"] - 24, i["y"] - 24)
                )

            for v in range(jogador["vida"]):
                pygame.draw.circle(
                    tela,
                    (255, 0, 0),
                    (30 + v * 35, 30),
                    12
                )

            tela.blit(
                fonte.render(
                    f"Wave {wave}",
                    True,
                    (255, 255, 255)
                ),
                (10, 60)
            )

            tela.blit(
                fonte.render(
                    f"Pontos {pontuacao}",
                    True,
                    (255, 255, 255)
                ),
                (10, 100)
            )

            pygame.display.flip()
            

        # game over
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type==pygame.KEYDOWN:
                    break
            else:
                tela.fill((0,0,0))
                tela.blit(fonte_grande.render("GAME OVER",True,(255,0,0)),(420,220))
                tela.blit(fonte.render(f"Pontuacao: {pontuacao}",True,(255,255,255)),(520,340))
                tela.blit(fonte.render(f"Recorde: {recorde}",True,(255,255,255)),(530,390))
                tela.blit(fonte.render("Pressione qualquer tecla",True,(255,255,255)),(460,470))
                pygame.display.flip()
                continue
            break
