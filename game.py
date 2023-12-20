import random
from Enums.move_side_enum import Side
from Enums.game_mode_enum import GameMode
from hexagonal_cell import HexagonalCell
from constants import *
import tkinter as tk
import math
import pygame
from queue import Queue
import time
from move import Move
from button import Button


class Game:
    def __init__(self, main_menu, game_mode: GameMode, log_index: int, size: int = 11,
                 move_time: int = 15, current_side: Side = Side.BLUE) -> None:
        pygame.init()
        pygame.font.init()
        self._menu = main_menu
        self.log_index = log_index
        self.size: int = size
        self._move_stack: list[Move] = []
        self._undone_stack: list[Move] = []
        self._move_time = move_time
        self.game_mode: GameMode = game_mode
        self._running: bool = True
        self._current_move_time = time.time()
        self._hex_size: int = 20
        self._screen_size: int = (size * 2 + 1) * self._hex_size + 100
        if self.size > 9:
            self._screen_size += 100
        self._screen = pygame.display.set_mode((self._screen_size, self._screen_size * 1.2))
        pygame.display.set_caption("Гекс")
        self._move_side: Side = current_side
        sides = [Side.RED, Side.BLUE]
        self._bot_side = random.choice(sides)
        sides.remove(self._bot_side)
        self._player_side = sides[0]
        self._is_ended = False
        self._cells: list[list[HexagonalCell]] = [[None for _ in range(self.size * 2 - 1)] for _ in range(self.size * 2 - 1)]  # noqa
        self._undo_button = Button(20, self._screen_size - 20, 80, 30, 'Undo')
        self._redo_button = Button(self._screen_size - 100, self._screen_size - 20, 80, 30, 'Redo')
        self.__create_field()

    def __create_field(self) -> None:
        hexagons = self.__create_hexagons()
        hex_index = 0
        hexagons_in_row = 0
        start_index = (self.size * 2 - 1) // 2 + 1
        for row in range(self.size * 2 - 1):
            hexagons_in_row = hexagons_in_row + 1 if row < self.size else hexagons_in_row - 1
            start_index = start_index - 1 if row < self.size else start_index + 1
            current_index = start_index
            for i in range(hexagons_in_row):
                self._cells[row][current_index] = HexagonalCell(hexagons[hex_index],
                                                                row, current_index,
                                                                i == 0 and row >= self.size - 1,
                                                                i == hexagons_in_row - 1 and row < self.size,
                                                                i == 0 and row < self.size,
                                                                i == hexagons_in_row - 1 and row >= self.size - 1,
                                                                Side.NEUTRAL)
                hex_index += 1
                current_index += 2

    def __create_hexagons(self) -> list[list[tuple[float, float]]]:
        hexagons = []
        vertical_distance = self._hex_size * math.sqrt(3)
        spacing = self._hex_size * 0.2
        total_width = (1.5 * self._hex_size + spacing) * (self.size - 1) + self._hex_size
        total_height = (vertical_distance / 2 + spacing / 2) * (2 * self.size - 1) + self._hex_size
        start_x = (self._screen_size - total_width) / 2
        start_y = (self._screen_size - total_height) / 2
        hex_index = 0
        for row in range(2 * self.size - 1):
            hexagons_in_row = self.size - abs(self.size - row - 1)
            start_index = (self.size - hexagons_in_row) / 2
            for col in range(hexagons_in_row):
                center_x = start_x + (start_index + col) * (1.5 * self._hex_size + spacing)
                center_y = start_y + row * (vertical_distance / 2 + spacing * 3) + self._hex_size
                hexagon = self.__create_hexagon(center_x, center_y, self._hex_size)
                hexagons.append(hexagon)
                hex_index += 1
        return hexagons

    def __draw_field(self) -> None:
        for row in self._cells:
            for cell in row:
                if cell:
                    pygame.draw.polygon(self._screen, cell.color, cell.hexagon)
                    pygame.draw.polygon(self._screen, BLACK, cell.hexagon, 1)

    def __create_hexagon(self, center_x: float, center_y: float, size: int) -> list[tuple[float, float]]:
        angles = [30 + 60 * i for i in range(6)]
        hexagon_points = [
            (center_x + size * math.cos(math.radians(angle)),
             center_y + size * math.sin(math.radians(angle)))
            for angle in angles
        ]
        return hexagon_points

    def __handle_mouse_click(self, mouse_x: float, mouse_y: float) -> None:
        for row in self._cells:
            for cell in row:
                if cell and cell.is_point_in_hexagon((mouse_x, mouse_y)) and cell.try_change_color(self._move_side):
                    if self.__check_win():
                        self._running = False
                        self._is_ended = True
                    else:
                        self._move_stack.append(Move(self._move_side, cell))
                        self.__update_move()
                    self._undone_stack.clear()
                    return

    def __make_bot_move(self) -> None:
        if self.game_mode == GameMode.EASY_BOT:
            self.__make_easy_bot_move()
        else:
            self.__make_hard_bot_move()

        if self.__check_win():
            self._running = False
            self._is_ended = True
        else:
            self.__update_move()

    def __make_easy_bot_move(self) -> None:
        neutral_cells = []
        for row in self._cells:
            for cell in row:
                if cell and cell.side == Side.NEUTRAL:
                    neutral_cells.append(cell)
        picked_cell: HexagonalCell = random.choice(neutral_cells)
        picked_cell.try_change_color(self._move_side)
        self._move_stack.append(Move(self._move_side, picked_cell))

    def __make_hard_bot_move(self):
        pass

    def __update_move(self):
        self._move_side = Side.BLUE if self._move_side == Side.RED else Side.RED
        self._current_move_time = time.time()

    def __undo_move(self):
        if len(self._move_stack) == 0:
            return
        last_move = self._move_stack.pop()
        last_move.undo()
        self._undone_stack.append(last_move)
        self.__update_move()

    def __redo_move(self):
        if len(self._undone_stack) == 0:
            return
        last_undone_move = self._undone_stack.pop()
        last_undone_move.redo()
        self._move_stack.append(last_undone_move)
        self.__update_move()

    def __check_win(self) -> bool:
        start_cells = set()
        queue = Queue()
        for row in self._cells:
            for cell in row:
                if cell and cell.is_start(self._move_side) and cell.side == self._move_side:
                    start_cells.add(cell)
                    queue.put(cell)
        return self.__hexagon_bfs(start_cells, queue)

    def __hexagon_bfs(self, visited: set[HexagonalCell], queue: Queue[HexagonalCell]) -> bool:
        while queue.qsize() > 0:
            cell = queue.get()
            visited.add(cell)
            if cell.is_final(self._move_side):
                return True
            for neighbor_cell in self.__get_neighbors(cell):
                if neighbor_cell.side == self._move_side and neighbor_cell not in visited:
                    queue.put(neighbor_cell)

    def __get_neighbors(self, cell: HexagonalCell) -> list[HexagonalCell]:
        possible_neighbors_cords = [
            (cell.x - 1, cell.y - 1), (cell.x + 1, cell.y + 1),
            (cell.x - 1, cell.y + 1), (cell.x + 1, cell.y - 1),
            (cell.x, cell.y - 2), (cell.x, cell.y + 2)
        ]
        result = []
        for cord in possible_neighbors_cords:
            x, y = cord[0], cord[1]
            if self.__is_point_inside_field(x, y) and self._cells[x][y]:
                result.append(self._cells[x][y])
        return result

    def __is_point_inside_field(self, x, y) -> bool:
        return 0 <= x < self.size * 2 - 1 and 0 <= y < self.size * 2 - 1

    def __create_winner_window(self) -> None:
        window = tk.Tk()
        window.resizable(False, False)
        window.geometry("400x200")
        # window.grab_set()
        winner_label = tk.Label(window, text=f"Победил {self._move_side.value} игрок!", font=('Roboto', 20))
        winner_label.place(x=50, y=80)

    def __update_records(self) -> None:
        with open("records.txt") as f:
            old_records = [int(a[:-1]) for a in f.readlines()]
            f.flush()
        new_record_index = 0
        if self.game_mode == GameMode.EASY_BOT or self.game_mode == GameMode.HARD_BOT:
            new_record_index += 2
        if self._move_side == Side.RED:
            new_record_index += 1
        old_records[new_record_index] += 1
        with open("records.txt", "w") as f:
            f.write('\n'.join([str(r) for r in old_records]) + '\n')

    def __draw_timer(self, pos=(60, 50)) -> None:
        color = (0, 0, 255) if self._move_side == Side.BLUE else (255, 0, 0)
        timer_font = pygame.font.Font(None, 36)
        remaining = self._current_move_time + self._move_time - time.time()
        if remaining <= 0:
            self._running = False
            self._move_side = Side.BLUE if self._move_side == Side.RED else Side.RED
            return
        else:
            timer_text = f"{remaining}"[:4]
        text_surface = timer_font.render(timer_text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self._screen.fill(BLACK, text_rect)
        self._screen.blit(text_surface, text_rect.topleft)

    def __check_button_press(self, pos, button) -> bool:
        return button.is_over(pos)

    def __draw_buttons(self) -> None:
        self._undo_button.draw(self._screen)
        self._redo_button.draw(self._screen)

    def continue_game(self) -> None:
        pygame.init()
        pygame.font.init()
        self._screen = pygame.display.set_mode((self._screen_size, self._screen_size * 1.2))
        pygame.display.set_caption("Гекс")
        self._running = True
        self.run()

    def __save_game(self):
        self._menu.save_game(self)

    def run(self) -> None:
        while self._running:
            self.__draw_field()
            self.__draw_timer()
            self.__draw_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif (self.game_mode == GameMode.EASY_BOT or self.game_mode == GameMode.HARD_BOT) and \
                        self._move_side == self._bot_side:
                    self.__make_bot_move()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    self.__handle_mouse_click(mouse_x, mouse_y)
                    if self.__check_button_press((mouse_x, mouse_y), self._redo_button):
                        self.__redo_move()
                    elif self.__check_button_press((mouse_x, mouse_y), self._undo_button):
                        self.__undo_move()
            pygame.display.flip()
        pygame.quit()

        if self._is_ended:
            self._menu.end_game(self)
            self.__update_records()
            self.__create_winner_window()
        else:
            self.__save_game()
