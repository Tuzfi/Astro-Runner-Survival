
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

    # Boss 2 sprites
    boss2s1_img = pygame.image.load(asset("Boss2sprite1.png")).convert_alpha()
    boss2s1_img = pygame.transform.scale(boss2s1_img,(200,200))

    boss2s2_img = pygame.image.load(asset("Boss2Sprit2.png")).convert_alpha()
    boss2s2_img = pygame.transform.scale(boss2s2_img,(200,200))

    boss2final_img = pygame.image.load(asset("Boss2Final.png")).convert_alpha()
    boss2final_img = pygame.transform.scale(boss2final_img,(580,580))

    # Menu sprites
    logo_img = pygame.image.load(asset("Logo.png")).convert_alpha()
    logo_img = pygame.transform.scale(logo_img,(500, int(logo_img.get_height() * (500/logo_img.get_width()))))

    jogar_img = pygame.image.load(asset("JOGAr.png")).convert_alpha()
    jogar_img = pygame.transform.scale(jogar_img,(300,80))

    sair_img = pygame.image.load(asset("SAIR.png")).convert_alpha()
    sair_img = pygame.transform.scale(sair_img,(300,80))

    continuar_img = pygame.image.load(asset("continuar.png")).convert_alpha()
    continuar_img = pygame.transform.scale(continuar_img,(300,80))

    voltarmenu_img = pygame.image.load(asset("Voltar AO menu.png")).convert_alpha()
    voltarmenu_img = pygame.transform.scale(voltarmenu_img,(300,80))

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
    musica_boss2final = asset("Slayer - Raining Blood bossFight final.mp3")

    musica_atual = [None]

    def tocar_musica(caminho, loop=-1, volume=0.4, start=0.0):
        if musica_atual[0] == caminho and start == 0.0:
            return
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop, start=start)
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

    def desenhar_botao_sprite(img, cx, cy, selecionado):
        """Desenha um sprite de botão centralizado. Adiciona brilho/escala se selecionado."""
        if selecionado:
            # escala ligeiramente maior quando selecionado
            w = int(img.get_width() * 1.08)
            h = int(img.get_height() * 1.08)
            img_draw = pygame.transform.scale(img, (w, h))
            # overlay brilhante
            brilho = img_draw.copy()
            brilho.fill((80, 0, 180, 60), special_flags=pygame.BLEND_RGBA_ADD)
            img_draw.blit(brilho, (0,0))
        else:
            img_draw = img
        tela.blit(img_draw, (cx - img_draw.get_width()//2, cy - img_draw.get_height()//2))

    def desenhar_botao(rect, texto, selecionado, fonte_botao=fonte):
        cor_borda = ROXO if selecionado else CINZA_CLARO
        cor_fundo = (40,30,60) if selecionado else (25,25,35)
        pygame.draw.rect(tela, cor_fundo, rect, border_radius=10)
        pygame.draw.rect(tela, cor_borda, rect, width=3, border_radius=10)
        txt = fonte_botao.render(texto, True, BRANCO)
        tela.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def menu_principal():
        """Tela inicial do jogo com sprites. Retorna quando o jogador escolhe Jogar."""
        tocar_musica(musica_menu, volume=0.6)
        opcoes = ["Jogar", "Sair"]
        selecionado = 0

        sprites_botoes = [jogar_img, sair_img]
        cx = LARGURA // 2
        # posições Y dos botões
        btn_y = [420, 530]

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
                # clique do mouse nos botões
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    for i, y in enumerate(btn_y):
                        img = sprites_botoes[i]
                        rx = cx - img.get_width()//2
                        ry = y - img.get_height()//2
                        if rx <= mx <= rx+img.get_width() and ry <= my <= ry+img.get_height():
                            if i == 0:
                                return
                            else:
                                pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEMOTION:
                    mx2, my2 = pygame.mouse.get_pos()
                    for i, y in enumerate(btn_y):
                        img = sprites_botoes[i]
                        rx = cx - img.get_width()//2
                        ry = y - img.get_height()//2
                        if rx <= mx2 <= rx+img.get_width() and ry <= my2 <= ry+img.get_height():
                            selecionado = i

            desenhar_fundo()

            # Logo sprite
            tela.blit(logo_img, (cx - logo_img.get_width()//2, 80))

            rec_txt = fonte.render(f"Recorde: {recorde}", True, BRANCO)
            tela.blit(rec_txt, (cx - rec_txt.get_width()//2, 310))

            for i, (img, y) in enumerate(zip(sprites_botoes, btn_y)):
                desenhar_botao_sprite(img, cx, y, i == selecionado)

            dica = fonte_pequena.render("WASD para mover | Mouse para apontar | Botao esquerdo para atirar | ESC pausa", True, CINZA_CLARO)
            tela.blit(dica, (LARGURA//2 - dica.get_width()//2, ALTURA-50))

            mx,my = pygame.mouse.get_pos()
            tela.blit(mira_img,(mx-mira_img.get_width()//2, my-mira_img.get_height()//2))

            pygame.display.flip()
            relogio.tick(FPS)

    def menu_pausa():
        """Mostra o menu de pausa com sprites. Retorna 'continuar' ou 'menu'."""
        opcoes_txt = ["Continuar", "Voltar ao Menu", "Sair do Jogo"]
        sprites_pausa = [continuar_img, voltarmenu_img, None]  # None = botão texto para Sair
        selecionado = 0
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0,0,0,160))

        pygame.mixer.music.pause()

        cx = LARGURA // 2
        btn_y = [340, 450, 560]

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()
                        return "continuar"
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        selecionado = (selecionado+1) % len(opcoes_txt)
                    elif e.key in (pygame.K_UP, pygame.K_w):
                        selecionado = (selecionado-1) % len(opcoes_txt)
                    elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                        escolha = opcoes_txt[selecionado]
                        if escolha == "Continuar":
                            pygame.mixer.music.unpause()
                            return "continuar"
                        elif escolha == "Voltar ao Menu":
                            return "menu"
                        else:
                            pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    for i, y in enumerate(btn_y):
                        img = sprites_pausa[i]
                        if img:
                            rx = cx - img.get_width()//2
                            ry = y - img.get_height()//2
                            if rx <= mx <= rx+img.get_width() and ry <= my <= ry+img.get_height():
                                selecionado = i
                                if i == 0:
                                    pygame.mixer.music.unpause()
                                    return "continuar"
                                elif i == 1:
                                    return "menu"
                        else:
                            rect = pygame.Rect(cx-160, y-30, 320, 60)
                            if rect.collidepoint(mx, my):
                                pygame.quit(); sys.exit()
                if e.type == pygame.MOUSEMOTION:
                    mx2, my2 = pygame.mouse.get_pos()
                    for i, y in enumerate(btn_y):
                        img = sprites_pausa[i]
                        if img:
                            rx = cx - img.get_width()//2
                            ry = y - img.get_height()//2
                            if rx <= mx2 <= rx+img.get_width() and ry <= my2 <= ry+img.get_height():
                                selecionado = i
                        else:
                            rect = pygame.Rect(cx-160, y-30, 320, 60)
                            if rect.collidepoint(mx2, my2):
                                selecionado = i

            tela.blit(overlay, (0,0))

            titulo = fonte_grande.render("PAUSADO", True, BRANCO)
            tela.blit(titulo, (cx - titulo.get_width()//2, 200))

            for i, y in enumerate(btn_y):
                img = sprites_pausa[i]
                if img:
                    desenhar_botao_sprite(img, cx, y, i == selecionado)
                else:
                    rect = pygame.Rect(cx-160, y-30, 320, 60)
                    desenhar_botao(rect, opcoes_txt[i], i == selecionado)

            mx,my = pygame.mouse.get_pos()
            tela.blit(mira_img,(mx-mira_img.get_width()//2, my-mira_img.get_height()//2))

            pygame.display.flip()
            relogio.tick(FPS)

    def tela_upgrade(jogador):
        """Tela de escolha de upgrade. Aplica direto no jogador."""
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

    # ─── ANIMAÇÃO DE TRANSFORMAÇÃO DO BOSS 2 ────────────────────────────────────
    def animacao_boss2_transformacao(inimigos, tiros, tiros_inimigos, drops, jogador):
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
        Offset de início da música = 0:27 - 3.5s = 23.5s  → começa em 23.5s.
        """
        # Início da música alinhado para o drop cair em 0:27
        DURACAO_ANIM = 3.5          # segundos de animação visual
        MUSIC_OFFSET = 23.5         # começa a tocar daqui para o drop cair em 0:27
        SHAKE_DURACAO = 3.0         # tremor por 3 segundos
        FLASH_START = 3.0           # flash começa em 3s
        FLASH_DURACAO = 0.5         # duração do flash

        # Para a música atual e começa Slayer do offset
        musica_atual[0] = None  # força reload
        try:
            pygame.mixer.music.load(musica_boss2final)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1, start=MUSIC_OFFSET)
            musica_atual[0] = musica_boss2final
        except Exception:
            pass

        t_inicio = pygame.time.get_ticks()
        cx = LARGURA // 2
        cy = 200  # posição y do boss durante animação

        while True:
            agora = pygame.time.get_ticks()
            elapsed = (agora - t_inicio) / 1000.0  # segundos

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            # ── Tremor de tela ──────────────────────────────────────
            if elapsed < SHAKE_DURACAO:
                intensidade = int(18 * (1 - elapsed / SHAKE_DURACAO)) + 4
                shake_x = random.randint(-intensidade, intensidade)
                shake_y = random.randint(-intensidade, intensidade)
            else:
                shake_x, shake_y = 0, 0

            # ── Desenhar fundo ──────────────────────────────────────
            desenhar_fundo()

            # Aplica tremor: blit fundo em surface deslocado
            # (Usamos um surface de offset para simular)
            if shake_x != 0 or shake_y != 0:
                snap = tela.copy()
                tela.fill(FUNDO)
                tela.blit(snap, (shake_x, shake_y))

            # ── Sprite alternando ───────────────────────────────────
            if elapsed < FLASH_START:
                # alterna a cada 3 frames (~20Hz)
                frame_idx = int(elapsed * 20) % 2
                sprite_boss = boss2s1_img if frame_idx == 0 else boss2s2_img
                tela.blit(sprite_boss, (cx - sprite_boss.get_width()//2, cy - sprite_boss.get_height()//2))

            # ── Flash de explosão ───────────────────────────────────
            if elapsed >= FLASH_START:
                prog = (elapsed - FLASH_START) / FLASH_DURACAO  # 0→1
                if prog < 1.0:
                    alpha = int(255 * (1 - prog))
                    flash = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
                    flash.fill((255, 200, 80, alpha))
                    tela.blit(flash, (0,0))
                else:
                    # Animação terminou: retorna para o loop principal
                    return

            pygame.display.flip()
            relogio.tick(FPS)

    # ────────────────────────────────────────────────────────────────────────────

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
        upgrade_dado=False
        boss=None
        boss_derrotado=False
        boss2=None
        boss2_fase="fase1"          # "fase1" | "final"
        boss2_derrotado=False
        boss2_anim_feita=False

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

            # ── Spawn inimigos normais ───────────────────────────────────────────
            sem_boss_ativo = (boss is None) and (boss2 is None)
            nao_e_wave_boss1 = not (wave == 10 and not boss_derrotado)
            nao_e_wave_boss2 = not (wave == 20 and not boss2_derrotado)

            if sem_boss_ativo and nao_e_wave_boss1 and nao_e_wave_boss2:
                while spawnados < alvo_wave:
                    lado=random.randint(0,3)
                    if lado==0: x,y=random.randint(0,LARGURA),-50
                    elif lado==1: x,y=LARGURA+50,random.randint(0,ALTURA)
                    elif lado==2: x,y=random.randint(0,LARGURA),ALTURA+50
                    else: x,y=-50,random.randint(0,ALTURA)

                    inimigos.append({"x":x,"y":y,"vel":1.5+wave*0.2})
                    spawnados+=1

            # ── Boss 1 (wave 10) ─────────────────────────────────────────────────
            if wave == 10 and boss is None and not boss_derrotado:
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

            # ── Boss 2 (wave 20) — fase 1 ────────────────────────────────────────
            if wave == 20 and boss2 is None and not boss2_derrotado:
                if not boss2_anim_feita:
                    inimigos.clear()
                    tiros_inimigos.clear()
                    spawnados = alvo_wave
                    # Animação de transformação (bloqueia até terminar)
                    animacao_boss2_transformacao(inimigos, tiros, tiros_inimigos, drops, jogador)
                    boss2_anim_feita = True

                boss2 = {
                    "x": LARGURA/2, "y": -250,
                    "vida_fase1": 120,
                    "vida_fase1_max": 120,
                    "vida_final": 200,
                    "vida_final_max": 200,
                    "fase": "fase1",
                    "cooldown_tiro": 45,
                    "vel": 1.8,
                    # atributos extras para o boss final
                    "angulo_orbita": 0.0,
                    "cooldown_laser": 180,
                    "laser_ativo": False,
                    "laser_timer": 0,
                    "laser_ang": 0.0,
                    "dash_timer": 0,
                    "dash_dx": 0, "dash_dy": 0,
                    "rage_timer": 0,
                }
                inimigos.clear()
                spawnados = alvo_wave

            # ── Tiros do jogador ─────────────────────────────────────────────────
            for t in tiros[:]:
                t["x"]+=t["dx"]; t["y"]+=t["dy"]
                if t["x"]<0 or t["x"]>LARGURA or t["y"]<0 or t["y"]>ALTURA:
                    tiros.remove(t)

            # ── Inimigos normais ─────────────────────────────────────────────────
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

            # ── Boss 1 — lógica ──────────────────────────────────────────────────
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

            # ── Boss 2 — lógica ──────────────────────────────────────────────────
            if boss2 is not None:
                ticks = pygame.time.get_ticks()

                if boss2["fase"] == "fase1":
                    # Entrada: desce até y=180
                    if boss2["y"] < 180:
                        boss2["y"] += boss2["vel"]
                    else:
                        # Movimento senoidal duplo (mais errático que o boss1)
                        boss2["x"] += math.sin(ticks * 0.0015) * 2.8
                        boss2["y"] = 180 + math.sin(ticks * 0.0008) * 40

                    boss2["x"] = max(120, min(LARGURA-120, boss2["x"]))

                    # Tiro triplo em spread
                    if boss2["cooldown_tiro"] <= 0:
                        ang=math.atan2(jogador["y"]-boss2["y"], jogador["x"]-boss2["x"])
                        for delta in [-0.25, 0, 0.25]:
                            a = ang + delta
                            tiros_inimigos.append({"x":boss2["x"],"y":boss2["y"],"dx":math.cos(a)*9,"dy":math.sin(a)*9})
                        boss2["cooldown_tiro"] = 45
                        som_play(som_tiro)
                    else:
                        boss2["cooldown_tiro"] -= 1

                    # Tiros do jogador acertam boss2 fase1
                    for t in tiros[:]:
                        if math.hypot(t["x"]-boss2["x"], t["y"]-boss2["y"]) < 90:
                            if t in tiros: tiros.remove(t)
                            boss2["vida_fase1"] -= 1
                            som_play(som_explosao)
                            if boss2["vida_fase1"] <= 0:
                                # Transição para boss final
                                boss2["fase"] = "final"
                                boss2["y"] = 220
                                boss2["cooldown_tiro"] = 80
                                boss2["dash_timer"] = 0
                                boss2["rage_timer"] = 0
                                pontuacao += 500
                            break

                elif boss2["fase"] == "final":
                    # Boss Final — comportamento muito mais agressivo e criativo
                    boss2["angulo_orbita"] += 0.018
                    raio_x = 380
                    raio_y = 120
                    centro_x = LARGURA / 2
                    centro_y = 260
                    boss2["x"] = centro_x + math.cos(boss2["angulo_orbita"]) * raio_x
                    boss2["y"] = centro_y + math.sin(boss2["angulo_orbita"] * 1.7) * raio_y

                    # Dash em direção ao jogador periodicamente
                    boss2["dash_timer"] -= 1
                    if boss2["dash_timer"] <= 0:
                        ang_dash = math.atan2(jogador["y"]-boss2["y"], jogador["x"]-boss2["x"])
                        boss2["dash_dx"] = math.cos(ang_dash) * 14
                        boss2["dash_dy"] = math.sin(ang_dash) * 14
                        boss2["x"] += boss2["dash_dx"] * 8  # impulso do dash
                        boss2["y"] += boss2["dash_dy"] * 8
                        boss2["x"] = max(80, min(LARGURA-80, boss2["x"]))
                        boss2["y"] = max(80, min(ALTURA//2, boss2["y"]))
                        boss2["dash_timer"] = random.randint(220, 340)

                    # Tiro múltiplo em padrão circular (5 direções)
                    if boss2["cooldown_tiro"] <= 0:
                        vida_pct = boss2["vida_final"] / boss2["vida_final_max"]
                        n_tiros = 5 if vida_pct > 0.5 else 8  # mais tiros quando com pouca vida
                        for k in range(n_tiros):
                            a = (2 * math.pi / n_tiros) * k + boss2["angulo_orbita"]
                            vel_t = 9 if vida_pct > 0.5 else 11
                            tiros_inimigos.append({"x":boss2["x"],"y":boss2["y"],"dx":math.cos(a)*vel_t,"dy":math.sin(a)*vel_t})
                        # Tiro direto ao jogador
                        ang_j = math.atan2(jogador["y"]-boss2["y"], jogador["x"]-boss2["x"])
                        tiros_inimigos.append({"x":boss2["x"],"y":boss2["y"],"dx":math.cos(ang_j)*13,"dy":math.sin(ang_j)*13})
                        boss2["cooldown_tiro"] = 55 if vida_pct > 0.5 else 35
                        som_play(som_tiro)
                    else:
                        boss2["cooldown_tiro"] -= 1

                    # Rage: quando abaixo de 30% de vida, invoca mini inimigos
                    boss2["rage_timer"] -= 1
                    vida_pct = boss2["vida_final"] / boss2["vida_final_max"]
                    if vida_pct < 0.30 and boss2["rage_timer"] <= 0 and len(inimigos) < 6:
                        for _ in range(3):
                            lado = random.randint(0,3)
                            if lado==0: x,y=random.randint(0,LARGURA),-50
                            elif lado==1: x,y=LARGURA+50,random.randint(0,ALTURA)
                            elif lado==2: x,y=random.randint(0,LARGURA),ALTURA+50
                            else: x,y=-50,random.randint(0,ALTURA)
                            inimigos.append({"x":x,"y":y,"vel":3.0})
                        boss2["rage_timer"] = 180

                    # Tiros do jogador acertam boss2 final
                    for t in tiros[:]:
                        if math.hypot(t["x"]-boss2["x"], t["y"]-boss2["y"]) < 100:
                            if t in tiros: tiros.remove(t)
                            boss2["vida_final"] -= 1
                            som_play(som_explosao)
                            if boss2["vida_final"] <= 0:
                                pontuacao += 2000
                                boss2 = None
                                boss2_derrotado = True
                                inimigos.clear()
                                tocar_musica(musica_jogo, volume=0.6)
                            break

            # ── Tiros inimigos ───────────────────────────────────────────────────
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

            # ── Drops de vida ────────────────────────────────────────────────────
            for d in drops[:]:
                if math.hypot(d["x"]-jogador["x"], d["y"]-jogador["y"]) < 30:
                    jogador["vida_max"] += 1
                    jogador["vida"] += 1
                    drops.remove(d)

            # ── Avanço de wave ───────────────────────────────────────────────────
            sem_boss_ativo = (boss is None) and (boss2 is None)
            nao_e_wave_boss1 = not (wave == 10 and not boss_derrotado)
            nao_e_wave_boss2 = not (wave == 20 and not boss2_derrotado)

            if sem_boss_ativo and nao_e_wave_boss1 and nao_e_wave_boss2:
                if spawnados>=alvo_wave and len(inimigos)==0:
                    wave+=1
                    alvo_wave+=3
                    spawnados=0

                    # Upgrade na wave 9
                    if wave == 9 and not upgrade_dado:
                        tela_upgrade(jogador)
                        upgrade_dado = True

            if pontuacao>recorde:
                recorde=pontuacao
                salvar_recorde(recorde)

            if morreu:
                rodando_partida = False
                continue

            # ── RENDER ───────────────────────────────────────────────────────────
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

            # Boss 1
            if boss is not None:
                tela.blit(boss_img,(boss["x"]-80, boss["y"]-80))
                barra_largura=400
                vida_pct = boss["vida"]/boss["vida_max"]
                pygame.draw.rect(tela,(60,0,0),(LARGURA//2-barra_largura//2,30,barra_largura,18))
                pygame.draw.rect(tela,(220,30,30),(LARGURA//2-barra_largura//2,30,int(barra_largura*vida_pct),18))
                pygame.draw.rect(tela,BRANCO,(LARGURA//2-barra_largura//2,30,barra_largura,18),2)
                nome_boss = fonte_pequena.render("BOSS", True, BRANCO)
                tela.blit(nome_boss,(LARGURA//2-nome_boss.get_width()//2,8))

            # Boss 2
            if boss2 is not None:
                barra_largura = 600
                if boss2["fase"] == "fase1":
                    sprite = boss2s1_img
                    vida_pct = boss2["vida_fase1"] / boss2["vida_fase1_max"]
                    cor_barra = (200, 60, 200)
                    label = "BOSS II"
                else:
                    # Pulsa entre sprite1 e sprite2 do boss final
                    pulse = int(pygame.time.get_ticks() / 120) % 2
                    sprite = boss2final_img
                    vida_pct = boss2["vida_final"] / boss2["vida_final_max"]
                    # efeito de aura vermelha piscando no boss final
                    if int(pygame.time.get_ticks() / 200) % 2 == 0:
                        aura = pygame.Surface((sprite.get_width()+20, sprite.get_height()+20), pygame.SRCALPHA)
                        aura.fill((255, 0, 0, 40))
                        tela.blit(aura, (boss2["x"]-sprite.get_width()//2-10, boss2["y"]-sprite.get_height()//2-10))
                    cor_barra = (220, 20, 20)
                    label = " BOSS II FINAL "

                tela.blit(sprite, (int(boss2["x"]-sprite.get_width()//2), int(boss2["y"]-sprite.get_height()//2)))

                pygame.draw.rect(tela,(60,0,0),(LARGURA//2-barra_largura//2,30,barra_largura,22))
                pygame.draw.rect(tela,cor_barra,(LARGURA//2-barra_largura//2,30,int(barra_largura*vida_pct),22))
                pygame.draw.rect(tela,BRANCO,(LARGURA//2-barra_largura//2,30,barra_largura,22),2)
                nome_b2 = fonte_pequena.render(label, True, BRANCO)
                tela.blit(nome_b2,(LARGURA//2-nome_b2.get_width()//2,8))

            # HUD
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
