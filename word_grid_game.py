import tkinter as tk
import random
import pygame
import os
import math

class WordGridGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Grid Game")
        self.selected_cells = []
        self.score = 0
        self.words1_list = ['boat', 'coat', 'tall', 'ball', 'july', 'crow', 'five', 'gain', 'exit', 'hide', 'rice', 'lace', 'race']

        self.words_list = self.split_words(self.words1_list)
        random.shuffle(self.words_list)
        self.word_grid = self.convert_to_grid(self.words_list)

        self.create_ui()
        self.init_sound()

    def split_words(self, words1_list):
        words_list = []
        for word in words1_list:
            if len(word) % 2 == 0:
                words_list.extend([word[:len(word)//2], word[len(word)//2:]])
        return words_list

    def convert_to_grid(self, words_list):
        grid_size = int(math.sqrt(len(words_list)))
        while grid_size * grid_size < len(words_list):
            grid_size += 1
        extra = grid_size * grid_size - len(words_list)
        words_list.extend([''] * extra)
        return [[words_list[i * grid_size + j] for j in range(grid_size)] for i in range(grid_size)]

    def create_ui(self):
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack()

        tk.Label(self.main_frame, text="Form words by selecting adjacent tiles", font=("Minion Pro", 16, "bold")).grid(row=0, column=0, columnspan=len(self.word_grid[0]), pady=10)

        self.entry_grid = []
        for i, row in enumerate(self.word_grid):
            grid_row = []
            for j, word in enumerate(row):
                entry = tk.Label(self.main_frame, text=word, padx=30, pady=30, relief=tk.RAISED,
                                 font=("Minion Pro", 20), borderwidth=5, bg="Medium Purple", width=6)
                entry.grid(row=i+1, column=j, padx=2, pady=2)
                entry.bind('<Button-1>', lambda event, row=i, col=j: self.on_cell_click(event, row, col))
                grid_row.append(entry)
            self.entry_grid.append(grid_row)

        row_offset = len(self.word_grid) + 1

        self.message_label = tk.Label(self.main_frame, text="", font=("Minion Pro", 14))
        self.message_label.grid(row=row_offset, column=0, columnspan=len(self.word_grid[0]), pady=5)

        self.score_label = tk.Label(self.main_frame, text=f"Score: {self.score}", font=("Minion Pro", 14, "bold"))
        self.score_label.grid(row=row_offset + 1, column=0, columnspan=len(self.word_grid[0]), pady=5)

        # Buttons
        button_row = row_offset + 2
        tk.Button(self.main_frame, text="Check Word", command=self.check_combined_word, font=("Minion Pro", 12),
                  bg="White", borderwidth=4).grid(row=button_row, column=0, columnspan=len(self.word_grid[0]), pady=3)

        tk.Button(self.main_frame, text="Reset", command=self.reset_selection, font=("Minion Pro", 12),
                  bg="White", borderwidth=4).grid(row=button_row + 1, column=0, columnspan=len(self.word_grid[0]), pady=3)

        tk.Button(self.main_frame, text="Toggle Sound", command=self.toggle_sound, font=("Minion Pro", 12),
                  bg="White", borderwidth=4).grid(row=button_row + 2, column=0, columnspan=len(self.word_grid[0]), pady=3)

        tk.Button(self.main_frame, text="Exit", command=self.root.quit, font=("Minion Pro", 12),
                  bg="White", borderwidth=4).grid(row=button_row + 3, column=0, columnspan=len(self.word_grid[0]), pady=3)

    def on_cell_click(self, event, row, col):
        if (row, col) not in self.selected_cells:
            if not self.selected_cells or self.is_adjacent(row, col, self.selected_cells[-1]):
                self.selected_cells.append((row, col))
                self.entry_grid[row][col].config(bg='lightblue')

    def is_adjacent(self, row, col, prev_cell):
        return abs(row - prev_cell[0]) <= 1 and abs(col - prev_cell[1]) <= 1

    def check_combined_word(self):
        if not self.selected_cells:
            self.message_label.config(text="No cells selected!", fg="orange")
            return

        combined_word = ''.join(self.word_grid[row][col] for row, col in self.selected_cells)
        if combined_word in self.words1_list:
            self.message_label.config(text=f"✅ '{combined_word}' is a valid word!", fg="green")
            self.score += 1
        else:
            self.message_label.config(text=f"❌ '{combined_word}' is not a valid word!", fg="red")

        self.score_label.config(text=f"Score: {self.score}")
        self.reset_selection()

    def reset_selection(self):
        for row, col in self.selected_cells:
            self.entry_grid[row][col].config(bg='Medium Purple')
        self.selected_cells = []

    def init_sound(self):
        pygame.init()
        self.sound_enabled = True
        self.sound_path = 'music.mp3'
        if os.path.exists(self.sound_path):
            self.sound = pygame.mixer.Sound(self.sound_path)
            self.sound.play(-1)  # Loop music
        else:
            self.message_label.config(text="⚠️ music.mp3 not found", fg="orange")

    def toggle_sound(self):
        if hasattr(self, 'sound') and self.sound_enabled:
            self.sound.stop()
            self.sound_enabled = False
        elif hasattr(self, 'sound') and not self.sound_enabled:
            self.sound.play(-1)
            self.sound_enabled = True

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGridGame(root)
    root.mainloop()
