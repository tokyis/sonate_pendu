import customtkinter as tk


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.show_start_dialog()

    def show_start_dialog(self):
        self.geometry("400x240")
        self.minsize(400, 240)
        # self.resizable(False, False)
        self.title("Sonate - Pendu")
        frame = tk.CTkFrame(self)
        frame.pack(expand=True, padx=10, pady=10)
        # frame.grid()
        frame.grid_anchor("center")
        title_label = (tk.CTkLabel(frame, text="Sonate\nPendu", font=tk.CTkFont(size=30, weight="bold")).
                       grid(column=0, row=0, padx=10, pady=10))
        name_field = (tk.CTkEntry(master=frame, width=300, placeholder_text="Nom du joueur").
                      grid(column=0, row=1, padx=40, pady=10))
        button = (tk.CTkButton(master=frame, text="Démarrer", command=self.on_start_button).
                  grid(column=0, row=2, padx=20, pady=20))

    def on_start_button(self):
        pass


def on_close():
    app.destroy()
    app.quit()


if __name__ == "__main__":
    tk.set_appearance_mode("system")
    tk.set_default_color_theme("theme/white.json")
    app = App()
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()
