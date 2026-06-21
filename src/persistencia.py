"""
Leitura e gravação do recorde de pontuação em recorde.txt.
"""

import os

from . import config


def _caminho_recorde():
    return os.path.join(config.caminho_base(), "recorde.txt")


def carregar_recorde():
    try:
        with open(_caminho_recorde(), "r", encoding="utf-8") as f:
            return int(f.read())
    except Exception:
        return 0


def salvar_recorde(valor):
    with open(_caminho_recorde(), "w", encoding="utf-8") as f:
        f.write(str(valor))
