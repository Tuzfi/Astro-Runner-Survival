import pygame
import sys
import math

LARGURA = 600
ALTURA = 600
FPS = 24
BRANCO = (255, 255, 255)
AZUL = (50, 120, 220)
VERMELHO = (220, 50, 50)
CINZA_ESCURO = (30, 30, 30)


def criar_jogador():
    return {"x": LARGURA // 2, "y": ALTURA // 2, "raio": 18, "velocidade": 5}


def criar_obstaculo():
    return {"x": 0, "y": 300, "raio": 14, "velocidade": 3}


def mover_jogador(jogador, teclas):
    if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jogador["x"] - jogador["raio"] > 0:
        jogador["x"] -= jogador["velocidade"]
    if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jogador["x"] + jogador["raio"] < LARGURA:
        jogador["x"] += jogador["velocidade"]
    if (teclas[pygame.K_UP] or teclas[pygame.K_w]) and jogador["y"] - jogador["raio"] > 0:
        jogador["y"] -= jogador["velocidade"]
    if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and jogador["y"] + jogador["raio"] < ALTURA:
        jogador["y"] += jogador["velocidade"]


def mover_obstaculo(obs, jogador):
    dx = jogador["x"] - obs["x"]
    dy = jogador["y"] - obs["y"]
    distancia = math.hypot(dx, dy)
    if distancia != 0:
        obs["x"] += (dx / distancia) * obs["velocidade"]
        obs["y"] += (dy / distancia) * obs["velocidade"]


def colidiu(jogador, obs):
    distancia = math.hypot(jogador["x"] - obs["x"], jogador["y"] - obs["y"])
    return distancia < jogador["raio"] + obs["raio"]


def desenhar(tela, jogador, obs):
    tela.fill(CINZA_ESCURO)
    pygame.draw.circle(tela, AZUL, (int(jogador["x"]), int(jogador["y"])), jogador["raio"])
    pygame.draw.circle(tela, VERMELHO, (int(obs["x"]), int(obs["y"])), obs["raio"])


def executar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Astro Runner: Survival")
    relogio = pygame.time.Clock()

    jogador = criar_jogador()
    obstaculo = criar_obstaculo()

    while True:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        mover_jogador(jogador, teclas)
        mover_obstaculo(obstaculo, jogador)

        if colidiu(jogador, obstaculo):
            jogador = criar_jogador()
            obstaculo = criar_obstaculo()

        desenhar(tela, jogador, obs=obstaculo)
        pygame.display.flip()


if __name__ == "__main__":
    executar_jogo()
