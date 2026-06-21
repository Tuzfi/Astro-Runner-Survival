import math
from src.config import LARGURA, ALTURA

#======= SISTEMA DE MOVIMENTO DOS TIROS =======
def atualizar_tiros(tiros):
    for t in tiros[:]:
        #------- movimento linear do tiro -------
        t["x"] += t["dx"]
        t["y"] += t["dy"]

        #------- remove se sair da tela -------
        if (
            t["x"] < 0
            or t["x"] > LARGURA
            or t["y"] < 0
            or t["y"] > ALTURA
        ):
            tiros.remove(t)

#======= SISTEMA DE MOVIMENTO DOS INIMIGOS =======
def atualizar_movimento_inimigos(inimigos, jogador):
    for i in inimigos:
        #------- direção até o jogador -------
        dx = jogador["x"] - i["x"]
        dy = jogador["y"] - i["y"]

        #------- normalização do vetor -------
        d = max(1, math.hypot(dx, dy))

        #------- movimento de perseguição -------
        i["x"] += dx / d * i["vel"]
        i["y"] += dy / d * i["vel"]

#======= SISTEMA DE COLISÃO JOGADOR =======
def checar_colisao_jogador(inimigos, jogador, dano_timer):
    for i in inimigos:
        dx = jogador["x"] - i["x"]
        dy = jogador["y"] - i["y"]

        d = math.hypot(dx, dy)

        #------- colisão por distância -------
        if d < 35 and dano_timer <= 0:
            return True

    return False

#======= SISTEMA DE COLISÃO TIRO X INIMIGO =======
def colisao_tiros(tiros, inimigos):
    pontuacao_ganha = 0

    for t in tiros[:]:
        for i in inimigos[:]:
            #------- distância entre tiro e inimigo -------
            if math.hypot(
                t["x"] - i["x"],
                t["y"] - i["y"]
            ) < 28:

                #------- remove tiro -------
                if t in tiros:
                    tiros.remove(t)

                #------- remove inimigo -------
                if i in inimigos:
                    inimigos.remove(i)

                #------- pontuação -------
                pontuacao_ganha += 10
                break

    return pontuacao_ganha

#======= SISTEMA DE WAVES =======
def atualizar_waves(spawnados, alvo_wave, inimigos):
    if spawnados >= alvo_wave and len(inimigos) == 0:
        return True
    return False