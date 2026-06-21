# Código-fonte (`src`)

Esta pasta contém os módulos principais do jogo, separados por
responsabilidade.

## Arquivos

- `jogo.py`: orquestrador — loop principal, eventos, ordem de
  atualização e renderização de cada frame. Não tem regra de jogo
  própria, só chama os outros módulos na ordem certa.
- `config.py`: constantes globais (tamanho da tela, FPS, cores) e o
  caminho base do projeto.
- `persistencia.py`: leitura/gravação do recorde em `recorde.txt`.
- `recursos.py`: carregamento de imagens, sons, músicas e fontes
  (classes `Recursos` e `Fontes`), além de `tocar_musica`/`tocar_som`.
- `jogador.py`: estado da nave, movimento (WASD), disparo e desenho.
- `inimigos.py`: spawn, perseguição, colisões e drops de vida dos
  inimigos comuns.
- `projeteis.py`: tiros inimigos (disparados pelos bosses) — movimento,
  colisão com o jogador e desenho.
- `melhorias.py`: tela de escolha de upgrade (wave 9).
- `interface.py`: fundo estrelado, botões, menu principal, menu de
  pausa, tela de game over e HUD da partida.
- `bosses/`: um arquivo por boss.
  - `boss1.py`: boss da wave 10.
  - `boss2.py`: boss da wave 20 (fase 1, fase final e a animação de
    transformação entre elas).

## Como adicionar um boss novo

1. Crie `bosses/boss3.py` com `criar()`, `atualizar(...)` e
   `desenhar(...)` seguindo o padrão de `boss1.py`/`boss2.py`.
2. Importe em `jogo.py` (`from .bosses import boss3`) e chame nos
   pontos equivalentes aos do boss1/boss2 dentro do loop principal.
