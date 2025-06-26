import pygame
import sys
import random

pygame.init()
pygame.mixer.init()
try:
    pygame.mixer.music.load("sounds/8bitmusic.mp3") 
    pygame.mixer.music.play(-1)  
except pygame.error as e:
    print(f"Erro ao carregar música: {e}")

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong v0.4")

fonte = pygame.font.SysFont("Arial", 36)

COR_FUNDO = (30, 30, 60)
COR_RAQUETE_1 = (255, 100, 100)
COR_RAQUETE_2 = (100, 255, 100)
COR_BOLA = (255, 255, 0)
COR_LINHA = (200, 200, 200)
COR_TEXTO = (255, 255, 255)
COR_PARTICULA = (255, 255, 255)

raquete_largura = 10
raquete_altura = 100
bola_tamanho = 20

class Particula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.raio = random.randint(2, 4)
        self.life = 20

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.raio = max(0, self.raio - 0.1)

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, COR_PARTICULA, (int(self.x), int(self.y)), int(self.raio))

def exibir_menu(titulo, opcoes):
    while True:
        tela.fill(COR_FUNDO)
        texto_titulo = fonte.render(titulo, True, COR_TEXTO)
        tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 100))

        for i, opcao in enumerate(opcoes):
            texto_opcao = fonte.render(f"{i+1} - {opcao[0]}", True, COR_TEXTO)
            tela.blit(texto_opcao, (largura // 2 - texto_opcao.get_width() // 2, 200 + i * 50))

        sair = fonte.render("ESC - Sair", True, COR_TEXTO)
        tela.blit(sair, (largura // 2 - sair.get_width() // 2, 450))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if pygame.K_1 <= evento.key <= pygame.K_9:
                    escolha = evento.key - pygame.K_1
                    if escolha < len(opcoes):
                        return opcoes[escolha][1]

def exibir_vitoria(vencedor):
    class Fogo:
        def __init__(self):
            self.x = random.randint(100, largura - 100)
            self.y = random.randint(100, altura - 200)
            self.particles = []
            self.gerar_particulas()

        def gerar_particulas(self):
            for _ in range(30):
                angulo = random.uniform(0, 2 * math.pi)
                velocidade = random.uniform(1, 5)
                vx = math.cos(angulo) * velocidade
                vy = math.sin(angulo) * velocidade
                cor = random.choice([
                    (255, 100, 100),
                    (100, 255, 100),
                    (100, 100, 255),
                    (255, 255, 100),
                    (255, 100, 255),
                    (100, 255, 255),
                ])
                self.particles.append({
                    'x': self.x,
                    'y': self.y,
                    'vx': vx,
                    'vy': vy,
                    'life': 60,
                    'cor': cor
                })

        def update(self):
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1

        def draw(self, surface):
            for p in self.particles:
                if p['life'] > 0:
                    pygame.draw.circle(surface, p['cor'], (int(p['x']), int(p['y'])), 3)

        def acabou(self):
            return all(p['life'] <= 0 for p in self.particles)

    import math
    fogos = []
    tempo = 0
    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                return

        if tempo % 30 == 0:
            fogos.append(Fogo())

        for f in fogos:
            f.update()

        fogos = [f for f in fogos if not f.acabou()]

        tela.fill(COR_FUNDO)
        texto = fonte.render(f"{vencedor} venceu!", True, COR_TEXTO)
        subtexto = fonte.render("Pressione qualquer tecla para voltar ao menu", True, COR_TEXTO)
        tela.blit(texto, (largura // 2 - texto.get_width() // 2, 220))
        tela.blit(subtexto, (largura // 2 - subtexto.get_width() // 2, 300))

        for f in fogos:
            f.draw(tela)

        pygame.display.flip()
        clock.tick(60)
        tempo += 1

def jogar(config, max_pontos):
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

    particulas = []
    particulas_ponto = []

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and player1_y > 0:
            player1_y -= velocidade_jogador
        if teclas[pygame.K_s] and player1_y < altura - raquete_altura:
            player1_y += velocidade_jogador

        if bola_y < player2_y + raquete_altura // 2 and player2_y > 0:
            player2_y -= velocidade_ia
        if bola_y > player2_y + raquete_altura // 2 and player2_y < altura - raquete_altura:
            player2_y += velocidade_ia

        bola_x += bola_vel_x
        bola_y += bola_vel_y

        if bola_y <= 0 or bola_y >= altura - bola_tamanho:
            bola_vel_y *= -1

        bateu = False
        if bola_x <= 10 + raquete_largura and player1_y < bola_y + bola_tamanho and bola_y < player1_y + raquete_altura:
            bola_vel_x *= -1
            bateu = True
        if bola_x + bola_tamanho >= largura - 20 and player2_y < bola_y + bola_tamanho and bola_y < player2_y + raquete_altura:
            bola_vel_x *= -1
            bateu = True

        if bateu:
            for _ in range(15):
                particulas.append(Particula(bola_x + bola_tamanho // 2, bola_y + bola_tamanho // 2))

        if bola_x < 0:
            pontos2 += 1
            for _ in range(50):
                particulas_ponto.append(Particula(largura // 2, altura // 2))
            bola_x, bola_y = largura // 2, altura // 2
            bola_vel_x = random.choice([-1, 1]) * config['bola']
            bola_vel_y = random.choice([-1, 1]) * config['bola']
        elif bola_x > largura:
            pontos1 += 1
            for _ in range(50):
                particulas_ponto.append(Particula(largura // 2, altura // 2))
            bola_x, bola_y = largura // 2, altura // 2
            bola_vel_x = random.choice([-1, 1]) * config['bola']
            bola_vel_y = random.choice([-1, 1]) * config['bola']

        if (max_pontos and pontos1 >= max_pontos):
            exibir_vitoria("Jogador 1")
            return
        elif (max_pontos and pontos2 >= max_pontos):
            exibir_vitoria("IA")
            return

        for p in particulas[:]:
            p.update()
            if p.life <= 0:
                particulas.remove(p)
        for p in particulas_ponto[:]:
            p.update()
            if p.life <= 0:
                particulas_ponto.remove(p)

        tela.fill(COR_FUNDO)
        pygame.draw.rect(tela, COR_RAQUETE_1, (10, player1_y, raquete_largura, raquete_altura), border_radius=8)
        pygame.draw.rect(tela, COR_RAQUETE_2, (largura - 20, player2_y, raquete_largura, raquete_altura), border_radius=8)
        pygame.draw.ellipse(tela, (180, 180, 0), (bola_x, bola_y, bola_tamanho, bola_tamanho))
        pygame.draw.ellipse(tela, COR_BOLA, (bola_x + 3, bola_y + 3, bola_tamanho - 6, bola_tamanho - 6))

        for y in range(0, altura, 35):
            pygame.draw.rect(tela, COR_LINHA, (largura // 2 - 2, y, 4, 20))

        texto = f"{pontos1}   {pontos2}"
        sombra = fonte.render(texto, True, (50, 50, 50))
        placar = fonte.render(texto, True, COR_TEXTO)
        pos_x = largura // 2 - placar.get_width() // 2
        tela.blit(sombra, (pos_x + 3, 23))
        tela.blit(placar, (pos_x, 20))

        for p in particulas:
            p.draw(tela)
        for p in particulas_ponto:
            p.draw(tela)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    while True:
        dificuldade = exibir_menu("Dificuldade", [("Fácil", {'bola': 4, 'ia': 2}),
                                                  ("Médio", {'bola': 6, 'ia': 4}),
                                                  ("Difícil", {'bola': 8, 'ia': 6}),
                                                  ("Muito Difícil", {'bola': 10, 'ia': 8})])

        max_pontos = exibir_menu("Pontuação Máxima", [("5 pontos", 5),
                                                       ("7 pontos", 7),
                                                       ("10 pontos", 10),
                                                       ("Sem limite", None)])

        jogar(dificuldade, max_pontos)
