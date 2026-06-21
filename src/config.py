"""
Configurações e constantes gerais do jogo.

Qualquer valor que precise ser ajustado globalmente (tamanho da tela,
FPS, paleta de cores) fica centralizado aqui para não ficar espalhado
pelos outros módulos.
"""

import os

LARGURA, ALTURA = 1920, 1080
FPS = 60

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
CINZA_CLARO = (120, 120, 140)
VERDE = (80, 220, 120)
ROXO = (170, 90, 255)
FUNDO = (5, 5, 15)


def caminho_base():
    """Pasta raiz do projeto (um nível acima de src/)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
