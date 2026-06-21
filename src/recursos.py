"""
Carregamento centralizado de tudo que vem da pasta assets/: sprites,
sons, músicas e fontes — além das funções para tocar música/som.

Precisa ser instanciado DEPOIS de pygame.display.set_mode(), pois usa
convert_alpha() nas imagens.
"""

import os

import pygame

from . import config


class Fontes:
    def __init__(self):
        self.pequena = pygame.font.SysFont(None, 28)
        self.normal = pygame.font.SysFont(None, 42)
        self.media = pygame.font.SysFont(None, 56)
        self.grande = pygame.font.SysFont(None, 90)


class Recursos:
    def __init__(self):
        self.assets_dir = os.path.join(config.caminho_base(), "assets")
        self._musica_atual = None

        self._carregar_imagens()
        self._carregar_sons()
        self._carregar_musicas()

    def asset(self, nome):
        return os.path.join(self.assets_dir, nome)

    # ── Imagens ──────────────────────────────────────────────────────────
    def _carregar_imagens(self):
        def carregar(nome, tamanho):
            img = pygame.image.load(self.asset(nome)).convert_alpha()
            return pygame.transform.scale(img, tamanho)

        self.nave_img = carregar("Voando.png", (64, 64))
        self.inimigo_img = carregar("Inimigo.png", (48, 48))
        self.tiro_img = carregar("Tiro.png", (18, 40))
        self.mira_img = carregar("Mira.png", (40, 40))
        self.coracao_img = carregar("coracao.png", (32, 32))
        self.boss_img = carregar("boss.png", (160, 160))

        # Boss 2
        self.boss2s1_img = carregar("Boss2sprite1.png", (200, 200))
        self.boss2s2_img = carregar("Boss2Sprit2.png", (200, 200))
        self.boss2final_img = carregar("Boss2Final.png", (580, 580))

        # Menu
        logo_bruto = pygame.image.load(self.asset("Logo.png")).convert_alpha()
        altura_logo = int(logo_bruto.get_height() * (500 / logo_bruto.get_width()))
        self.logo_img = pygame.transform.scale(logo_bruto, (500, altura_logo))

        self.jogar_img = carregar("JOGAr.png", (300, 80))
        self.sair_img = carregar("SAIR.png", (300, 80))
        self.continuar_img = carregar("continuar.png", (300, 80))
        self.voltarmenu_img = carregar("Voltar AO menu.png", (300, 80))

    # ── Sons ─────────────────────────────────────────────────────────────
    def _carregar_som(self, nome, volume=1.0):
        try:
            s = pygame.mixer.Sound(self.asset(nome))
            s.set_volume(volume)
            return s
        except Exception:
            return None

    def _carregar_sons(self):
        self.som_tiro = self._carregar_som("blaster.mp3", 0.15)
        self.som_explosao = self._carregar_som(
            "8 Bit bomb explosion - Sound Effect.mp3", 0.2
        )

    def tocar_som(self, som):
        if som is not None:
            som.play()

    # ── Músicas ──────────────────────────────────────────────────────────
    def _carregar_musicas(self):
        self.musica_menu = self.asset("Deftones - Change 8bi Musica Menu.mp3")
        self.musica_jogo = self.asset(
            "GOJIRA - In The Wilderness 8 bit Musica de fundo do jogo.mp3"
        )
        self.musica_boss = self.asset("Deftones - elite 8bit Musica do boss.mp3")
        self.musica_boss2final = self.asset(
            "Slayer - Raining Blood bossFight final.mp3"
        )

    def tocar_musica(self, caminho, loop=-1, volume=0.4, start=0.0):
        if self._musica_atual == caminho and start == 0.0:
            return
        try:
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loop, start=start)
            self._musica_atual = caminho
        except Exception:
            pass

    def forcar_recarga_musica(self):
        """Usado quando uma música é trocada via pygame.mixer.music direto
        (ex: animação do boss2), para que tocar_musica() não ache que ela
        já está tocando."""
        self._musica_atual = None
