# Proposta Inicial do Jogo

## 1. Nome provisório do jogo

> Astro Runner: Survival

## 2. Integrantes do grupo

* Gabriel Otávio Assrany Nascimento
* Keven Henrique de Carvalho Lino
* Michael Willian Tang
* Iury Emanuel Alves da Silva

## 3. Tipo de jogo

Tipo escolhido pelo grupo:

> Jogo de sobrevivência espacial com elementos de ação e progressão.

## 4. Descrição geral do jogo

Descrição:

> O jogador controla uma nave espacial em um ambiente espacial repleto de inimigos e asteroides. O objetivo é sobreviver o maior tempo possível enquanto desvia dos perigos e elimina ameaças. 

## 5. Objetivo do jogador

Objetivo:

> Sobreviver o maior tempo possível enquanto evolui sua nave e enfrenta ondas crescentes de inimigos e obstáculos.

## 6. Regras principais

Regras do grupo:

* O jogador inicia a partida com uma quantidade limitada de vida.
* Asteroides e inimigos surgem continuamente durante a partida.
* Colisões ou ataques inimigos reduzem a vida da nave.
* A cada 60 segundos o jogador escolhe uma melhoria para sua nave.
* O jogo termina quando a vida da nave chegar a zero.

## 7. Condição de vitória

Condição de vitória:

> Não existe um final definido. O objetivo é sobreviver o máximo de tempo possível e alcançar a maior pontuação.

## 8. Condição de derrota ou encerramento

Condição de derrota ou encerramento:

> A partida termina quando a nave perde toda a sua vida.

## 9. Elementos previstos no jogo

### Jogador ou elemento principal

Descrição:

> Uma nave espacial controlada pelo jogador através do teclado.

### Obstáculos, inimigos ou desafios

Descrição:

> Asteroides e naves inimigas aparecem continuamente e tentam atingir o jogador.

### Itens, alvos ou objetos de interação

Descrição:

> Melhorias temporárias ou permanentes poderão ser obtidas durante a partida para fortalecer a nave.

### Pontuação, vidas, tempo ou progresso

Descrição:

> O tempo sobrevivido será utilizado como principal indicador de desempenho. O jogador possui uma barra de vida e recebe melhorias periódicas ao sobreviver.

## 10. Controles previstos

Controles do grupo:

* W, A, S e D ou setas direcionais: movimentar a nave.
* Mouse esquerdo: disparar.
* ESC: pausar ou sair do jogo.

## 11. Organização inicial do código

Organização planejada:

* `main.py`: inicia o jogo.
* `src/jogo.py`: contém o loop principal.
* `src/jogador.py`: controla a nave do jogador.
* `src/inimigos.py`: controla os inimigos.
* `src/asteroides.py`: controla os asteroides.
* `src/projeteis.py`: controla os disparos.
* `src/melhorias.py`: gerencia as melhorias.
* `src/config.py`: armazena configurações gerais.



## 12. Principais dificuldades esperadas

Dificuldades previstas:

* Implementação do sistema de melhorias.
* Controle de colisões entre diversos objetos.
* Balanceamento da dificuldade ao longo da partida.

## 13. Escopo mínimo para a entrega final

Escopo mínimo:

> A versão mínima do jogo terá uma nave controlada pelo teclado, movimentação dos inimigos e asteroides, sistema de colisão, barra de vida, disparos básicos, contador de tempo sobrevivido e tela de fim de jogo.

## 14. Possíveis melhorias, caso haja tempo

Melhorias possíveis:

* Sistema de ranking.
* Diferentes tipos de inimigos.
* Efeitos sonoros e trilha sonora.
* Animações de explosão.
* Sistema de fases.
* Bosses especiais.
* Menu principal e tela de pausa aprimorada.

## 15. Estruturas de dados que poderão ser utilizadas

Estruturas previstas:

* Listas para armazenar inimigos, asteroides e projéteis ativos na tela.
* Dicionários para armazenar atributos da nave, como vida, velocidade e dano.
* Variáveis numéricas para controlar pontuação, tempo sobrevivido e nível de dificuldade.
* Arquivos de texto ou JSON para armazenamento de recordes e configurações.

## 16. Uso previsto de arquivos

Uso previsto:

* Arquivo para salvar o recorde de maior tempo sobrevivido.
* Arquivo para armazenar configurações futuras do jogo.
* Pasta de recursos contendo imagens, sons e fontes utilizadas durante a execução.

## 17. Testes planejados

Testes previstos:

* Verificar a movimentação correta da nave.
* Testar colisões entre nave, inimigos, asteroides e projéteis.
* Validar o funcionamento do sistema de melhorias.
* Verificar se o sistema de pontuação registra corretamente o tempo sobrevivido.
* Testar o encerramento da partida quando a vida da nave chegar a zero.
