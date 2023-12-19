from tkinter import *
from tkinter.messagebox import showerror
from Enums.game_mode_enum import GameMode
from game import Game


class MainMenu:
    def __init__(self) -> None:
        self._window = Tk()
        self._window.resizable(False, False)
        self._window.grab_set()
        self._window.geometry("400x280")
        self.__draw_menu()
        self._window.mainloop()

    def __draw_menu(self) -> None:
        main_label = Label(self._window, text="Гекс", font=('Roboto', 20, 'bold'))
        size_var = StringVar(self._window, value='Введите размер поля (от 3 до 15)')
        size_entry = Entry(self._window, textvariable=size_var, width=40)
        timer_var = StringVar(self._window, value='Введите ограничение времени на ход (по умолчанию 15)')
        timer_entry = Entry(self._window, textvariable=timer_var, width=40)
        play_with_bot_button = Button(self._window, text='Играть с ботом', font=('Roboto', 14),
                                      width=12, height=2, command=lambda:
                                      self.__start_game(GameMode.EASY_BOT, size_var.get(), timer_var.get()))
        play_with_player_button = Button(self._window, text='Играть вдвоем', font=('Roboto', 14),
                                         width=12, height=2, command=lambda:
                                         self.__start_game(GameMode.PLAYER, size_var.get(), timer_var.get()))
        record_table_button = Button(self._window, text='Таблица побед', font=("Roboto", 14),
                                     command=lambda: self.__show_record_table())

        main_label.pack(anchor='center', pady=10)
        size_entry.pack(anchor='center', pady=5)
        timer_entry.pack(anchor='center', pady=5)
        play_with_bot_button.place(x=50, y=130)
        play_with_player_button.place(x=220, y=130)
        record_table_button.pack(side=BOTTOM, pady=20)

    def __start_game(self, game_mode: GameMode, field_size: str, timer: str) -> None:
        if not field_size.isdigit() or not 3 <= int(field_size) <= 15:
            showerror("Ошибка", "Нужно ввести размер поля в строку ввода (целое число от 3 до 15)")
            return
        if not timer.isdigit():
            timer = '15'
        self._window.destroy()
        game = Game(game_mode, int(field_size), int(timer))
        game.run()
        self.__init__()

    def __show_record_table(self) -> None:
        with open("records.txt") as f:
            records = f.readlines()
        window = Toplevel(self._window)
        window.resizable(False, False)
        window.grab_set()
        window.geometry("380x210")

        blue_label = Label(window, text="Синий", font=('Roboto', 16), pady=10, padx=10)
        red_label = Label(window, text='Красный', font=('Roboto', 16), pady=10, padx=10)
        player_label = Label(window, text="Против игрока", font=('Roboto', 16), padx=10, pady=10)
        bot_label = Label(window, text="Против бота", font=('Roboto', 16), padx=10, pady=10)
        reset_button = Button(window, text='Сбросить', font=("Roboto", 14), command=lambda: self.__clear_records(window))
        blue_label.grid(row=0, column=1)
        red_label.grid(row=0, column=2)
        player_label.grid(row=1, column=0)
        bot_label.grid(row=2, column=0)
        reset_button.grid(row=3, column=2, padx=10, pady=10)

        row, column = 1, 1
        for record in records:
            record_label = Label(window, text=record[:-1], font=('Roboto', 16))
            record_label.grid(row=row, column=column)
            if column == 1:
                column += 1
                continue
            row += 1
            column = 1

    def __clear_records(self, window: Toplevel) -> None:
        with open("records.txt", 'w') as f:
            f.flush()
            f.write('0\n' * 4)
        window.destroy()
        self.__show_record_table()
