import random
import tkinter as tk

try:
    import winsound
except ImportError:
    winsound = None


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Snake")
        self.root.resizable(False, False)

        # Game settings
        self.cell_size = 25
        self.grid_width = 20
        self.grid_height = 20
        self.difficulties = {
            "Chill": {"speed": 190, "increment": 8, "color": "#7dd56f"},
            "Classic": {"speed": 140, "increment": 10, "color": "#00ff88"},
            "Rage": {"speed": 95, "increment": 12, "color": "#ff6b6b"},
        }
        self.difficulty = "Classic"
        self.speed = self.difficulties[self.difficulty]["speed"]

        # Colors
        self.bg_color = "#1a1a2e"
        self.grid_color_dark = "#0f1a2e"
        self.grid_color = "#16213e"
        self.snake_color = "#0f3460"
        self.snake_head_color = "#e94560"
        self.food_color = self.difficulties[self.difficulty]["color"]
        self.text_color = "#ffffff"

        # Game state
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.food = None
        self.score = 0
        self.game_running = False
        self.game_over = False

        # Create UI
        self.create_widgets()
        self.place_food()
        self.draw_game()

        # Bind keys
        self.root.bind("<KeyPress>", self.on_key_press)

    def create_widgets(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=10)

        # Title
        title_label = tk.Label(
            header_frame,
            text="NEON SNAKE",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
        )
        title_label.pack()

        # Score frame
        score_frame = tk.Frame(self.root, bg=self.bg_color)
        score_frame.pack(pady=5)

        self.score_label = tk.Label(
            score_frame,
            text=f"Score: {self.score}",
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.food_color,
        )
        self.score_label.pack()

        # Difficulty selector
        difficulty_frame = tk.Frame(self.root, bg=self.bg_color)
        difficulty_frame.pack(pady=(0, 8))
        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg="#99aacc",
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulty_menu = tk.OptionMenu(
            difficulty_frame,
            self.difficulty_var,
            *self.difficulties.keys(),
            command=self.set_difficulty,
        )
        difficulty_menu.config(
            font=("Arial", 11, "bold"),
            bg="#0f3460",
            fg="white",
            activebackground="#1f4d80",
            bd=0,
            highlightthickness=0,
        )
        difficulty_menu["menu"].config(
            bg="#0f3460", fg="white", activebackground="#1f4d80"
        )
        difficulty_menu.pack(side=tk.LEFT)

        # Canvas
        canvas_frame = tk.Frame(self.root, bg=self.bg_color)
        canvas_frame.pack(padx=20, pady=10)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.cell_size * self.grid_width,
            height=self.cell_size * self.grid_height,
            bg=self.grid_color,
            highlightthickness=2,
            highlightbackground=self.snake_head_color,
        )
        self.canvas.pack()

        # Control buttons frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="START",
            font=("Arial", 12, "bold"),
            bg=self.food_color,
            fg=self.bg_color,
            activebackground="#00cc66",
            command=self.start_game,
            width=10,
            relief=tk.RAISED,
            bd=3,
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="PAUSE",
            font=("Arial", 12, "bold"),
            bg="#ffaa00",
            fg=self.bg_color,
            activebackground="#ff8800",
            command=self.toggle_pause,
            width=10,
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(
            button_frame,
            text="RESET",
            font=("Arial", 12, "bold"),
            bg=self.snake_head_color,
            fg=self.text_color,
            activebackground="#cc3850",
            command=self.reset_game,
            width=10,
            relief=tk.RAISED,
            bd=3,
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Instructions
        instructions_frame = tk.Frame(self.root, bg=self.bg_color)
        instructions_frame.pack(pady=10)

        instructions = tk.Label(
            instructions_frame,
            text="Arrow Keys / WASD to move • SPACE pause • R reset",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg="#aaaaaa",
        )
        instructions.pack()

        self.root.configure(bg=self.bg_color)

    def draw_game(self):
        self.canvas.delete("all")

        # Draw grid
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                x1 = i * self.cell_size
                y1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = self.grid_color_dark if (i + j) % 2 == 0 else self.grid_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Draw food
        if self.food:
            x, y = self.food
            x1 = x * self.cell_size + 2
            y1 = y * self.cell_size + 2
            x2 = x1 + self.cell_size - 4
            y2 = y1 + self.cell_size - 4
            self.canvas.create_oval(
                x1,
                y1,
                x2,
                y2,
                fill=self.food_color,
                outline="#00dd77",
                width=2,
            )

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            x1 = x * self.cell_size + 2
            y1 = y * self.cell_size + 2
            x2 = x1 + self.cell_size - 4
            y2 = y1 + self.cell_size - 4

            if i == 0:  # Head
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self.snake_head_color,
                    outline="#ff6677",
                    width=2,
                )
                # Eyes
                if self.direction == "Right":
                    self.canvas.create_oval(x2 - 10, y1 + 5, x2 - 6, y1 + 9, fill="white")
                    self.canvas.create_oval(x2 - 10, y2 - 9, x2 - 6, y2 - 5, fill="white")
                elif self.direction == "Left":
                    self.canvas.create_oval(x1 + 6, y1 + 5, x1 + 10, y1 + 9, fill="white")
                    self.canvas.create_oval(x1 + 6, y2 - 9, x1 + 10, y2 - 5, fill="white")
                elif self.direction == "Up":
                    self.canvas.create_oval(x1 + 5, y1 + 6, x1 + 9, y1 + 10, fill="white")
                    self.canvas.create_oval(x2 - 9, y1 + 6, x2 - 5, y1 + 10, fill="white")
                else:  # Down
                    self.canvas.create_oval(x1 + 5, y2 - 10, x1 + 9, y2 - 6, fill="white")
                    self.canvas.create_oval(x2 - 9, y2 - 10, x2 - 5, y2 - 6, fill="white")
            else:  # Body
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self.snake_color,
                    outline="#1a4d7a",
                    width=1,
                )

    def place_food(self):
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in self.snake
        ]
        if free_cells:
            self.food = random.choice(free_cells)

    def start_game(self):
        if not self.game_running and not self.game_over:
            self.game_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.play_start_sound()
            self.game_loop()

    def toggle_pause(self):
        if self.game_over:
            return
        self.game_running = not self.game_running
        if self.game_running:
            self.pause_button.config(text="PAUSE")
            self.game_loop()
        else:
            self.pause_button.config(text="RESUME")

    def reset_game(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.game_running = False
        self.game_over = False
        self.speed = self.difficulties[self.difficulty]["speed"]

        self.score_label.config(text=f"Score: {self.score}", fg=self.food_color)
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="PAUSE")

        self.place_food()
        self.draw_game()

    def on_key_press(self, event):
        key = event.keysym

        if key == "space":
            self.toggle_pause()
            return
        if key in ("r", "R"):
            self.reset_game()
            return

        if not self.game_running:
            return

        # Update direction
        if key in ("Up", "w", "W") and self.direction != "Down":
            self.next_direction = "Up"
        elif key in ("Down", "s", "S") and self.direction != "Up":
            self.next_direction = "Down"
        elif key in ("Left", "a", "A") and self.direction != "Right":
            self.next_direction = "Left"
        elif key in ("Right", "d", "D") and self.direction != "Left":
            self.next_direction = "Right"

    def game_loop(self):
        if not self.game_running:
            return

        self.direction = self.next_direction

        # Get new head position
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        new_head = (head_x, head_y)

        # Check collisions
        if (
            head_x < 0
            or head_x >= self.grid_width
            or head_y < 0
            or head_y >= self.grid_height
            or new_head in self.snake
        ):
            self.end_game()
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += self.difficulties[self.difficulty]["increment"]
            self.score_label.config(text=f"Score: {self.score}")
            self.place_food()
            self.play_food_sound()
            # Increase speed slightly
            self.speed = max(60, self.speed - 3)
        else:
            self.snake.pop()

        self.draw_game()
        self.root.after(self.speed, self.game_loop)

    def end_game(self):
        self.game_running = False
        self.game_over = True
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED)

        # Draw game over overlay
        x1 = self.cell_size * self.grid_width // 4
        y1 = self.cell_size * self.grid_height // 3
        x2 = x1 + self.cell_size * self.grid_width // 2
        y2 = y1 + 100

        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill="#1a1a2e", outline=self.snake_head_color, width=3
        )
        self.canvas.create_text(
            self.cell_size * self.grid_width // 2,
            self.cell_size * self.grid_height // 3 + 30,
            text="GAME OVER!",
            font=("Arial", 24, "bold"),
            fill=self.snake_head_color,
        )
        self.canvas.create_text(
            self.cell_size * self.grid_width // 2,
            self.cell_size * self.grid_height // 3 + 65,
            text=f"Final Score: {self.score}",
            font=("Arial", 16),
            fill=self.food_color,
        )
        self.play_game_over_sound()

    def set_difficulty(self, value):
        if self.game_running:
            return
        self.difficulty = value
        self.food_color = self.difficulties[self.difficulty]["color"]
        self.speed = self.difficulties[self.difficulty]["speed"]
        self.score_label.config(fg=self.food_color)
        self.draw_game()

    def play_start_sound(self):
        if winsound:
            winsound.Beep(600, 80)
            winsound.Beep(750, 80)

    def play_food_sound(self):
        if winsound:
            winsound.Beep(900, 80)

    def play_game_over_sound(self):
        if winsound:
            winsound.Beep(400, 120)
            winsound.Beep(300, 120)
            winsound.Beep(200, 160)


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
