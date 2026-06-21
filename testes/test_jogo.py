"""
Testes automatizados — Astro Runner: Survival
Executar com: pytest tests/
"""

import math
import sys
import os
import types

# ---------------------------------------------------------------------------
# Stub do pygame: evita erro de importação em ambientes sem display
# ---------------------------------------------------------------------------
if "pygame" not in sys.modules:
    pygame_stub = types.ModuleType("pygame")
    pygame_stub.K_w = 119
    pygame_stub.K_s = 115
    pygame_stub.K_a = 97
    pygame_stub.K_d = 100
    sys.modules["pygame"] = pygame_stub

import pygame  # agora é o stub (ou o pygame real, se disponível)

# Garante que o pacote src seja encontrado a partir da raiz do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config
from src import jogador as mod_jogador
from src import inimigos as mod_inimigos
from src import projeteis as mod_projeteis
from src import persistencia


# ===========================================================================
# Utilitários
# ===========================================================================

def _mk_keys(w=False, s=False, a=False, d=False):
    """Cria um mapeamento de teclas para passar ao módulo jogador."""
    return {
        pygame.K_w: w,
        pygame.K_s: s,
        pygame.K_a: a,
        pygame.K_d: d,
    }


class _RecursosFake:
    """Substituto mínimo de Recursos para testes que precisam de sons."""
    class _Som:
        def play(self): pass
    som_explosao = _Som()
    def tocar_som(self, s): pass


def _aplicar_upgrade(jogador, tipo):
    """Replica a lógica de aplicação de upgrade de melhorias.py."""
    if tipo == "tiros":
        jogador["tiros_extra"] += 2
    else:
        jogador["vida_max"] += 2
        jogador["vida"] += 2


# ===========================================================================
# 1. MOVIMENTAÇÃO DA NAVE
# ===========================================================================

class TestMovimentacao:
    """Verifica que a nave se move nas quatro direções e respeita os limites."""

    def test_move_cima(self):
        j = mod_jogador.criar_jogador()
        y_antes = j["y"]
        mod_jogador.mover(j, _mk_keys(w=True))
        assert j["y"] < y_antes, "Pressionar W deve mover a nave para cima (y diminui)."

    def test_move_baixo(self):
        j = mod_jogador.criar_jogador()
        y_antes = j["y"]
        mod_jogador.mover(j, _mk_keys(s=True))
        assert j["y"] > y_antes, "Pressionar S deve mover a nave para baixo (y aumenta)."

    def test_move_esquerda(self):
        j = mod_jogador.criar_jogador()
        x_antes = j["x"]
        mod_jogador.mover(j, _mk_keys(a=True))
        assert j["x"] < x_antes, "Pressionar A deve mover a nave para a esquerda (x diminui)."

    def test_move_direita(self):
        j = mod_jogador.criar_jogador()
        x_antes = j["x"]
        mod_jogador.mover(j, _mk_keys(d=True))
        assert j["x"] > x_antes, "Pressionar D deve mover a nave para a direita (x aumenta)."

    def test_sem_tecla_nao_move(self):
        j = mod_jogador.criar_jogador()
        x_antes, y_antes = j["x"], j["y"]
        mod_jogador.mover(j, _mk_keys())
        assert j["x"] == x_antes and j["y"] == y_antes, \
            "Sem teclas pressionadas a nave não deve se mover."

    def test_diagonal_normalizado(self):
        """Movimento diagonal não deve ser mais rápido que o cardinal."""
        j = mod_jogador.criar_jogador()
        x_antes, y_antes = j["x"], j["y"]
        vel = 5.5
        mod_jogador.mover(j, _mk_keys(w=True, d=True), vel=vel)
        distancia = math.hypot(j["x"] - x_antes, j["y"] - y_antes)
        assert abs(distancia - vel) < 0.01, \
            f"Movimento diagonal deve ter magnitude {vel}, obteve {distancia:.4f}."

    def test_limite_borda_superior_esquerda(self):
        j = mod_jogador.criar_jogador()
        j["x"] = 0
        j["y"] = 0
        for _ in range(20):
            mod_jogador.mover(j, _mk_keys(w=True, a=True))
        assert j["x"] >= 20, "Nave não deve sair pela borda esquerda."
        assert j["y"] >= 20, "Nave não deve sair pela borda superior."

    def test_limite_borda_inferior_direita(self):
        j = mod_jogador.criar_jogador()
        j["x"] = config.LARGURA
        j["y"] = config.ALTURA
        for _ in range(20):
            mod_jogador.mover(j, _mk_keys(s=True, d=True))
        assert j["x"] <= config.LARGURA - 20, "Nave não deve sair pela borda direita."
        assert j["y"] <= config.ALTURA - 20, "Nave não deve sair pela borda inferior."


# ===========================================================================
# 2. SISTEMA DE DISPARO
# ===========================================================================

class TestDisparo:
    """Verifica criação e movimento dos tiros do jogador."""

    def test_atirar_cria_tiro(self):
        j = mod_jogador.criar_jogador()
        tiros = mod_jogador.atirar(j, j["x"] + 100, j["y"])
        assert len(tiros) == 1, "Disparo padrão deve criar exatamente 1 tiro."

    def test_tiro_tem_campos_necessarios(self):
        j = mod_jogador.criar_jogador()
        tiro = mod_jogador.atirar(j, j["x"] + 100, j["y"])[0]
        for campo in ("x", "y", "dx", "dy"):
            assert campo in tiro, f"Tiro deve ter o campo '{campo}'."

    def test_tiro_parte_da_posicao_do_jogador(self):
        j = mod_jogador.criar_jogador()
        tiro = mod_jogador.atirar(j, j["x"] + 100, j["y"])[0]
        assert tiro["x"] == j["x"] and tiro["y"] == j["y"], \
            "Tiro deve partir da posição atual da nave."

    def test_tiros_extras_aumentam_quantidade(self):
        j = mod_jogador.criar_jogador()
        j["tiros_extra"] = 2
        tiros = mod_jogador.atirar(j, j["x"] + 100, j["y"])
        assert len(tiros) == 3, \
            "Com tiros_extra=2 devem ser criados 3 tiros (1 base + 2 extras)."

    def test_tiro_removido_apos_sair_da_tela(self):
        j = mod_jogador.criar_jogador()
        tiros = mod_jogador.atirar(j, j["x"] + 100, j["y"])
        tiros[0]["x"] = config.LARGURA + 100
        mod_jogador.atualizar_tiros(tiros)
        assert len(tiros) == 0, "Tiro fora da tela deve ser removido."

    def test_tiro_dentro_da_tela_nao_removido(self):
        j = mod_jogador.criar_jogador()
        tiros = mod_jogador.atirar(j, j["x"] + 100, j["y"])
        mod_jogador.atualizar_tiros(tiros)
        assert len(tiros) == 1, "Tiro dentro da tela não deve ser removido."


# ===========================================================================
# 3. COLISÕES COM INIMIGOS
# ===========================================================================

class TestColisoes:
    """Testa colisão de tiros com inimigos e de inimigos com o jogador."""

    def test_tiro_elimina_inimigo_proximo(self):
        tiros = [{"x": 100.0, "y": 100.0, "dx": 0, "dy": 0}]
        inimigos = [{"x": 105.0, "y": 100.0, "vel": 1.5}]  # distância < 28
        drops = []
        pontos = mod_inimigos.colidir_com_tiros(tiros, inimigos, drops, _RecursosFake())
        assert len(inimigos) == 0, "Tiro próximo ao inimigo deve eliminá-lo."
        assert pontos == 10, "Cada inimigo eliminado deve valer 10 pontos."

    def test_tiro_longe_nao_elimina_inimigo(self):
        tiros = [{"x": 100.0, "y": 100.0, "dx": 0, "dy": 0}]
        inimigos = [{"x": 300.0, "y": 300.0, "vel": 1.5}]  # distância >> 28
        drops = []
        mod_inimigos.colidir_com_tiros(tiros, inimigos, drops, _RecursosFake())
        assert len(inimigos) == 1, "Tiro longe do inimigo não deve eliminá-lo."

    def test_inimigo_causa_dano_ao_colidir(self):
        j = mod_jogador.criar_jogador()
        vida_antes = j["vida"]
        inimigos = [{"x": j["x"], "y": j["y"], "vel": 0}]
        mod_inimigos.atualizar(inimigos, j, 0, _RecursosFake())
        assert j["vida"] < vida_antes, \
            "Inimigo em cima da nave deve causar dano ao jogador."

    def test_dano_timer_evita_dano_repetido(self):
        j = mod_jogador.criar_jogador()
        inimigos = [{"x": j["x"], "y": j["y"], "vel": 0}]
        mod_inimigos.atualizar(inimigos, j, 60, _RecursosFake())
        assert j["vida"] == 3, \
            "Com dano_timer ativo o jogador não deve sofrer dano."

    def test_drop_vida_aumenta_atributos(self):
        j = mod_jogador.criar_jogador()
        j["vida"] = 2
        drops = [{"x": j["x"], "y": j["y"]}]
        mod_inimigos.coletar_drops(drops, j)
        assert j["vida_max"] == 4, "Drop deve aumentar vida_max em 1."
        assert j["vida"] == 3, "Drop deve curar 1 ponto de vida."
        assert len(drops) == 0, "Drop coletado deve ser removido da lista."


# ===========================================================================
# 4. ENCERRAMENTO DO JOGO (VIDA ZERO)
# ===========================================================================

class TestVidaZero:
    """Verifica que o jogo detecta corretamente a morte do jogador."""

    def test_vida_zero_sinaliza_morte(self):
        j = mod_jogador.criar_jogador()
        j["vida"] = 1
        inimigos = [{"x": j["x"], "y": j["y"], "vel": 0}]
        _, morreu = mod_inimigos.atualizar(inimigos, j, 0, _RecursosFake())
        assert morreu, "Jogador com 1 de vida ao sofrer dano deve ter morreu=True."

    def test_projetil_boss_mata_jogador_fraco(self):
        """Projéteis de boss causam 2 de dano; valida que vida ≤ 0 é morte."""
        j = mod_jogador.criar_jogador()
        j["vida"] = 1
        tiros_inimigos = [{"x": j["x"], "y": j["y"], "dx": 0, "dy": 0}]
        _, morreu = mod_projeteis.atualizar(tiros_inimigos, j, 0, _RecursosFake(), dano=2)
        assert morreu, \
            "Projétil de boss (dano 2) em jogador com 1 de vida deve sinalizar morte."

    def test_vida_acima_de_zero_nao_sinaliza_morte(self):
        j = mod_jogador.criar_jogador()
        j["vida"] = 2
        inimigos = [{"x": j["x"], "y": j["y"], "vel": 0}]
        _, morreu = mod_inimigos.atualizar(inimigos, j, 0, _RecursosFake())
        assert not morreu, \
            "Jogador com vida restante após dano não deve ter morreu=True."


# ===========================================================================
# 5. SISTEMA DE MELHORIAS
# ===========================================================================

class TestMelhorias:
    """Verifica que os upgrades alteram corretamente os atributos do jogador."""

    def test_upgrade_tiros_aumenta_tiros_extra(self):
        j = mod_jogador.criar_jogador()
        extra_antes = j["tiros_extra"]
        _aplicar_upgrade(j, "tiros")
        assert j["tiros_extra"] == extra_antes + 2, \
            "Upgrade de tiros deve adicionar 2 ao tiros_extra."

    def test_upgrade_vida_aumenta_vida_max(self):
        j = mod_jogador.criar_jogador()
        vida_max_antes = j["vida_max"]
        _aplicar_upgrade(j, "vida")
        assert j["vida_max"] == vida_max_antes + 2, \
            "Upgrade de vida deve adicionar 2 à vida_max."

    def test_upgrade_vida_cura_jogador(self):
        j = mod_jogador.criar_jogador()
        j["vida"] = 1
        _aplicar_upgrade(j, "vida")
        assert j["vida"] == 3, \
            "Upgrade de vida deve curar o jogador em 2 pontos de vida."

    def test_upgrades_tiros_acumulam(self):
        j = mod_jogador.criar_jogador()
        _aplicar_upgrade(j, "tiros")
        _aplicar_upgrade(j, "tiros")
        assert j["tiros_extra"] == 4, \
            "Dois upgrades de tiros devem acumular para tiros_extra=4."

    def test_upgrade_tiros_gera_tiros_adicionais(self):
        j = mod_jogador.criar_jogador()
        _aplicar_upgrade(j, "tiros")
        tiros = mod_jogador.atirar(j, j["x"] + 100, j["y"])
        assert len(tiros) == 3, \
            "Após upgrade de tiros, atirar deve gerar 3 projéteis."


# ===========================================================================
# 6. PERSISTÊNCIA (RECORDE)
# ===========================================================================

class TestPersistencia:
    """Testa leitura e gravação do recorde em arquivo."""

    def test_salvar_e_carregar_recorde(self, tmp_path, monkeypatch):
        caminho = str(tmp_path / "recorde.txt")
        monkeypatch.setattr(persistencia, "_caminho_recorde", lambda: caminho)
        persistencia.salvar_recorde(42)
        assert persistencia.carregar_recorde() == 42, \
            "Recorde salvo deve ser recuperado corretamente."

    def test_carregar_recorde_inexistente_retorna_zero(self, tmp_path, monkeypatch):
        caminho = str(tmp_path / "nao_existe.txt")
        monkeypatch.setattr(persistencia, "_caminho_recorde", lambda: caminho)
        assert persistencia.carregar_recorde() == 0, \
            "Recorde não encontrado deve retornar 0."

    def test_novo_recorde_sobrescreve_anterior(self, tmp_path, monkeypatch):
        caminho = str(tmp_path / "recorde.txt")
        monkeypatch.setattr(persistencia, "_caminho_recorde", lambda: caminho)
        persistencia.salvar_recorde(100)
        persistencia.salvar_recorde(250)
        assert persistencia.carregar_recorde() == 250, \
            "Salvar novo recorde deve sobrescrever o anterior."
