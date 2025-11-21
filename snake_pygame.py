import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Colors
BLACK = (10, 10, 20)
DARK_BLUE = (15, 33, 62)
BLUE = (15, 52, 96)
CYAN = (126, 246, 213)
LIGHT_BLUE = (122, 162, 255)
RED = (255, 124, 156)
WHITE = (255, 255, 255)
GRAY = (141, 162, 197)
DARK_GRAY = (50, 50, 70)

# Game settings
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 18
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT + 120

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("🐍 Snake Game")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = font_small.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class SnakeGame:
    def __init__(self):
        self.reset()
        self.game_started = False
        self.paused = False
        
        # Buttons
        button_y = WINDOW_HEIGHT - 90
        self.start_button = Button(50, button_y, 150, 50, "START", BLUE, LIGHT_BLUE)
        self.pause_button = Button(220, button_y, 150, 50, "PAUSE", BLUE, LIGHT_BLUE)
        self.reset_button = Button(390, button_y, 150, 50, "RESET", RED, (255, 100, 120))
    
    def reset(self):
        self.snake = [(10, 9), (9, 9), (8, 9)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.place_food()
        self.score = 0
        self.speed = 8
        self.game_over = False
        self.game_started = False
        self.paused = False
    
    def place_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def update(self):
        if not self.game_started or self.paused or self.game_over:
            return
        
        self.direction = self.next_direction
        
        # New head position
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):
            self.game_over = True
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food
        if new_head == self.food:
            self.score += 10
            self.food = self.place_food()
            self.speed = min(self.speed + 0.3, 20)
        else:
            self.snake.pop()
    
    def change_direction(self, new_direction):
        # Prevent 180-degree turn
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def draw(self, surface):
        # Background
        surface.fill(BLACK)
        
        # Draw grid
        grid_surface = pygame.Surface((WINDOW_WIDTH, CELL_SIZE * GRID_HEIGHT))
        grid_surface.fill(DARK_BLUE)
        
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if (x + y) % 2 == 0:
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(grid_surface, BLUE, rect)
        
        surface.blit(grid_surface, (0, 0))
        
        # Draw grid lines
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, CELL_SIZE * GRID_HEIGHT), 1)
        for y in range(0, CELL_SIZE * GRID_HEIGHT, CELL_SIZE):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (WINDOW_WIDTH, y), 1)
        
        # Draw food
        food_rect = pygame.Rect(
            self.food[0] * CELL_SIZE + 3,
            self.food[1] * CELL_SIZE + 3,
            CELL_SIZE - 6,
            CELL_SIZE - 6
        )
        pygame.draw.ellipse(surface, CYAN, food_rect)
        pygame.draw.ellipse(surface, WHITE, food_rect, 2)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            if i == 0:  # Head
                pygame.draw.rect(surface, RED, rect, border_radius=8)
                pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
                
                # Eyes
                eye_size = 5
                if self.direction == (1, 0):  # Right
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 22, y * CELL_SIZE + 10), eye_size)
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 22, y * CELL_SIZE + 20), eye_size)
                elif self.direction == (-1, 0):  # Left
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 8, y * CELL_SIZE + 10), eye_size)
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 8, y * CELL_SIZE + 20), eye_size)
                elif self.direction == (0, -1):  # Up
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 10, y * CELL_SIZE + 8), eye_size)
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 20, y * CELL_SIZE + 8), eye_size)
                else:  # Down
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 10, y * CELL_SIZE + 22), eye_size)
                    pygame.draw.circle(surface, WHITE, (x * CELL_SIZE + 20, y * CELL_SIZE + 22), eye_size)
            else:  # Body
                pygame.draw.rect(surface, LIGHT_BLUE, rect, border_radius=5)
                pygame.draw.rect(surface, CYAN, rect, 2, border_radius=5)
        
        # Draw UI panel
        ui_y = CELL_SIZE * GRID_HEIGHT
        pygame.draw.rect(surface, BLACK, (0, ui_y, WINDOW_WIDTH, 120))
        pygame.draw.line(surface, CYAN, (0, ui_y), (WINDOW_WIDTH, ui_y), 2)
        
        # Score
        score_text = font_medium.render(f"SCORE: {self.score}", True, CYAN)
        surface.blit(score_text, (20, ui_y + 15))
        
        # Status
        if self.game_over:
            status_text = font_medium.render("GAME OVER!", True, RED)
        elif self.paused:
            status_text = font_medium.render("PAUSED", True, GRAY)
        elif self.game_started:
            status_text = font_medium.render("PLAYING", True, CYAN)
        else:
            status_text = font_medium.render("READY", True, GRAY)
        
        status_rect = status_text.get_rect(center=(WINDOW_WIDTH // 2, ui_y + 30))
        surface.blit(status_text, status_rect)
        
        # Buttons
        self.start_button.draw(surface)
        self.pause_button.draw(surface)
        self.reset_button.draw(surface)
        
        # Game over overlay
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, CELL_SIZE * GRID_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            surface.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("GAME OVER!", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, CELL_SIZE * GRID_HEIGHT // 2 - 30))
            surface.blit(game_over_text, game_over_rect)
            
            final_score_text = font_medium.render(f"Final Score: {self.score}", True, CYAN)
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, CELL_SIZE * GRID_HEIGHT // 2 + 20))
            surface.blit(final_score_text, final_score_rect)
            
            restart_text = font_small.render("Click RESET to play again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, CELL_SIZE * GRID_HEIGHT // 2 + 60))
            surface.blit(restart_text, restart_rect)

def main():
    game = SnakeGame()
    running = True
    frame_count = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Button events
            if game.start_button.handle_event(event):
                if not game.game_started and not game.game_over:
                    game.game_started = True
                    game.paused = False
            
            if game.pause_button.handle_event(event):
                if game.game_started and not game.game_over:
                    game.paused = not game.paused
            
            if game.reset_button.handle_event(event):
                game.reset()
            
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.change_direction((0, -1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.change_direction((0, 1))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.change_direction((1, 0))
                elif event.key == pygame.K_SPACE:
                    if game.game_started and not game.game_over:
                        game.paused = not game.paused
                elif event.key == pygame.K_RETURN:
                    if not game.game_started and not game.game_over:
                        game.game_started = True
                elif event.key == pygame.K_r:
                    game.reset()
        
        # Update game
        frame_count += 1
        if frame_count >= 60 / game.speed:
            game.update()
            frame_count = 0
        
        # Draw
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

