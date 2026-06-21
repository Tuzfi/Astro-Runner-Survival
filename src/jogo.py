
import pygame, random, math, sys, os

LARGURA, ALTURA = 1920, 1080
FPS = 60

BRANCO=(255,255,255)
VERMELHO=(255,0,0)
AMARELO=(255,255,0)
CINZA_CLARO=(120,120,140)
VERDE=(80,220,120)
ROXO=(170,90,255)
FUNDO=(5,5,15)

def caminho_base():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def carregar_recorde():
    try:
        with open(os.path.join(caminho_base(),"recorde.txt"),"r",encoding="utf-8") as f:
            return int(f.read())
    except:
        return 0

def salvar_recorde(valor):
    with open(os.path.join(caminho_base(),"recorde.txt"),"w",encoding="utf-8") as f:
        f.write(str(valor))


def executar_jogo():
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        pass

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Astro Runner Survival")
    relogio = pygame.time.Clock()

    fonte_pequena = pygame.font.SysFont(None, 28)
    fonte = pygame.font.SysFont(None, 42)
    fonte_media = pygame.font.SysFont(None, 56)
    fonte_grande = pygame.font.SysFont(None, 90)

    base = caminho_base()
    assets = os.path.join(base, "assets")

    def asset(nome):
        return os.path.join(assets, nome)

    nave_img = pygame.image.load(asset("Voando.png")).convert_alpha()
    nave_img = pygame.transform.scale(nave_img,(64,64))

    inimigo_img = pygame.image.load(asset("Inimigo.png")).convert_alpha()
    inimigo_img = pygame.transform.scale(inimigo_img,(48,48))

    tiro_img = pygame.image.load(asset("Tiro.png")).convert_alpha()
    tiro_img = pygame.transform.scale(tiro_img,(18,40))

    mira_img = pygame.image.load(asset("Mira.png")).convert_alpha()
    mira_img = pygame.transform.scale(mira_img,(40,40))

    coracao_img = pygame.image.load(asset("coracao.png")).convert_alpha()
    coracao_img = pygame.transform.scale(coracao_img,(32,32))

    boss_img = pygame.image.load(asset("boss.png")).convert_alpha()
    boss_img = pygame.transform.scale(boss_img,(160,160))


    def carregar_som(nome, volume=1.0):
        try:
            s = pygame.mixer.Sound(asset(nome))
            s.set_volume(volume)
            return s
        except Exception:
            return None

    som_tiro = carregar_som("blaster.mp3", 0.15)
    som_explosao = carregar_som("8 Bit bomb explosion - Sound Effect.mp3", 0.2)

    musica_menu = asset("Deftones - Change 8bi Musica Menu.mp3")
    musica_jogo = asset("GOJIRA - In The Wilderness 8 bit Musica de fundo do jogo.mp3")
    musica_boss = asset("Deftones - elite 8bit Musica do boss.mp3")

    musica_atual = [None]

    def tocar_musica(caminho, loop=-1, volume=0.4):
        if musica_atual[0] == caminho:
            return
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop)
            musica_atual[0] = caminho
        except Exception:
            pass

    def som_play(som):
        if som is not None:
            som.play()

    estrelas = [[random.randint(0,LARGURA), random.randint(0,ALTURA), random.randint(1,3)] for _ in range(150)]

    recorde = carregar_recorde()

    pygame.mouse.set_visible(False)



    def desenhar_fundo():
        tela.fill(FUNDO)
        for e in estrelas:
            pygame.draw.circle(tela,BRANCO,(int(e[0]),int(e[1])),e[2])
            e[1]+=0.3
            if e[1]>ALTURA:
                e[1]=0
                e[0]=random.randint(0,LARGURA)

    def desenhar_botao(rect, texto, selecionado, fonte_botao=fonte):
        cor_borda = ROXO if selecionado else CINZA_CLARO
        cor_fundo = (40,30,60) if selecionado else (25,25,35)
        pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
        pygame.draw.rect(tela, cor_borda, rect, width=3, border_radius=10)
        txt = fonte_botao.render(texto, True, BRANCO)
        tela.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def menu_principal():
        """Tela inicial do jogo. Retorna quando o jogador escolhe Jogar."""
        tocar_musica(musica_menu, volume=0.6)
        opcoes = ["Jogar", "Sair"]
        selecionado = 0

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_DOWN, pygame.K_s):
                        selecionado = (selecionado+1) % len(opcoes)
                    elif e.key in (pygame.K_UP, pygame.K_w):
                        selecionado = (selecionado-1) % len(opcoes)
                    elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if opcoes[selecionado] == "Jogar":
                            return
                        else:
                            pygame.quit(); sys.exit()
                    elif e.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

            desenhar_fundo()

            titulo = fonte_grande.render("ASTRO RUNNER", True, BRANCO)
            tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 100))
            sub = fonte_media.render("SURVIVAL", True, ROXO)
            tela.blit(sub, (LARGURA//2 - sub.get_width()//2, 190))

            rec_txt = fonte.render(f"Recorde: {recorde}", True, BRANCO)
            tela.blit(rec_txt, (LARGURA//2 - rec_txt.get_width()//2, 290))

            largura_botao, altura_botao = 300, 60
            for i, op in enumerate(opcoes):
                rect = pygame.Rect(LARGURA//2 - largura_botao//2, 380 + i*80, largura_botao, altura_botao)
                desenhar_botao(rect, op, i == selecionado)

            dica = fonte_pequena.render("WASD para mover | Mouse para apontar | Botao esquerdo para atirar | ESC pausa", True, CINZA_CLARO)
            tela.blit(dica, (LARGURA//2 - dica.get_width()//2, ALTURA-50))

            mx,my = pygame.mouse.get_pos()
            tela.blit(mira_img,(mx-mira_img.get_width()//2, my-mira_img.get_height()//2))

            pygame.display.flip()
            relogio.tick(FPS)

    def menu_pausa():
        """Mostra o menu de pausa. Retorna 'continuar' ou 'menu'."""
        opcoes = ["Continuar", "Voltar ao Menu", "Sair do Jogo"]
        selecionado = 0
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0,0,0,160))

        pygame.mixer.music.pause()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        return "continuar"
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        selecionado = (selecionado+1) % len(opcoes)
                    elif e.key in (pygame.K_UP, pygame.K_w):
                        selecionado = (selecionado-1) % len(opcoes)
                    elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                        escolha = opcoes[selecionado]
                        if escolha == "Continuar":
                            pygame.mixer.music.unpause()
                            return "continuar"
                        elif escolha == "Voltar ao Menu":
                            return "menu"
                        else:
                            pygame.quit(); sys.exit()

            tela.blit(overlay, (0,0))

            titulo = fonte_grande.render("PAUSADO", True, BRANCO)
            tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 140))

            largura_botao, altura_botao = 320, 60
            for i, op in enumerate(opcoes):
                rect = pygame.Rect(LARGURA//2 - largura_botao//2, 300 + i*80, largura_botao, altura_botao)
                desenhar_botao(rect, op, i == selecionado)

            mx,my = pygame.mouse.get_pos()
            tela.blit(mira_img,(mx-mira_img.get_width()//2, my-mira_img.get_height()//2))

            pygame.display.flip()
            relogio.tick(FPS)

    def tela_upgrade(jogador):
        """Tela de escolha de upgrade na wave 10. Aplica direto no jogador."""
        opcoes = [
            ("+2 Tiros", "tiros"),
            ("+2 Coracoes", "vida"),
        ]
        selecionado = 0

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_LEFT, pygame.K_a):
                        selecionado = (selecionado-1) % len(opcoes)
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):
                        selecionado = (selecionado+1) % len(opcoes)
                    elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                        tipo = opcoes[selecionado][1]
                        if tipo == "tiros":
                            jogador["tiros_extra"] += 2
                        else:
                            jogador["vida_max"] += 2
                            jogador["vida"] += 2
                        return

            overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            desenhar_fundo()
            tela.blit(overlay,(0,0))

            titulo = fonte_media.render("Escolha um upgrade!", True, BRANCO)
            tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 150))

            largura_card, altura_card = 320, 220
            espaco = 60
            inicio_x = LARGURA//2 - (largura_card*2 + espaco)//2
            for i, (texto, tipo) in enumerate(opcoes):
                rect = pygame.Rect(inicio_x + i*(largura_card+espaco), 260, largura_card, altura_card)
                cor_borda = ROXO if i == selecionado else CINZA_CLARO
                cor_fundo = (40,30,60) if i == selecionado else (25,25,35)
                pygame.draw.rect(tela, cor_fundo, rect, border_radius=14)
                pygame.draw.rect(tela, cor_borda, rect, width=4, border_radius=14)

                if tipo == "tiros":
                    tela.blit(tiro_img, (rect.centerx - 30, rect.top+40))
                    tela.blit(tiro_img, (rect.centerx + 12, rect.top+40))
                else:
                    tela.blit(coracao_img, (rect.centerx - 40, rect.top+50))
                    tela.blit(coracao_img, (rect.centerx + 8, rect.top+50))

                txt = fonte.render(texto, True, BRANCO)
                tela.blit(txt, (rect.centerx - txt.get_width()//2, rect.bottom-60))

            dica = fonte_pequena.render("Use A/D ou Setas para escolher e ENTER para confirmar", True, CINZA_CLARO)
            tela.blit(dica, (LARGURA//2 - dica.get_width()//2, ALTURA-60))

            pygame.display.flip()
            relogio.tick(FPS)

    def tela_game_over(pontuacao, recorde):
        while True:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type==pygame.KEYDOWN:
                    return
                if e.type==pygame.MOUSEBUTTONDOWN:
                    return

            tela.fill((0,0,0))
            tela.blit(fonte_grande.render("GAME OVER",True,VERMELHO),(LARGURA//2-220,220))
            txt1 = fonte.render(f"Pontuacao: {pontuacao}",True,BRANCO)
            tela.blit(txt1,(LARGURA//2-txt1.get_width()//2,340))
            txt2 = fonte.render(f"Recorde: {recorde}",True,BRANCO)
            tela.blit(txt2,(LARGURA//2-txt2.get_width()//2,390))
            txt3 = fonte.render("Pressione qualquer tecla para voltar ao menu",True,BRANCO)
            tela.blit(txt3,(LARGURA//2-txt3.get_width()//2,470))
            pygame.display.flip()
            relogio.tick(FPS)



    while True:
        menu_principal()

        jogador = {
            "x": LARGURA/2, "y": ALTURA/2,
            "vida": 3, "vida_max": 3,
            "tiros_extra": 0,
        }
        tiros=[]
        tiros_inimigos=[]
        inimigos=[]
        drops=[]
        pontuacao=0
        wave=1
        alvo_wave=5
        spawnados=0
        cooldown=0
        dano_timer=0
        upgrade_dado_wave15=False
        boss=None
        boss_derrotado=False

        tocar_musica(musica_jogo, volume=0.6)

        rodando_partida = True
        morreu = False

        while rodando_partida:
            relogio.tick(FPS)

            mx,my=pygame.mouse.get_pos()

            teclas = pygame.key.get_pressed()
            vel_nave = 5.5

            mover_x, mover_y = 0, 0
            if teclas[pygame.K_w]: mover_y -= 1
            if teclas[pygame.K_s]: mover_y += 1
            if teclas[pygame.K_a]: mover_x -= 1
            if teclas[pygame.K_d]: mover_x += 1

            if mover_x != 0 or mover_y != 0:
                norm = math.hypot(mover_x, mover_y)
                jogador["x"] += (mover_x/norm) * vel_nave
                jogador["y"] += (mover_y/norm) * vel_nave

            jogador["x"] = max(20, min(LARGURA-20, jogador["x"]))
            jogador["y"] = max(20, min(ALTURA-20, jogador["y"]))

            pausar = False
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    pygame.quit(); sys.exit()

                if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                    pausar = True

                if e.type==pygame.MOUSEBUTTONDOWN and e.button==1 and cooldown<=0:
                    ang=math.atan2(my-jogador["y"], mx-jogador["x"])
                    quantidade_tiros = 1 + jogador["tiros_extra"]
                    espalhamento = 0.12

                    if quantidade_tiros == 1:
                        angulos = [ang]
                    else:
                        angulos = [
                            ang + (i - (quantidade_tiros-1)/2) * espalhamento
                            for i in range(quantidade_tiros)
                        ]

                    for a in angulos:
                        tiros.append({"x":jogador["x"],"y":jogador["y"],"dx":math.cos(a)*12,"dy":math.sin(a)*12})

                    som_play(som_tiro)
                    cooldown=12

            if pausar:
                resultado = menu_pausa()
                if resultado == "menu":
                    rodando_partida = False
                    continue

            if cooldown>0: cooldown-=1
            if dano_timer>0: dano_timer-=1

            if boss is None and not (wave == 16 and not boss_derrotado):
                while spawnados < alvo_wave:
                    lado=random.randint(0,3)
                    if lado==0: x,y=random.randint(0,LARGURA),-50
                    elif lado==1: x,y=LARGURA+50,random.randint(0,ALTURA)
                    elif lado==2: x,y=random.randint(0,LARGURA),ALTURA+50
                    else: x,y=-50,random.randint(0,ALTURA)

                    inimigos.append({"x":x,"y":y,"vel":1.5+wave*0.2})
                    spawnados+=1

            if wave == 16 and boss is None and not boss_derrotado:
                boss = {
                    "x": LARGURA/2, "y": -200,
                    "vida": 75,
                    "vida_max": 75,
                    "cooldown_tiro": 60,
                    "vel": 1.2,
                }
                inimigos.clear()
                spawnados = alvo_wave
                tocar_musica(musica_boss, volume=1)

            for t in tiros[:]:
                t["x"]+=t["dx"]; t["y"]+=t["dy"]
                if t["x"]<0 or t["x"]>LARGURA or t["y"]<0 or t["y"]>ALTURA:
                    tiros.remove(t)

            for i in inimigos[:]:
                dx=jogador["x"]-i["x"]
                dy=jogador["y"]-i["y"]
                d=max(1, math.hypot(dx,dy))
                i["x"]+=dx/d*i["vel"]
                i["y"]+=dy/d*i["vel"]

                if d<35 and dano_timer<=0:
                    jogador["vida"]-=1
                    dano_timer=60
                    som_play(som_explosao)
                    if jogador["vida"]<=0:
                        morreu = True

            for t in tiros[:]:
                for i in inimigos[:]:
                    if math.hypot(t["x"]-i["x"], t["y"]-i["y"])<28:
                        if t in tiros: tiros.remove(t)
                        if i in inimigos: inimigos.remove(i)
                        pontuacao+=10
                        som_play(som_explosao)
                        if random.randint(1,14)==1:
                            drops.append({"x":i["x"],"y":i["y"]})
                        break

            if boss is not None:
                if boss["y"] < 150:
                    boss["y"] += boss["vel"]
                else:
                    boss["x"] += math.sin(pygame.time.get_ticks()*0.001) * 2

                boss["x"] = max(100, min(LARGURA-100, boss["x"]))

                if boss["cooldown_tiro"] <= 0:
                    ang=math.atan2(jogador["y"]-boss["y"], jogador["x"]-boss["x"])
                    tiros_inimigos.append({"x":boss["x"],"y":boss["y"],"dx":math.cos(ang)*8,"dy":math.sin(ang)*8})
                    boss["cooldown_tiro"] = 55
                    som_play(som_tiro)
                else:
                    boss["cooldown_tiro"] -= 1

                for t in tiros[:]:
                    if math.hypot(t["x"]-boss["x"], t["y"]-boss["y"]) < 70:
                        if t in tiros: tiros.remove(t)
                        boss["vida"] -= 1
                        som_play(som_explosao)
                        if boss["vida"] <= 0:
                            pontuacao += 1000
                            boss = None
                            boss_derrotado = True
                            tocar_musica(musica_jogo, volume=0.6)
                        break

            for t in tiros_inimigos[:]:
                t["x"]+=t["dx"]; t["y"]+=t["dy"]
                if t["x"]<0 or t["x"]>LARGURA or t["y"]<0 or t["y"]>ALTURA:
                    tiros_inimigos.remove(t)
                    continue
                if math.hypot(t["x"]-jogador["x"], t["y"]-jogador["y"]) < 16 and dano_timer<=0:
                    jogador["vida"] -= 2
                    dano_timer = 60
                    som_play(som_explosao)
                    tiros_inimigos.remove(t)
                    if jogador["vida"] <= 0:
                        morreu = True

           
            for d in drops[:]:
                if math.hypot(d["x"]-jogador["x"], d["y"]-jogador["y"]) < 30:
                    jogador["vida_max"] += 1
                    jogador["vida"] += 1
                    drops.remove(d)

           
            if boss is None and not (wave == 16 and not boss_derrotado):
                if spawnados>=alvo_wave and len(inimigos)==0:
                    wave+=1
                    alvo_wave+=3
                    spawnados=0

                    if wave == 10 and not upgrade_dado_wave15:
                        tela_upgrade(jogador)
                        upgrade_dado_wave15 = True

            if pontuacao>recorde:
                recorde=pontuacao
                salvar_recorde(recorde)

            if morreu:
                rodando_partida = False
                continue

    
            desenhar_fundo()

            angulo=-math.degrees(math.atan2(my-jogador["y"], mx-jogador["x"]))
            nave_rot = pygame.transform.rotate(nave_img, angulo-90)
            tela.blit(nave_rot,(jogador["x"]-nave_rot.get_width()/2,jogador["y"]-nave_rot.get_height()/2))

            for t in tiros:
                ang_tiro = -math.degrees(math.atan2(t["dy"], t["dx"]))
                tiro_rot = pygame.transform.rotate(tiro_img, ang_tiro-90)
                tela.blit(tiro_rot,(t["x"]-tiro_rot.get_width()/2, t["y"]-tiro_rot.get_height()/2))

            for t in tiros_inimigos:
                pygame.draw.circle(tela,(255,80,80),(int(t["x"]),int(t["y"])),6)

            for i in inimigos:
                tela.blit(inimigo_img,(i["x"]-24,i["y"]-24))

            for d in drops:
                tela.blit(coracao_img,(d["x"]-16,d["y"]-16))

            if boss is not None:
                tela.blit(boss_img,(boss["x"]-80, boss["y"]-80))
                barra_largura=400
                vida_pct = boss["vida"]/boss["vida_max"]
                pygame.draw.rect(tela,(60,0,0),(LARGURA//2-barra_largura//2,30,barra_largura,18))
                pygame.draw.rect(tela,(220,30,30),(LARGURA//2-barra_largura//2,30,int(barra_largura*vida_pct),18))
                pygame.draw.rect(tela,BRANCO,(LARGURA//2-barra_largura//2,30,barra_largura,18),2)
                nome_boss = fonte_pequena.render("BOSS", True, BRANCO)
                tela.blit(nome_boss,(LARGURA//2-nome_boss.get_width()//2,8))

            for v in range(jogador["vida_max"]):
                pos_x = 30+v*36
                if v < jogador["vida"]:
                    tela.blit(coracao_img,(pos_x,20))
                else:
                    cinza_coracao = coracao_img.copy()
                    cinza_coracao.fill((70,70,70,180), special_flags=pygame.BLEND_RGBA_MULT)
                    tela.blit(cinza_coracao,(pos_x,20))

            tela.blit(fonte.render(f"Wave {wave}",True,BRANCO),(10,65))
            tela.blit(fonte.render(f"Pontos {pontuacao}",True,BRANCO),(10,105))

            if jogador["tiros_extra"] > 0:
                tela.blit(fonte_pequena.render(f"Tiros extras: {jogador['tiros_extra']}",True,VERDE),(10,150))

            tela.blit(mira_img,(mx-mira_img.get_width()//2, my-mira_img.get_height()//2))

            pygame.display.flip()

        if morreu:
            tocar_musica(musica_menu, volume=0.6)
            tela_game_over(pontuacao, recorde)
