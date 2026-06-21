import random, math
from src.config import LARGURA, ALTURA

#======= CRIA O JOGADOR =======
def criar_jogador():
    return {
        "x": LARGURA / 2,
        "y": ALTURA / 2,
        "vida": 3
    }

#======= CRIA UM TIRO =======
def criar_tiro(jogador, mx, my):

    #------- calcula ângulo entre jogador e mouse -------
    ang = math.atan2(
        my - jogador["y"],
        mx - jogador["x"]
    )

    #------- retorna estrutura do tiro -------
    return {
        "x": jogador["x"],
        "y": jogador["y"],
        "dx": math.cos(ang) * 12,
        "dy": math.sin(ang) * 12,
        "angulo": ang
    }

#======= CRIA INIMIGO =======
def criar_inimigo(wave):
    lado = random.randint(0, 3)

    #------- esquerda / direita / cima / baixo -------
    if lado == 0:
        x, y = random.randint(0, LARGURA), -50
    elif lado == 1:
        x, y = LARGURA + 50, random.randint(0, ALTURA)
    elif lado == 2:
        x, y = random.randint(0, LARGURA), ALTURA + 50
    else:
        x, y = -50, random.randint(0, ALTURA)

    #------- inimigo escala com wave -------
    return {
        "x": x,
        "y": y,
        "vel": 1.5 + wave * 0.2
    }