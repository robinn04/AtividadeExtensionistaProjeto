def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
import pygame
import sys
import random
import json
import os

# -----------------------------
# CONFIGURAÇÕES GERAIS
# -----------------------------

pygame.init() #pygame
pygame.mixer.init() #sistema de audio

#tamanho da tela e relogio (fps)
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MathRush")
CLOCK = pygame.time.Clock()

#fontes
FONT_BIG = pygame.font.SysFont("Impact", 48)
FONT_MED = pygame.font.SysFont("arial", 32)
FONT_SMALL = pygame.font.SysFont("Arial", 24)

#cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
BLUE = (70, 130, 180)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)

# Música de fundo
pygame.mixer.music.load(resource_path("sons/musica_fundo.mp3")) #musica de fundo
pygame.mixer.music.set_volume(0.3)  # volume
pygame.mixer.music.play(-1)  # -1 = loop infinito

#sons de efeito
SOUND_CLICK = pygame.mixer.Sound(resource_path("sons/click.wav"))
SOUND_CORRECT = pygame.mixer.Sound(resource_path("sons/correto.wav"))
SOUND_WRONG = pygame.mixer.Sound(resource_path("sons/errado.wav"))
SOUND_TIME = pygame.mixer.Sound(resource_path("sons/tempo.wav"))

#controle de audio dos efeito sonoros
SOUND_CLICK.set_volume(0.1)
SOUND_CORRECT.set_volume(0.7)
SOUND_WRONG.set_volume(0.3)
SOUND_TIME.set_volume(0.3)

# -----------------------------
# ESTADOS DO JOGO
# -----------------------------

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_TRANSITION = "transition"
STATE_LEVEL_UP = "level_up"
STATE_GAME_OVER = "game_over"
STATE_SCORE = "score"

# -----------------------------
# PONTUAÇÃO POR NUMERAÇÃO
# -----------------------------

OP_POINTS = {
    1: 1,  # Adição
    2: 2,  # Subtração
    3: 3,  # Multiplicação
    4: 4   # Divisão
}

OP_NAMES = {
    1: "Adição",
    2: "Subtração",
    3: "Multiplicação",
    4: "Divisão"
}

# -----------------------------
# SITEMA DE RANKINGS
# -----------------------------
SCORES_FILE = resource_path("scores.json")

#carregar scores/ranking
def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

#salvar scores/ranking
def save_score(name, score, correct):
    scores = load_scores()
    scores.append({"nome": name, "pontuacao": score, "acertos": correct})
    # ira ordena por pontuação decrescente, depois acertos decrescentes
    scores.sort(key=lambda s: (s["pontuacao"], s["acertos"]), reverse=True)
    # Mantém top 10 jogadores que foram melhores
    scores = scores[:10]
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

# -----------------------------
# FUNÇÕES PARA A INTERFACE
# -----------------------------

#desenha o texto na tela (centralizado)
def draw_text_center(text, font, color, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    SCREEN.blit(surf, rect)

#detecta o mouse em cima do texto para o evento de clique (mudar a cor do hover)
def button(rect, text, font, bg, fg, hover_bg=None):
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    r = pygame.Rect(rect)
    is_hover = r.collidepoint(mouse)
    color = hover_bg if (hover_bg and is_hover) else bg
    pygame.draw.rect(SCREEN, color, r, border_radius=8)
    label = font.render(text, True, fg)
    SCREEN.blit(label, label.get_rect(center=r.center))
    return is_hover and clicked

#caixa de texto - texto digitado
def input_box(rect, text, font, active):
    r = pygame.Rect(rect)
    pygame.draw.rect(SCREEN, WHITE if active else GRAY, r, border_radius=8)
    label = font.render(text, True, BLACK)
    SCREEN.blit(label, (r.x + 10, r.y + (r.height - label.get_height()) // 2))
    return r

# -----------------------------
# GERAÇÃO DE QUESTÕES
# -----------------------------
def gerar_questao(operacao, nivel):
    # Operandos de 1 dígito (1 a 9) aleatorio
    a = random.randint(1, 9)
    b = random.randint(1, 9)

# Adição
    if operacao == 1:
        expr = f"{a} + {b}"
        ans = a + b
# Subtração
    elif operacao == 2:
        # Garantir que o resultado não seja negativo
        if a < b:
            a, b = b, a
        expr = f"{a} - {b}"
        ans = a - b
# Multiplicação
    elif operacao == 3:
        expr = f"{a} × {b}"
        ans = a * b
# Divisão inteira
    elif operacao == 4:
        # Garantir divisão exata: (ans = a), (b = divisor), (a*b = dividendo)
        ans = random.randint(1, 9)
        b = random.randint(1, 9)
        expr = f"{ans * b} ÷ {b}"
        ans = ans
    else:
        expr, ans = "0 + 0", 0

    return expr, ans

# -----------------------------
# JOGO MATEMATICO
# -----------------------------
class MathGame:
#começa com o menu
    def __init__(self):
        self.state = STATE_MENU
        self.reset_game()

        #reseta quando chega no final da jogada, perguntas nivel, pontuação, timer, nome do jogador etc
    def reset_game(self):
        self.current_op = 1
        self.current_level = 1
        self.total_levels = 20
        self.level_count = 0     # contador global de níveis
        self.score = 0
        self.correct = 0
        self.question = ""
        self.answer = None
        self.user_input = ""
        self.timer_ms = 10000
        self.start_time = 0
        self.transition_msg = ""
        self.transition_color = WHITE
        self.transition_until = 0
        self.player_name = ""
        self.name_active = False
        self.score_saved = False

        #gera a pergunta, zera o input e inicia o timer
    def start_level(self):
        self.question, self.answer = gerar_questao(self.current_op, self.current_level)
        self.user_input = ""
        self.start_time = pygame.time.get_ticks()

        #avança de nivel, trocando a operação a cada 5 niveis/ finaliza no nivel 20
    def next_level(self):
        self.level_count += 1
        if self.level_count >= self.total_levels:
            self.state = STATE_GAME_OVER
            return
        # Avança nível dentro da operação
        self.current_level += 1
        if self.current_level > 5:
            self.current_level = 1
            self.current_op += 1
        # Transição de nível
        self.state = STATE_LEVEL_UP
        self.transition_msg = f"Avançando para {OP_NAMES[self.current_op]} - Nível {self.current_level}"
        self.transition_color = YELLOW
        self.transition_until = pygame.time.get_ticks() + 1200

    def handle_answer(self):
        # Verifica tempo
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed > self.timer_ms:
# Tempo esgotado
            SOUND_TIME.play()
            self.transition_msg = "Tempo esgotado! +0 pontos"
            self.transition_color = RED
            self.state = STATE_TRANSITION
            self.transition_until = pygame.time.get_ticks() + 1200
            return
        # Verifica resposta
        try:
            val = int(self.user_input)
        except:
            val = None
        if val is not None and val == self.answer:
            SOUND_CORRECT.play()
            pts = OP_POINTS[self.current_op]
            self.score += pts
            self.correct += 1
            self.transition_msg = f"Correto! +{pts} pontos"
            self.transition_color = GREEN
        else:
            SOUND_WRONG.play()
            self.transition_msg = f"Errado! Resposta: {self.answer} | +0 pontos"
            self.transition_color = RED
        self.state = STATE_TRANSITION
        self.transition_until = pygame.time.get_ticks() + 1200

#transições
    def update_transition(self):
        if pygame.time.get_ticks() >= self.transition_until:
        # Após transição, avança para próximo nível
            self.next_level()
            if self.state == STATE_LEVEL_UP:
        # Após mostrar level up, inicia pergunta
                self.start_level()
                self.state = STATE_GAME

#telas principal
    def draw_menu(self):
        SCREEN.fill(GRAY)
        draw_text_center("MATH RUSH", FONT_BIG, YELLOW, 140)
        draw_text_center("OPERAÇÕES: adição, subtração, multiplicação e divisão", FONT_SMALL, WHITE, 260)
        draw_text_center("5 NÍVEIS POR OPERAÇÃO — TOTAL 20 NÍVEIS", FONT_SMALL, WHITE, 200)
        draw_text_center("TEMPO: 10 segundos por pergunta", FONT_SMALL, WHITE, 230)
        draw_text_center("PONTUAÇÃO: +1 (adição) +2 (subtração) +3 (multiplicação) +4 (divisão)", FONT_SMALL, WHITE, 290)

        # Botão iniciar
        if button((WIDTH//2 - 120, 360, 240, 60), "Iniciar", FONT_MED, BLUE, BLACK, hover_bg=(90, 150, 210)):
            SOUND_CLICK.play()
            self.reset_game()
            self.start_level()
            self.state = STATE_GAME

        # Botão ranking
        if button((WIDTH // 2 - 120, 440, 240, 60), "Ranking", FONT_MED, YELLOW, BLACK, hover_bg=(255, 220, 120)):
            SOUND_CLICK.play()
            self.state = STATE_SCORE

        # Botão sair
        if button((WIDTH // 2 - 120, 520, 240, 60),
                  "Sair", FONT_MED, RED, BLACK, hover_bg=(200, 60, 60)):
            SOUND_CLICK.play()
            pygame.quit()
            sys.exit()

# tela do score/pontução
    def draw_score(self):
        SCREEN.fill(BLACK)
        draw_text_center("Ranking", FONT_BIG, YELLOW, 80)

        scores = load_scores()

        if not scores:
            draw_text_center("Nenhum score salvo ainda.", FONT_MED, WHITE, HEIGHT // 2)
        else:
            y = 160
            for i, s in enumerate(scores, start=1):
                text = f"{i}. {s['nome']} — {s['pontuacao']} pts | {s['acertos']} acertos"
                draw_text_center(text, FONT_SMALL, WHITE, y)
                y += 30

        # Botão voltar ao menu
        if button((WIDTH // 1 - 300, HEIGHT - 80, 240, 60),
                  "Voltar", FONT_MED, BLUE, BLACK, hover_bg=(90, 150, 210)):
            SOUND_CLICK.play()
            self.state = STATE_MENU

#tela do game em si
    def draw_game(self):
        SCREEN.fill(GRAY)
        # Cabeçalho
        draw_text_center(f"Operação: {OP_NAMES[self.current_op]} | Nível {self.current_level}/5 | ({self.level_count+1}/20)", FONT_SMALL, WHITE, 40)
        draw_text_center(f"Pontuação: {self.score} | Acertos: {self.correct}", FONT_SMALL, WHITE, 70)

        # Pergunta
        draw_text_center("Resolva:", FONT_MED, WHITE, 160)
        draw_text_center(self.question, FONT_BIG, YELLOW, 220)

        # Timer
        elapsed = pygame.time.get_ticks() - self.start_time
        remaining = max(0, (self.timer_ms - elapsed) // 1000)
        draw_text_center(f"Tempo: {remaining}s", FONT_MED, WHITE, 280)

        # Input
        box = input_box((WIDTH//2 - 150, 340, 300, 60), self.user_input, FONT_MED, True)
        draw_text_center("Digite sua resposta e pressione Enter", FONT_SMALL, WHITE, 420)

        # Dica de pontuação por operação
        draw_text_center(f"Esta operação vale +{OP_POINTS[self.current_op]} ponto(s)", FONT_SMALL, WHITE, 460)

# tela das transições acerto/erro
    def draw_transition(self):
        SCREEN.fill(BLACK)
        draw_text_center(self.transition_msg, FONT_MED, self.transition_color, HEIGHT//2)

# tela da mudança de nivel
    def draw_level_up(self):
        SCREEN.fill(BLACK)
        draw_text_center(self.transition_msg, FONT_MED, YELLOW, HEIGHT//2)

# tela do fim de jogo
    def draw_game_over(self):
        SCREEN.fill(BLACK)
        draw_text_center("Fim do jogo!", FONT_BIG, YELLOW, 140)
        draw_text_center(f"Pontuação total: {self.score}", FONT_MED, WHITE, 200)
        draw_text_center(f"Acertos: {self.correct} de 20", FONT_MED, WHITE, 240)

        # Input nome para salvar score
        draw_text_center("Digite seu nome para salvar no ranking:", FONT_SMALL, WHITE, 300)
        name_rect = input_box((WIDTH//2 - 200, 330, 400, 50), self.player_name, FONT_MED, self.name_active)

        # Botões
        save_clicked = button((WIDTH//2 - 220, 410, 180, 50), "Salvar", FONT_MED, GREEN, BLACK, hover_bg=(60, 220, 140))
        menu_clicked = button((WIDTH//2 + 40, 410, 180, 50), "Menu", FONT_MED, BLUE, BLACK, hover_bg=(90, 150, 210))

        # Eventos de clique no input
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            self.name_active = name_rect.collidepoint(mouse)

        if save_clicked and not self.score_saved:
            name = self.player_name.strip() or "Jogador"
            save_score(name, self.score, self.correct)
            self.score_saved = True
            self.state = STATE_SCORE

        if menu_clicked:
            self.state = STATE_MENU

#eventos de teclado e mouse
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.state == STATE_GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.handle_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        if event.unicode.isdigit() or (event.unicode == '-' and len(self.user_input) == 0):
                            self.user_input += event.unicode
            elif self.state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN and self.name_active:
                    if event.key == pygame.K_RETURN:
                        # Salva e volta ao menu
                        if event.key == pygame.K_RETURN and not self.score_saved:
                            name = self.player_name.strip() or "Jogador"
                            save_score(name, self.score, self.correct)
                            self.score_saved = True
                            self.state = STATE_SCORE
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 20 and (event.unicode.isalnum() or event.unicode in " _-"):
                            self.player_name += event.unicode

#atualiza estados de transição
    def update(self):
        if self.state == STATE_TRANSITION or self.state == STATE_LEVEL_UP:
            self.update_transition()

# dicisao de qual tela desenhar quando o jogo ocorrer - estado atual
    def draw(self):
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_GAME:
            self.draw_game()
        elif self.state == STATE_TRANSITION:
            self.draw_transition()
        elif self.state == STATE_LEVEL_UP:
            self.draw_level_up()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        elif self.state == STATE_SCORE:
            self.draw_score()

# -----------------------------
# LOOP PRINCIPAL
# -----------------------------
def main(): #cria o jogo
    game = MathGame()
    while True: #loop infinito
        CLOCK.tick(60)
        game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()

if __name__ == "__main__": #começar o jogo
    main()
