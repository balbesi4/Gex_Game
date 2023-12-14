from tkinter import *
from Enums.game_mode_enum import GameMode


class MainMenu:
    def __init__(self) -> None:
        self._window = Tk()
        self._window.resizable(False, False)
        self._window.grab_set()
        self._window.geometry("400x200")
        self.__draw_menu()
        self._window.mainloop()

    def __draw_menu(self) -> None:
        main_label = Label(self._window, text="Гекс", font=('Roboto', 20, 'bold'))
        size_var = StringVar(self._window, value='Введите размер поля (от 3 до 15)')
        size_entry = Entry(self._window, textvariable=size_var, width=40)
        play_with_bot_button = Button(self._window, text='Играть с ботом', font=('Roboto', 14), width=12, height=2)
        play_with_player_button = Button(self._window, text='Играть вдвоем', font=('Roboto', 14), width=12, height=2)

        main_label.pack(anchor='center', pady=10)
        size_entry.pack(anchor='center', pady=5)
        play_with_bot_button.place(x=50, y=100)
        play_with_player_button.place(x=220, y=100)

    def __start_game_with_bot(self) -> None:
        self._window.destroy()
        # game.start()

    def __start_game_with_player(self) -> None:
        self._window.destroy()
        # game.start()
