import tkinter as tk
import random
from tkinter import messagebox

class SnakesAndLadders:
    # --- Game Constants ---
    BOARD_SIZE = 10
    CELL_SIZE = 40
    BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE
    DICE_SIZE = 60  # Size for the visual dice square
    
    # Define the "shortcuts" as (start_square, end_square)
    LADDERS = {
        4: 14, 9: 31, 20: 38, 28: 84, 40: 59,
        51: 67, 63: 81, 71: 91
    }
    SNAKES = {
        99: 54, 95: 75, 92: 73, 87: 24, 64: 60,
        62: 19, 53: 33, 46: 5, 25: 2
    }
    
    PLAYER_COLORS = ["red", "blue"]

    def __init__(self, master):
        self.master = master
        master.title("Tkinter Snakes and Ladders with Visual Dice")
        
        # --- GUI Setup ---
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=20, pady=20)
        
        # 1. Canvas for the board
        self.canvas = tk.Canvas(self.main_frame, width=self.BOARD_PIXEL_SIZE, 
                                height=self.BOARD_PIXEL_SIZE, bg="light gray")
        self.canvas.pack(side=tk.LEFT)
        
        # 2. Controls Panel
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.RIGHT, padx=20)
        
        self.status_label = tk.Label(self.control_frame, text="", 
                                     font=('Arial', 14, 'bold'))
        self.status_label.pack(pady=10)
        
        # NEW: Dice Display Canvas
        self.dice_canvas = tk.Canvas(self.control_frame, width=self.DICE_SIZE, 
                                     height=self.DICE_SIZE, bg="white", highlightthickness=1, highlightbackground="black")
        self.dice_canvas.pack(pady=10)
        
        self.dice_label = tk.Label(self.control_frame, text="Roll: -", font=('Arial', 16))
        self.dice_label.pack(pady=5)
        
        self.roll_button = tk.Button(self.control_frame, text="Roll Dice", command=self.roll_dice, 
                                     font=('Arial', 16), width=15, bg="#2ecc71", fg="white")
        self.roll_button.pack(pady=20)
        
        # NEW: Reset/Play Again Button
        self.reset_button = tk.Button(self.control_frame, text="Play Again", command=self.reset_game, 
                                      font=('Arial', 16), width=15, bg="#f39c12", fg="white", state=tk.DISABLED)
        self.reset_button.pack(pady=10)
        
        # Initialize Game and Board
        self.draw_board()
        self.player_tokens = [
            self.canvas.create_oval(0, 0, 0, 0, fill=self.PLAYER_COLORS[0], outline="black"),
            self.canvas.create_oval(0, 0, 0, 0, fill=self.PLAYER_COLORS[1], outline="black")
        ]
        
        # Set initial game state (positions, turn, etc.)
        self.reset_game_state()

    def draw_dice(self, number):
        """Draws the visual representation of the dice (1-6) on the small canvas."""
        self.dice_canvas.delete("all")
        size = self.DICE_SIZE
        pip_size = size / 10
        center = size / 2
        offset = size / 4
        
        # Define pip positions for all numbers (relative to the center)
        positions = {
            # Corners and Center
            1: [(center, center)],
            2: [(center - offset, center - offset), (center + offset, center + offset)],
            3: [(center - offset, center - offset), (center, center), (center + offset, center + offset)],
            4: [(center - offset, center - offset), (center + offset, center - offset), 
                (center - offset, center + offset), (center + offset, center + offset)],
            5: [(center - offset, center - offset), (center + offset, center - offset), 
                (center - offset, center + offset), (center + offset, center + offset), 
                (center, center)],
            6: [(center - offset, center - offset), (center + offset, center - offset), 
                (center - offset, center), (center + offset, center),
                (center - offset, center + offset), (center + offset, center + offset)],
        }
        
        # Draw pips based on the number
        if number in positions:
            for x, y in positions[number]:
                self.dice_canvas.create_oval(x - pip_size, y - pip_size, 
                                            x + pip_size, y + pip_size, 
                                            fill="black")

    def get_coords(self, square_number):
        """Converts a square number (1-100) to (x, y) pixel coordinates."""
        if square_number < 1 or square_number > 100:
            return -10, -10 # Off-screen
        
        r = (square_number - 1) // self.BOARD_SIZE
        c = (square_number - 1) % self.BOARD_SIZE
        
        # Adjust column for serpentine board pattern (alternating rows)
        if r % 2 == 1: 
            c = self.BOARD_SIZE - 1 - c

        x = (c * self.CELL_SIZE) + (self.CELL_SIZE / 2)
        # Rows are drawn top-down, but the game is played bottom-up (1-100)
        y = (self.BOARD_SIZE - 1 - r) * self.CELL_SIZE + (self.CELL_SIZE / 2)
        
        return x, y

    def draw_board(self):
        """Draws the 10x10 grid, numbers, snakes, and ladders."""
        
        for i in range(1, 101):
            x_center, y_center = self.get_coords(i)
            x0 = x_center - self.CELL_SIZE / 2
            y0 = y_center - self.CELL_SIZE / 2
            
            # Draw the cell rectangle
            color = "white" if (i % 2) == 0 else "light yellow"
            self.canvas.create_rectangle(x0, y0, x0 + self.CELL_SIZE, y0 + self.CELL_SIZE, 
                                         fill=color, outline="gray")
            
            # Draw the square number
            self.canvas.create_text(x0 + 5, y0 + 5, text=str(i), anchor=tk.NW, font=('Arial', 7))

        # Draw Ladders (Green)
        for start, end in self.LADDERS.items():
            start_x, start_y = self.get_coords(start)
            end_x, end_y = self.get_coords(end)
            self.canvas.create_line(start_x, start_y, end_x, end_y, width=3, fill="green", arrow=tk.LAST, capstyle=tk.ROUND)
            
        # Draw Snakes (Brown)
        for start, end in self.SNAKES.items():
            start_x, start_y = self.get_coords(start)
            end_x, end_y = self.get_coords(end)
            self.canvas.create_line(start_x, start_y, end_x, end_y, width=3, fill="brown", arrow=tk.LAST, capstyle=tk.ROUND)

    def update_token_position(self, player_index):
        """Moves the player token on the canvas."""
        pos = self.player_positions[player_index]
        x_center, y_center = self.get_coords(pos)
        
        # Offset the tokens slightly so they don't completely overlap
        offset = -5 if player_index == 0 else 5
        
        token_id = self.player_tokens[player_index]
        
        # Coordinates for the oval (x1, y1, x2, y2)
        x1 = x_center - 10 + offset
        y1 = y_center - 10
        x2 = x_center + 10 + offset
        y2 = y_center + 10
        
        # Use canvas.coords to reposition the existing token
        self.canvas.coords(token_id, x1, y1, x2, y2)

    def check_win(self):
        """Checks if the current player has reached or passed square 100."""
        if self.player_positions[self.current_player] >= 100:
            self.game_over = True
            winner = self.current_player + 1
            self.status_label.config(text=f"Player {winner} Wins!", fg="purple")
            messagebox.showinfo("Game Over", f"Congratulations! Player {winner} wins!")
            self.roll_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL) # Enable reset button on win
            return True
        return False

    def roll_dice(self):
        """Handles the dice roll and player movement."""
        if self.game_over:
            return

        dice_roll = random.randint(1, 6)
        
        # NEW: Draw the dice visual
        self.draw_dice(dice_roll)
        
        player_index = self.current_player
        current_pos = self.player_positions[player_index]
        new_pos = current_pos + dice_roll

        self.dice_label.config(text=f"Roll: {dice_roll}")

        # Rule: Cannot overshoot 100. If new_pos > 100, stay at current_pos.
        if new_pos > 100:
            new_pos = current_pos
        
        self.player_positions[player_index] = new_pos
        self.update_token_position(player_index)
        
        if self.check_win():
            return
            
        # Check for snake or ladder after a slight delay
        self.master.after(500, lambda: self.check_shortcuts(player_index)) 
            
    def check_shortcuts(self, player_index):
        """Applies the snake or ladder move."""
        current_pos = self.player_positions[player_index]
        target = current_pos
        message = ""
        
        # Check Ladders
        if current_pos in self.LADDERS:
            target = self.LADDERS[current_pos]
            message = f"Player {player_index+1} climbed a **ladder** to {target}!"
            
        # Check Snakes
        elif current_pos in self.SNAKES:
            target = self.SNAKES[current_pos]
            message = f"Player {player_index+1} was bitten by a **snake**, sliding down to {target}!"
            
        if target != current_pos:
             self.player_positions[player_index] = target
             messagebox.showinfo("Shortcut Taken", message)
            
        # Update UI again after the shortcut move (even if no shortcut occurred)
        self.update_token_position(player_index)
        
        # Switch turn
        self.switch_turn()

    def switch_turn(self):
        """Switches the current player's turn."""
        self.current_player = 1 - self.current_player # Switches 0 to 1, and 1 to 0
        player_name = self.current_player + 1
        player_color = self.PLAYER_COLORS[self.current_player]
        self.status_label.config(text=f"Player {player_name}'s Turn ({player_color.capitalize()})", 
                                 fg=player_color)

    def reset_game_state(self):
        """Resets the game state variables to start a new game."""
        self.player_positions = [1, 1]
        self.current_player = 0
        self.game_over = False
        
        # Update UI elements
        self.status_label.config(text="Player 1's Turn (Red)", fg=self.PLAYER_COLORS[0])
        self.dice_label.config(text="Roll: -")
        self.roll_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        
        self.draw_dice(1) # Show initial dice face
        
        # Move both tokens back to square 1
        self.update_token_position(0)
        self.update_token_position(1)

    def reset_game(self):
        """Wrapper to call the reset logic."""
        self.reset_game_state()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakesAndLadders(root)
    root.mainloop()