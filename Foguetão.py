import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

#som
pygame.mixer.music.load("CornfieldChase.mp3")
pygame.mixer.music.set_volume(2.0)
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound("Colisao.mp3")
som_ponto = pygame.mixer.Sound("Ponto.mp3")
som_colisao.set_volume(0.2)
som_ponto.set_volume(0.2)

#os negocio da tela
LARGURA = 600
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Viagem ao Desconhecido")

fonte = pygame.font.SysFont(None, 36)
BRANCO = (255, 255, 255)
CINZA = (200, 200, 200)
PRETO = (0, 0, 40)

#imagens
fundo_img = pygame.image.load("Fundo.png")
fundo_img = pygame.transform.scale(fundo_img, (LARGURA, ALTURA))

frames_jogador = [
    pygame.image.load("Foguete1.png"),
    pygame.image.load("Foguete2.png"),
    pygame.image.load("Foguete3.png"),
    pygame.image.load("Foguete4.png")
]
frames_jogador = [pygame.transform.scale(img, (60, 70)) for img in frames_jogador]

meteoro_img_original = pygame.image.load("Meteoro.png")
meteoro_img_original = pygame.transform.scale(meteoro_img_original, (100, 100))

#lua
lua_img = pygame.image.load("Lua.png")
lua_img = pygame.transform.scale(lua_img, (200, 200))

#Menu
def menu_inicial():
    while True:
        TELA.fill(PRETO)
        titulo = fonte.render("Viagem ao Desconhecido ", True, BRANCO)
        jogar_texto = fonte.render("Decolar", True, PRETO)
        sair_texto = fonte.render("Abandonar", True, PRETO)

        jogar_rect = pygame.Rect(LARGURA//2 - 100, 300, 200, 50)
        sair_rect = pygame.Rect(LARGURA//2 - 100, 400, 200, 50)

        pygame.draw.rect(TELA, CINZA, jogar_rect)
        pygame.draw.rect(TELA, CINZA, sair_rect)

        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 150))
        TELA.blit(jogar_texto, (jogar_rect.centerx - jogar_texto.get_width()//2, jogar_rect.centery - jogar_texto.get_height()//2))
        TELA.blit(sair_texto, (sair_rect.centerx - sair_texto.get_width()//2, sair_rect.centery - sair_texto.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if jogar_rect.collidepoint(event.pos):
                    return
                if sair_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

#FIm
def fim():
    y_foguete = ALTURA - 100
    x_foguete = LARGURA // 2 - 30
    velocidade_subida = 3
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        TELA.blit(fundo_img, (0, 0))
        TELA.blit(lua_img, (LARGURA//2 - 100, 30))
        TELA.blit(frames_jogador[0], (x_foguete, y_foguete))
        y_foguete -= velocidade_subida

        if y_foguete < -100:
            texto_vitoria = fonte.render("Você chegou à Lua!", True, BRANCO)
            TELA.blit(texto_vitoria, (LARGURA//2 - texto_vitoria.get_width()//2, ALTURA//2))
            pygame.display.flip()
            pygame.time.wait(4000)
            return

        pygame.display.flip()
        clock.tick(60)

#código primcipal
def jogar():
    x_jogador = LARGURA // 2 - 25
    y_jogador = ALTURA - 80
    velocidade_jogador = 5

    x_obs = random.randint(50, LARGURA - 100)
    y_obs = -100
    velocidade_obs = 7

    pontos = 0
    clock = pygame.time.Clock()
    perdeu = False
    frame_atual = 0
    contador_frame = 0
    angulo = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if perdeu and event.type == pygame.KEYDOWN:
                pygame.mixer.music.play()
                return

        teclas = pygame.key.get_pressed()
        if not perdeu:
            if teclas[pygame.K_a] and x_jogador > 0:
                x_jogador -= velocidade_jogador
            if teclas[pygame.K_d] and x_jogador < LARGURA - 60:
                x_jogador += velocidade_jogador

            y_obs += velocidade_obs
            if y_obs > ALTURA:
                y_obs = -100
                x_obs = random.randint(50, LARGURA - 100)
                pontos += 1
                velocidade_obs += 0.3
                som_ponto.play()

            jogador_rect = pygame.Rect(x_jogador, y_jogador, 50, 60)
            obstaculo_rect = pygame.Rect(x_obs, y_obs, 80, 80)
            if jogador_rect.colliderect(obstaculo_rect):
                perdeu = True
                som_colisao.play()
                pygame.mixer.music.pause()

            contador_frame += 1
            if contador_frame >= 8:
                contador_frame = 0
                frame_atual = (frame_atual + 1) % len(frames_jogador)

            angulo = (angulo + 3) % 360
            meteoro_girando = pygame.transform.rotate(meteoro_img_original, angulo)
            rect_meteoro = meteoro_girando.get_rect(center=(x_obs + 50, y_obs + 50))

#fim do jogo
            if pontos >= 40:
                fim()
                return

        else:
            meteoro_girando = pygame.transform.rotate(meteoro_img_original, angulo)
            rect_meteoro = meteoro_girando.get_rect(center=(x_obs + 50, y_obs + 50))

        TELA.blit(fundo_img, (0, 0))
        TELA.blit(frames_jogador[frame_atual], (x_jogador, y_jogador))
        TELA.blit(meteoro_girando, rect_meteoro.topleft)

        texto_pontos = fonte.render(f"Desvios: {pontos}", True, BRANCO)
        TELA.blit(texto_pontos, (10, 10))

        if perdeu:
            texto_gameover = fonte.render("Missão Falhada! Pressione qualquer tecla.", True, BRANCO)
            TELA.blit(texto_gameover, (LARGURA//2 - texto_gameover.get_width()//2, ALTURA//2))

        pygame.display.flip()
        clock.tick(60)

#loop
while True:
    menu_inicial()
    jogar()
