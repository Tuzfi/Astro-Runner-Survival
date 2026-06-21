import pygame

#======= CARREGAMENTO DE SPRITES DO JOGO =======
def carregar_sprites():

    #------- sprite da nave do jogador -------
    nave = pygame.image.load("assets/Voando.png").convert_alpha()
    nave = pygame.transform.scale(nave, (64, 64))

    #------- sprite do inimigo -------
    inimigo_img = pygame.image.load("assets/Inimigo.png").convert_alpha()
    inimigo_img = pygame.transform.scale(inimigo_img, (48, 48))

    #------- sprite do tiro -------
    tiro_img = pygame.image.load("assets/Tiro.png").convert_alpha()
    tiro_img = pygame.transform.scale(tiro_img, (6, 20))

    #------- retorno dos sprites -------
    return nave, inimigo_img, tiro_img