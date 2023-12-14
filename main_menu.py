from tkinter import *
from tkinter.messagebox import showerror
from Enums.game_mode_enum import GameMode
from game import Game


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
        play_with_bot_button = Button(self._window, text='Играть с ботом', font=('Roboto', 14),
                                      width=12, height=2, command=lambda:
                                      self.__start_game(GameMode.BOT, size_var.get()))
        play_with_player_button = Button(self._window, text='Играть вдвоем', font=('Roboto', 14),
                                         width=12, height=2, command=lambda:
                                         self.__start_game(GameMode.PLAYER, size_var.get()))

        main_label.pack(anchor='center', pady=10)
        size_entry.pack(anchor='center', pady=5)
        play_with_bot_button.place(x=50, y=100)
        play_with_player_button.place(x=220, y=100)

    def __start_game(self, game_mode: GameMode, field_size: str) -> None:
        if not field_size.isdigit() or not 3 <= int(field_size) <= 15:
            showerror("Ошибка", "Нужно ввести размер поля в строку ввода (целое число от 3 до 15)")
            return
        self._window.destroy()
        game = Game(game_mode, int(field_size))
        game.run()
