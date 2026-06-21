import math, random
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
def colisao_tiros(tiros, inimigos, particulas):
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
                    criar_explosao(
                        particulas,
                        i["x"],
                        i["y"]
                    )

                #------- pontuação -------
                pontuacao_ganha += 10
                break

    return pontuacao_ganha

#======= SISTEMA DE WAVES =======
def atualizar_waves(spawnados, alvo_wave, inimigos):
    if spawnados >= alvo_wave and len(inimigos) == 0:
        return True
    return False

#======= CRIA EXPLOSÃO =======
def criar_explosao(particulas, x, y):
    for _ in range(18):
        ang = random.uniform(0, math.pi * 2)
        vel = random.uniform(1, 5)

        particulas.append({
            "x": x,
            "y": y,
            "dx": math.cos(ang) * vel,
            "dy": math.sin(ang) * vel,
            "vida": random.randint(20,35),
            "cor": random.choice([
                (255, 200, 80),
                (255, 120, 50),
                (255, 60, 30)
            ]),
            "tamanho": random.randint(2,4)
        })

#======= ATUALIZA PARTÍCULAS =======
def atualizar_particulas(particulas):
    for p in particulas[:]:
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["dy"] += 0.1
        p["vida"] -= 1
        if p["vida"] <= 0:
            particulas.remove(p)