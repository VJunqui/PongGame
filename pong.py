import pygame
import sys
import random

# Inicialização
pygame.init()
pygame.mixer.init()  # Inicializa o mixer de áudio

try:
    pygame.mixer.music.load("sounds/8bitmusic.mp3")  # substitua pelo nome do seu arquivo
    pygame.mixer.music.play(-1)  # -1 para tocar em loop infinito
except pygame.error as e:
    print(f"Erro ao carregar música: {e}")

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong com IA, Dificuldades e Cores")
fonte = pygame.font.SysFont("Arial", 36)

# Definindo cores personalizadas (RGB)
COR_FUNDO = (30, 30, 60)          # Fundo azul escuro
COR_RAQUETE_1 = (255, 100, 100)  # Raquete jogador 1 vermelho claro
COR_RAQUETE_2 = (100, 255, 100)  # Raquete IA verde claro
COR_BOLA = (255, 255, 0)          # Bola amarela
COR_LINHA = (200, 200, 200)       # Linha central cinza clara
COR_TEXTO = (255, 255, 255)       # Texto branco

# Tamanhos
raquete_largura = 10
raquete_altura = 100
bola_tamanho = 20

# Menu de dificuldade
def exibir_menu():
    while True:
        tela.fill(COR_FUNDO)
        titulo = fonte.render("PONG - Selecione a Dificuldade", True, COR_TEXTO)
        facil = fonte.render("1 - Fácil", True, COR_TEXTO)
        medio = fonte.render("2 - Médio", True, COR_TEXTO)
        dificil = fonte.render("3 - Difícil", True, COR_TEXTO)
        muito_dificil = fonte.render("4 - Muito Difícil", True, COR_TEXTO)
        sair = fonte.render("ESC - Sair", True, COR_TEXTO)

        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 100))
        tela.blit(facil, (largura//2 - facil.get_width()//2, 200))
        tela.blit(medio, (largura//2 - medio.get_width()//2, 250))
        tela.blit(dificil, (largura//2 - dificil.get_width()//2, 300))
        tela.blit(muito_dificil, (largura//2 - muito_dificil.get_width()//2, 350))
        tela.blit(sair, (largura//2 - sair.get_width()//2, 450))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_1:
                    return {'bola': 4, 'ia': 2}
                if evento.key == pygame.K_2:
                    return {'bola': 6, 'ia': 4}
                if evento.key == pygame.K_3:
                    return {'bola': 8, 'ia': 6}
                if evento.key == pygame.K_4:
                    return {'bola': 10, 'ia': 8}

# Loop do jogo
def jogar(config):
    player1_y = altura // 2 - raquete_altura // 2
    player2_y = altura // 2 - raquete_altura // 2
    bola_x = largura // 2 - bola_tamanho // 2
    bola_y = altura // 2 - bola_tamanho // 2
    velocidade_jogador = 7
    bola_vel_x = random.choice([-1, 1]) * config['bola']
    bola_vel_y = random.choice([-1, 1]) * config['bola']
    velocidade_ia = config['ia']
    pontos1 = 0
    pontos2 = 0
    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return  # Volta ao menu

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and player1_y > 0:
            player1_y -= velocidade_jogador
        if teclas[pygame.K_s] and player1_y < altura - raquete_altura:
            player1_y += velocidade_jogador

        # Movimento da IA
        if bola_y < player2_y + raquete_altura // 2 and player2_y > 0:
            player2_y -= velocidade_ia
        if bola_y > player2_y + raquete_altura // 2 and player2_y < altura - raquete_altura:
            player2_y += velocidade_ia

        # Movimento da bola
        bola_x += bola_vel_x
        bola_y += bola_vel_y

        # Colisão borda superior/inferior
        if bola_y <= 0 or bola_y >= altura - bola_tamanho:
            bola_vel_y *= -1

        # Colisão com raquetes
        if bola_x <= 10 + raquete_largura and player1_y < bola_y + bola_tamanho and bola_y < player1_y + raquete_altura:
            bola_vel_x *= -1
        if bola_x + bola_tamanho >= largura - 20 and player2_y < bola_y + bola_tamanho and bola_y < player2_y + raquete_altura:
            bola_vel_x *= -1

        # Pontuação
        if bola_x < 0:
            pontos2 += 1
            bola_x = largura // 2
            bola_y = altura // 2
            bola_vel_x = random.choice([-1, 1]) * config['bola']
            bola_vel_y = random.choice([-1, 1]) * config['bola']
        elif bola_x > largura:
            pontos1 += 1
            bola_x = largura // 2
            bola_y = altura // 2
            bola_vel_x = random.choice([-1, 1]) * config['bola']
            bola_vel_y = random.choice([-1, 1]) * config['bola']

        # Desenhar
        tela.fill(COR_FUNDO)
        pygame.draw.rect(tela, COR_RAQUETE_1, (10, player1_y, raquete_largura, raquete_altura))
        pygame.draw.rect(tela, COR_RAQUETE_2, (largura - 20, player2_y, raquete_largura, raquete_altura))
        pygame.draw.ellipse(tela, COR_BOLA, (bola_x, bola_y, bola_tamanho, bola_tamanho))
        pygame.draw.aaline(tela, COR_LINHA, (largura // 2, 0), (largura // 2, altura))
        placar = fonte.render(f"{pontos1}   {pontos2}", True, COR_TEXTO)
        tela.blit(placar, (largura // 2 - placar.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)

# Loop principal
if __name__ == "__main__":
    while True:
        dificuldade = exibir_menu()
        jogar(dificuldade)
