import pygame
import sys
import random
import math
from enum import Enum

# ============= CORES =============
DARK_BG = (10, 5, 25) 
NEON_PINK = (255, 20, 147) 
NEON_MAGENTA = (255, 0, 255) 
NEON_CYAN = (0, 255, 255) 
DEEP_PURPLE = (75, 0, 130)  
HOT_PINK = (255, 105, 180)  
WHITE = (255, 255, 255)
GREEN_CHECK = (0, 255, 100)
RED_X = (255, 50, 50)
YELLOW_WARN = (255, 255, 0)
BLACK = (0, 0, 0) 

class GameState(Enum):
    MENU = 1
    MODULE_SELECTION = 2
    VERB_TABLE = 3
    QUIZ = 4
    RESULTS = 5
    DETAILED_RESULTS = 6

# ============= BANCO DE DADOS =============
EXERCISES_DATABASE = {
    "verb_to_be": {
        "fill": [
            {"text": "She ___ a teacher.", "answer": "is"},
            {"text": "They ___ students.", "answer": "are"},
            {"text": "I ___ happy.", "answer": "am"},
            {"text": "We ___ friends.", "answer": "are"},
            {"text": "It ___ cold outside.", "answer": "is"},
        ],
        "multiple_choice": [
            {"text": "You ___ my friend.", "answer": "are", "options": ["am", "is", "are"]},
            {"text": "The cat ___ sleeping.", "answer": "is", "options": ["am", "are", "is"]},
            {"text": "Are they ready? Yes, they ___.", "answer": "are", "options": ["is", "am", "are", "be"]},
            {"text": "My father ___ a pilot.", "answer": "is", "options": ["are", "is", "am", "be"]},
            {"text": "___ I correct?", "answer": "Am", "options": ["Is", "Are", "Am", "Be"]},
        ]
    },
    
    "regular_irregular_verbs": {
        "fill": [
            {"text": "She (study) ___ for the test yesterday.", "answer": "studied"},
            {"text": "I (eat) ___ pizza for dinner.", "answer": "ate"},
            {"text": "He (go) ___ to London last year.", "answer": "went"},
            {"text": "The cat (sleep) ___ on the couch.", "answer": "slept"},
            {"text": "I (drive) ___ to the beach this morning.", "answer": "drove"},
        ],
        "multiple_choice": [
            {"text": "She ___ (teach) English in Japan.", "answer": "taught", "options": ["teach", "teached", "taught"]},
            {"text": "We ___ (try) to fix the car all morning.", "answer": "tried", "options": ["tryed", "tried", "tride"]},
            {"text": "I ___ (hear) a strange noise outside.", "answer": "heard", "options": ["heard", "heared", "hear"]},
            {"text": "He ___ (forget) his wallet at home.", "answer": "forgot", "options": ["forgot", "forget", "forgotted"]},
            {"text": "The company ___ (close) last month.", "answer": "closed", "options": ["closed", "closen", "close"]},
        ]
    },
}

# ============= TABELA DE VERBOS =============
VERB_TABLE = """
TABELA DE VERBOS - Principais Irregulares
Infinitivo     Past Simple    Past Participle
─────────────────────────────────────────────
be             was/were       been
go             went           gone
do             did            done
make           made           made
come           came           come
take           took           taken
see            saw            seen
know           knew           known
think          thought        thought
find           found          found
give           gave           given
tell           told           told
work           worked         worked
call           called         called
try            tried          tried
ask            asked          asked
need           needed         needed
feel           felt           felt
become         became         become
leave          left           left
put            put            put
mean           meant          meant
keep           kept           kept
let            let            let
begin          began          begun
seem           seemed         seemed
help           helped         helped
show           showed         shown
hear           heard          heard
write          wrote          written
read           read           read
allow          allowed        allowed
drink          drank          drunk
bring          brought        brought
eat            ate            eaten
fall           fell           fallen
cut            cut            cut
run            ran            run
speak          spoke          spoken
forget         forgot         forgotten
grow           grew           grown
sell           sold           sold
pay            paid           paid
meet           met            met
include        included       included
continue       continued      continued
set            set            set
learn          learned/learnt learned/learnt
change         changed        changed
lead           led            led
understand     understood     understood
watch          watched        watched
follow         followed        followed
"""

# ============= FUNÇÕES DE DESENHO =============

def draw_cyberpunk_grid(screen, width, height, color, spacing=60, alpha=30):
    
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.set_alpha(alpha)
    for y in range(0, height + spacing, spacing):
        pygame.draw.line(s, color, (0, y), (width, y), 1)
    for x in range(0, width + spacing, spacing):
        pygame.draw.line(s, color, (x, 0), (x, height), 1)
    screen.blit(s, (0, 0))

def draw_neon_glow_text(screen, font, text, x, y, color):
    
    shadow_offset = 2
    shadow_color = tuple(max(0, c - 50) for c in color) 
    shadow_text = font.render(text, True, shadow_color)
    screen.blit(shadow_text, shadow_text.get_rect(center=(x + shadow_offset, y + shadow_offset)))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, text_surface.get_rect(center=(x, y)))

def draw_neon_rect(screen, color, rect, border_width=2):
    
    pygame.draw.rect(screen, color, rect, border_width, border_radius=8)

def draw_cyberpunk_button(screen, rect, text, font, color, text_color, hover=False, feedback_color=None):
    
    button_color = feedback_color if feedback_color else color
    
    
    if hover or feedback_color:
        highlight_color = tuple(min(255, c + 30) for c in button_color)
        pygame.draw.rect(screen, highlight_color, rect.inflate(2, 2), border_radius=10)

    pygame.draw.rect(screen, DARK_BG, rect, border_radius=8)
    draw_neon_rect(screen, button_color, rect, border_width=2)

    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, text_surface.get_rect(center=rect.center))

def draw_scanlines(screen, width, height):
    """Scanlines muito sutis."""
    s = pygame.Surface((width, height), pygame.SRCALPHA) 
    s.set_alpha(15) 
    for y in range(0, height, 4): 
        pygame.draw.line(s, BLACK, (0, y), (width, y), 1)
    screen.blit(s, (0, 0))

class CyberpunkButton:
    def __init__(self, x, y, width, height, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover = False

    def draw(self, screen, font, feedback_color=None):
        draw_cyberpunk_button(screen, self.rect, self.text,
                              font, self.color, self.text_color, self.hover, feedback_color)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

# ============= JOGO PRINCIPAL =============

class LINGGOGame:
    width = 1200
    height = 800
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("LINGGO Cyberpunk Essencial")

        self.font_title = pygame.font.Font(None, 100) 
        self.font_large = pygame.font.Font(None, 50)  
        self.font_normal = pygame.font.Font(None, 36) 
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18) 
        
        self.scroll_y = 0 
        self.max_scroll_y = 0 
        self.answer_submitted_frame = -1
        self.answer_delay_frames = 30     
        self.last_setup_question_index = -1 
        
        try:
            self.logo = pygame.image.load("linggo_logo.png").convert_alpha()
            # CORREÇÃO DO LOGO: Redimensionar mantendo a proporção
            logo_width = 800
            logo_height = int(self.logo.get_height() * (logo_width / self.logo.get_width()))
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        except pygame.error:
            self.logo = None
        
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        
        self.current_module = None
        self.exercises = []
        self.user_answers = []
        self.score = 0
        self.input_text = ""
        self.selected_option = None
        self.module_buttons = []
        self.option_buttons = []
        
        self.frame_count = 0
        
       
        self.back_button_quiz = CyberpunkButton(30, 700, 200, 60, "ABORT MISSION", NEON_CYAN) 
        self.view_details_button = CyberpunkButton(850, 650, 300, 80, "VIEW REPORT", NEON_MAGENTA) 
        self.back_to_summary_button = CyberpunkButton(50, 50, 250, 60, "SUMMARY", NEON_PINK)
        
       
        self.rain_drops = []
        for _ in range(50): 
            self.rain_drops.append(self._create_drop())

    def _create_drop(self):
        return {
            'x': random.randint(0, self.width), 'y': random.randint(-500, 0),
            'speed': random.uniform(3, 8), 
            'length': random.randint(5, 20), 
            'color': random.choice([NEON_CYAN, DEEP_PURPLE, HOT_PINK]) 
        }

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == GameState.QUIZ: self.back_button_quiz.check_hover(mouse_pos)
        
        if self.answer_submitted_frame == -1:
            for btn in self.module_buttons: btn.check_hover(mouse_pos)
            for btn in self.option_buttons: btn.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if self.state == GameState.DETAILED_RESULTS and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: self.scroll_y = min(self.scroll_y + 20, 0)
                elif event.button == 5: self.scroll_y = max(self.scroll_y - 20, self.max_scroll_y)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.MENU: self.handle_menu_click(mouse_pos)
                elif self.state == GameState.MODULE_SELECTION: self.handle_module_selection_click(mouse_pos)
                elif self.state == GameState.QUIZ:
                    if self.back_button_quiz.is_clicked(mouse_pos): self.state = GameState.MENU; self.reset_game_state()
                    elif self.answer_submitted_frame == -1: self.handle_quiz_click(mouse_pos)
                elif self.state == GameState.VERB_TABLE: self.handle_verb_table_click(mouse_pos)
                elif self.state == GameState.RESULTS:
                    if self.view_details_button.is_clicked(mouse_pos):
                        self.max_scroll_y = min(0, -(len(self.user_answers) * 120 + 50))
                        self.state = GameState.DETAILED_RESULTS
                    else: self.handle_results_click(mouse_pos)
                elif self.state == GameState.DETAILED_RESULTS:
                    if self.back_to_summary_button.is_clicked(mouse_pos): self.state = GameState.RESULTS
            
            if event.type == pygame.KEYDOWN and self.state == GameState.QUIZ and self.is_fill_exercise():
                if event.key == pygame.K_BACKSPACE: self.input_text = self.input_text[:-1]
                elif event.key == pygame.K_RETURN: self.submit_fill_answer()
                elif event.unicode.isalnum() or event.unicode in (' ', "'", "-"): self.input_text += event.unicode

        return True

    def reset_game_state(self):
        self.current_module = None; self.exercises = []; self.user_answers = []; self.score = 0
        self.input_text = ""; self.selected_option = None; self.answer_submitted_frame = -1
        self.scroll_y = 0; self.max_scroll_y = 0; self.last_setup_question_index = -1

    def handle_menu_click(self, pos):
        if pygame.Rect(self.width // 2 - 200, 500, 400, 100).collidepoint(pos):
            self.setup_module_buttons()
            self.state = GameState.MODULE_SELECTION

    def handle_module_selection_click(self, pos):
        for i, btn in enumerate(self.module_buttons):
            if btn.is_clicked(pos):
                if i == 0: self.load_exercises("verb_to_be")
                elif i == 1: self.load_exercises("regular_irregular_verbs")
                elif i == 2: self.state = GameState.VERB_TABLE; return
                
                self.state = GameState.QUIZ; return

    def handle_verb_table_click(self, pos):
        if pygame.Rect(50, 700, 200, 60).collidepoint(pos): self.state = GameState.MODULE_SELECTION

    def handle_quiz_click(self, pos):
        if self.answer_submitted_frame != -1: return
        for btn in self.option_buttons:
            if btn.is_clicked(pos):
                self.selected_option = btn.text
                self.submit_multiple_choice_answer()
                return

    def handle_results_click(self, pos):
        if pygame.Rect(400, 650, 400, 80).collidepoint(pos):
            self.state = GameState.MODULE_SELECTION
            self.reset_game_state()

    def setup_module_buttons(self):
        self.module_buttons = [
            CyberpunkButton(100, 150, 1000, 80, "PROTOCOL 1: VERB TO BE (10 QS)", NEON_CYAN), 
            CyberpunkButton(100, 280, 1000, 80, "PROTOCOL 2: IRREGULAR VERBS (10 QS)", NEON_PINK),
            CyberpunkButton(100, 410, 1000, 80, "DATABASE: VERB TABLE", NEON_MAGENTA),
        ]

    def load_exercises(self, module):
        self.current_module = module
        exercises = EXERCISES_DATABASE[module]
        fill_exercises = exercises.get("fill", [])[:5]
        multiple_choice = exercises.get("multiple_choice", [])[:5]
        self.exercises = fill_exercises + multiple_choice
        random.shuffle(self.exercises)
        
        self.current_exercise_index = 0; self.user_answers = []; self.score = 0
        self.input_text = ""; self.selected_option = None; self.answer_submitted_frame = -1
        self.last_setup_question_index = -1

    def is_fill_exercise(self):
        if self.current_exercise_index >= len(self.exercises): return False
        return "options" not in self.exercises[self.current_exercise_index]

    def submit_fill_answer(self):
        exercise = self.exercises[self.current_exercise_index]
        is_correct = self.input_text.lower().strip() == exercise["answer"].lower()
        if is_correct: self.score += 1
        self.user_answers.append({"question": exercise["text"], "user_answer": self.input_text, "correct_answer": exercise["answer"], "is_correct": is_correct})
        self.input_text = ""
        self.answer_submitted_frame = self.frame_count
        self.answer_delay_frames = 15 
        
    def submit_multiple_choice_answer(self):
        exercise = self.exercises[self.current_exercise_index]
        is_correct = self.selected_option == exercise["answer"]
        if is_correct: self.score += 1
        self.user_answers.append({"question": exercise["text"], "user_answer": self.selected_option, "correct_answer": exercise["answer"], "is_correct": is_correct})
        self.answer_submitted_frame = self.frame_count 
        self.answer_delay_frames = 30 

    def setup_option_buttons(self):
        exercise = self.exercises[self.current_exercise_index]
        options = exercise["options"].copy()
        random.shuffle(options)
        self.option_buttons = []
        colors = [NEON_PINK, NEON_MAGENTA, NEON_CYAN, HOT_PINK, (0, 191, 255)]
        
        for i, option in enumerate(options):
            y = 350 + i * 90
            self.option_buttons.append(CyberpunkButton(250, y, 700, 70, option, colors[i % len(colors)]))

    def update_effects(self):
        self.frame_count += 1
        
        if self.answer_submitted_frame != -1:
            if self.frame_count - self.answer_submitted_frame >= self.answer_delay_frames:
                self.current_exercise_index += 1
                self.selected_option = None 
                self.answer_submitted_frame = -1 
                self.last_setup_question_index = -1
                if self.current_exercise_index >= len(self.exercises):
                    self.state = GameState.RESULTS 

    
        for drop in self.rain_drops:
            drop['y'] += drop['speed']
            if drop['y'] > self.height:
                drop['y'] = -drop['length']
                drop['x'] = random.randint(0, self.width)

    def draw_effects(self):
        
        for drop in self.rain_drops:
            pygame.draw.line(self.screen, drop['color'], (int(drop['x']), int(drop['y'])), (int(drop['x']), int(drop['y'] - drop['length'])), 1)


    def render_menu(self):
        self.screen.fill(DARK_BG)
        draw_cyberpunk_grid(self.screen, self.width, self.height, DEEP_PURPLE)
        self.draw_effects()
        
        if self.logo:
            self.screen.blit(self.logo, self.logo.get_rect(center=(self.width // 2, 250)))
        else:
            draw_neon_glow_text(self.screen, self.font_title, "LINGGO!", self.width // 2, 250, NEON_PINK)
        
        start_rect = pygame.Rect(self.width // 2 - 200, 500, 400, 100)
        draw_cyberpunk_button(self.screen, start_rect, "START", self.font_large, NEON_PINK, WHITE, False)
        
        if self.frame_count % 30 < 20:
            press_text = self.font_small.render("PRESS START TO ENTER", True, HOT_PINK)
            self.screen.blit(press_text, press_text.get_rect(center=(self.width // 2, 650)))

    def render_module_selection(self):
        self.screen.fill(DARK_BG)
        draw_cyberpunk_grid(self.screen, self.width, self.height, NEON_PINK)
        self.draw_effects()
        draw_neon_glow_text(self.screen, self.font_large, "SELECT PROTOCOL", self.width // 2, 100, NEON_PINK)
        for btn in self.module_buttons: btn.draw(self.screen, self.font_normal)

    def render_verb_table(self):
        self.screen.fill(DARK_BG)
        draw_cyberpunk_grid(self.screen, self.width, self.height, NEON_MAGENTA)
        self.draw_effects()
        draw_neon_glow_text(self.screen, self.font_large, "DATALOG: VERB TABLE", self.width // 2, 50, NEON_MAGENTA)
        
        table_rect = pygame.Rect(40, 120, self.width - 80, 550)
        pygame.draw.rect(self.screen, DARK_BG, table_rect, border_radius=10)
        draw_neon_rect(self.screen, NEON_CYAN, table_rect)
        
        y = 140
        for line in VERB_TABLE.split('\n'):
            line_surface = self.font_tiny.render(line, True, NEON_CYAN); self.screen.blit(line_surface, (60, y)); y += 18
        
        back_btn = CyberpunkButton(50, 700, 200, 60, "BACK", NEON_PINK); back_btn.draw(self.screen, self.font_small)

    def render_quiz(self):
        self.screen.fill(DARK_BG)
        draw_cyberpunk_grid(self.screen, self.width, self.height, DEEP_PURPLE)
        self.draw_effects()
        
        total_qs = len(self.exercises)
        progress_text = self.font_small.render(f"LEVEL {self.current_exercise_index + 1}/{total_qs}", True, NEON_MAGENTA)
        self.screen.blit(progress_text, (30, 30))
        score_text = self.font_small.render(f"SCORE: {self.score}", True, NEON_CYAN)
        self.screen.blit(score_text, (self.width - 200, 30))
        self.back_button_quiz.draw(self.screen, self.font_small)

        if self.current_exercise_index < total_qs:
            exercise = self.exercises[self.current_exercise_index]
            is_fill = self.is_fill_exercise()

            if is_fill:
                container_rect = pygame.Rect(150, 150, 900, 450); pygame.draw.rect(self.screen, BLACK, container_rect, border_radius=15)
                draw_neon_rect(self.screen, NEON_PINK, container_rect)
                draw_neon_glow_text(self.screen, self.font_normal, exercise["text"], self.width // 2, 250, NEON_CYAN)
                
                input_rect = pygame.Rect(300, 350, 600, 70); pygame.draw.rect(self.screen, BLACK, input_rect, border_radius=10)
                draw_neon_rect(self.screen, NEON_MAGENTA, input_rect)
                
                cursor = "|" if self.frame_count % 15 < 10 else " "
                input_surface = self.font_normal.render(self.input_text + cursor, True, HOT_PINK)
                self.screen.blit(input_surface, (320, 365))
                instruction = self.font_small.render("TYPE ANSWER AND PRESS ENTER", True, NEON_CYAN)
                self.screen.blit(instruction, instruction.get_rect(center=(self.width // 2, 480)))
            else:
                if self.last_setup_question_index != self.current_exercise_index: self.setup_option_buttons(); self.last_setup_question_index = self.current_exercise_index
                
                words = exercise["text"].split(); lines = []; current_line = ""
                for word in words:
                    if len(current_line + word) > 50 and current_line: lines.append(current_line); current_line = word + " "
                    else: current_line += word + " "
                lines.append(current_line)
                y_offset = 150
                for line in lines:
                    question_text = self.font_normal.render(line.strip(), True, NEON_PINK)
                    self.screen.blit(question_text, question_text.get_rect(center=(self.width // 2, y_offset))); y_offset += 50
                
                show_feedback = self.selected_option is not None; correct_answer = exercise["answer"]
                
                for btn in self.option_buttons:
                    feedback_color = None
                    if show_feedback:
                        is_correct = btn.text == correct_answer; is_selected = btn.text == self.selected_option
                        if is_correct: feedback_color = GREEN_CHECK
                        elif is_selected: feedback_color = RED_X
                        btn.draw(self.screen, self.font_small, feedback_color)
                    else:
                        btn.draw(self.screen, self.font_small)

    def render_results(self):
        self.screen.fill(DARK_BG)
        draw_cyberpunk_grid(self.screen, self.width, self.height, NEON_PINK)
        self.draw_effects()
        
        results_rect = pygame.Rect(200, 150, 800, 450); pygame.draw.rect(self.screen, BLACK, results_rect, border_radius=20)
        draw_neon_rect(self.screen, NEON_MAGENTA, results_rect, border_width=5)
        
        draw_neon_glow_text(self.screen, self.font_title, "TRANSMISSION COMPLETE", self.width // 2, 220, NEON_PINK)
        
        percentage = (self.score / len(self.exercises)) * 100 if len(self.exercises) > 0 else 0
        score_color = GREEN_CHECK if percentage >= 70 else NEON_MAGENTA
        draw_neon_glow_text(self.screen, self.font_large, f"SCORE: {self.score}/{len(self.exercises)}", self.width // 2, 350, score_color)
        
        message = "PERFECT RUN! YOUR DATA IS CLEAN." if percentage >= 80 else ("GREAT WORK! MINOR ERRORS DETECTED." if percentage >= 60 else "TRY AGAIN! OPTIMIZATION REQUIRED.")
        message_text = self.font_small.render(message, True, NEON_CYAN)
        self.screen.blit(message_text, message_text.get_rect(center=(self.width // 2, 500)))
        
        back_btn = CyberpunkButton(400, 650, 400, 80, "CONTINUE", NEON_PINK); back_btn.draw(self.screen, self.font_normal)
        self.view_details_button.draw(self.screen, self.font_normal)

    def render_detailed_results(self):
        self.screen.fill(DARK_BG)
        draw_cyberpunk_grid(self.screen, self.width, self.height, DEEP_PURPLE)
        self.draw_effects()
        draw_neon_glow_text(self.screen, self.font_large, "DETAILED REPORT", self.width // 2, 50, NEON_CYAN)
        self.back_to_summary_button.draw(self.screen, self.font_small)

        display_rect = pygame.Rect(50, 120, self.width - 100, self.height - 180); pygame.draw.rect(self.screen, DARK_BG, display_rect, border_radius=10)
        draw_neon_rect(self.screen, HOT_PINK, display_rect, border_width=2)
        
        total_content_height = 50 
        for answer in self.user_answers: total_content_height += 80 + (30 if not answer["is_correct"] else 0)

        self.max_scroll_y = min(0, display_rect.height - total_content_height)
        content_surface = pygame.Surface((display_rect.width, max(display_rect.height, total_content_height)), pygame.SRCALPHA); content_surface.fill(BLACK) # Usando BLACK como fundo do scroll
        y_content = 20 + self.scroll_y

        for i, answer_data in enumerate(self.user_answers):
            current_line_height = 80 + (30 if not answer_data["is_correct"] else 0)
            if i % 2 == 0: pygame.draw.rect(content_surface, (15, 5, 45, 100), (0, y_content - self.scroll_y, display_rect.width, current_line_height))

            status_symbol = "✓" if answer_data["is_correct"] else "X"; status_color = GREEN_CHECK if answer_data["is_correct"] else RED_X
            status_surface = self.font_small.render(f"Q{i+1} ({status_symbol})", True, status_color); content_surface.blit(status_surface, (20, y_content))
            
            question_text = answer_data["question"].replace("___", "______"); question_surface = self.font_small.render(question_text, True, WHITE)
            content_surface.blit(question_surface, (100, y_content)); y_pos = y_content + 30
            
            user_ans_text = f"Input: {str(answer_data['user_answer'])}"; user_answer_surface = self.font_small.render(user_ans_text, True, status_color)
            content_surface.blit(user_answer_surface, (100, y_pos)); y_pos += 30
            
            if not answer_data["is_correct"]:
                correct_surface = self.font_small.render(f"Correct: {str(answer_data['correct_answer'])}", True, YELLOW_WARN)
                content_surface.blit(correct_surface, (100, y_pos)); y_pos += 30
            
            y_content = y_content - self.scroll_y + current_line_height; y_content += self.scroll_y 

        self.screen.blit(content_surface, display_rect.topleft, (0, -self.scroll_y, display_rect.width, display_rect.height))


    def render(self):
        if self.state == GameState.MENU: self.render_menu()
        elif self.state == GameState.MODULE_SELECTION: self.render_module_selection()
        elif self.state == GameState.VERB_TABLE: self.render_verb_table()
        elif self.state == GameState.QUIZ: self.render_quiz()
        elif self.state == GameState.RESULTS: self.render_results()
        elif self.state == GameState.DETAILED_RESULTS: self.render_detailed_results()
        
        
        draw_scanlines(self.screen, self.width, self.height)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update_effects()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = LINGGOGame()
    game.run()