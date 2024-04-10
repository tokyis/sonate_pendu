import random
import string

import customtkinter as tk

import server
from server import GameState
from PIL import Image, ImageTk


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.dictionary = server.build_dictionary(server.DICTIONARY_PATH)
        self.game_state: GameState = None
        # self.name_field: tk.CTkEntry = None
        self.player_name_sv = tk.StringVar()
        self.player_lives_text: tk.CTkLabel = None
        self.content_frame: tk.CTkFrame = None
        self.game_image: tk.CTkLabel = None

        # self.geometry("800x800")
        # self.minsize(800, 800)
        self.resizable(False, False)
        self.title("Sonate - Pendu")
        self.pack_propagate(True)

        self.show_start_dialog()

    def show_start_dialog(self):
        frame = tk.CTkFrame(self)
        self.content_frame = frame
        frame.pack(expand=True, padx=10, pady=10)
        frame.grid_anchor("center")

        title_label = tk.CTkLabel(frame, text="Sonate\nPendu", font=tk.CTkFont(size=30, weight="bold"))
        title_label.grid(column=0, row=0, padx=10, pady=10)

        name_field = tk.CTkEntry(master=frame, width=300, placeholder_text="Nom du joueur",
                                 textvariable=self.player_name_sv)
        name_field.bind("<Return>", lambda event: self.on_start_button())
        name_field.grid(column=0, row=1, padx=40, pady=10)
        self.after(500, lambda: name_field.focus_set())

        button = tk.CTkButton(master=frame, text="Démarrer", command=self.on_start_button())
        button.grid(column=0, row=2, padx=20, pady=20)

    def on_start_button(self):
        if self.player_name_sv is None:
            return
        player_name = self.player_name_sv.get().strip()
        if player_name == "":
            return
        self.content_frame.destroy()
        self.init_game_state(player_name)
        self.show_game_screen()

    def init_game_state(self, player_name):
        self.game_state = GameState(player_name, server.MAX_LIVES, random.choice(self.dictionary), "'")

    def on_close(self):
        app.destroy()
        app.quit()

    def show_game_screen(self):
        frame = tk.CTkFrame(self)
        self.content_frame = frame
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title_label = tk.CTkLabel(frame, text="Sonate Pendu", font=tk.CTkFont(size=30, weight="bold"))
        title_label.pack(padx=10, pady=10)

        header_frame = tk.CTkFrame(frame)
        header_frame.pack(fill=tk.BOTH, expand=True)
        player_name_text = tk.CTkLabel(header_frame, text=f'Player : {self.game_state.player_name}',
                                       font=tk.CTkFont(size=14, weight="bold"))
        player_name_text.pack(padx=10, pady=10, side=tk.LEFT, anchor="nw")

        self.player_lives_text = tk.CTkLabel(header_frame, text=f'{self.game_state.player_lives} lives left',
                                             font=tk.CTkFont(size=14, weight="bold"))
        self.player_lives_text.pack(padx=10, pady=10, side=tk.RIGHT, anchor="ne")

        img = Image.open("./static/p5.png")
        ctkimg = tk.CTkImage(light_image=img, size=(512, 512))

        self.game_image = tk.CTkLabel(frame, text="", image=ctkimg)
        self.game_image.pack(padx=10, pady=10)
        self.game_image.pack_propagate(False)

        masked_word = server.get_masked_word(self.game_state.secret_word, self.game_state.player_guesses)
        masked_word_label = tk.CTkLabel(frame, text=masked_word, font=tk.CTkFont(size=24, weight="bold"))
        masked_word_label.pack(padx=10, pady=10, side=tk.TOP, after=self.game_image)

        keyboard = tk.CTkFrame(self)
        keyboard.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        keyboard.anchor("center")

        offset_row = 5
        buttons_per_line = 9
        i = 0
        for letter in string.ascii_lowercase:
            button = tk.CTkButton(master=keyboard, width=50, text=letter,
                                  command=lambda l=letter, m=masked_word_label: self.on_letter_button(l, m))
            button.grid(column=i % buttons_per_line, row=offset_row + i // buttons_per_line, padx=3, pady=3)
            i += 1
            if i % buttons_per_line == 0:
                offset_row += 1

    def on_letter_button(self, letter, masked_word_label):
        if letter in self.game_state.player_guesses:
            return
        self.game_state.player_guesses += letter
        if letter not in self.game_state.secret_word:
            self.game_state.player_lives -= 1
            self.player_lives_text.configure(text=f'{self.game_state.player_lives} lives left')

        if server.is_word_found(self.game_state.player_guesses, self.game_state.secret_word):
            self.game_image.configure(
                image=tk.CTkImage(light_image=Image.open(f"./static/pw.png"), size=(512, 512)))
        else:
            self.game_image.configure(
                image=tk.CTkImage(light_image=Image.open(f"./static/p{self.game_state.player_lives}.png"), size=(512, 512)))

        masked_word_label.configure(
            text=server.get_masked_word(self.game_state.secret_word, self.game_state.player_guesses))

        if self.game_state.player_lives == 0:
            print("gameover")


if __name__ == "__main__":
    tk.set_appearance_mode("system")
    tk.set_default_color_theme("theme/white.json")
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
