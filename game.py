from Enums.move_side_enum import Side
from Enums.game_mode_enum import GameMode
from hexagonal_cell import HexagonalCell
from constants import *
from tkinter import *
import math
import pygame
from queue import Queue


class Game:
    def __init__(self, game_mode: GameMode, size: int = 11) -> None:
        pygame.init()
        self.size: int = size
        self.game_mode: GameMode = game_mode
        self._running: bool = True
        self._hex_size: int = 20
        self._screen_size: int = (size * 2 + 1) * self._hex_size + 100
        self._screen = pygame.display.set_mode((self._screen_size, self._screen_size * 1.2))
        pygame.display.set_caption("Гекс")
        self._move_side: Side = Side.BLUE
        self._cells: list[list[HexagonalCell]] = [[None for _ in range(self.size * 2 - 1)] for _ in range(self.size * 2 - 1)] # noqa
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
                    else:
                        self._move_side = Side.BLUE if self._move_side == Side.RED else Side.RED

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
            (cell.x, cell.y - 2), (cell.x, cell.y - 2)
        ]
        result = []
        for cord in possible_neighbors_cords:
            x, y = cord[0], cord[1]
            if self.__is_point_inside_field(x, y) and self._cells[x][y]:
                result.append(self._cells[x][y])
        return result

    def __is_point_inside_field(self, x, y):
        return 0 <= x < self.size * 2 - 1 and 0 <= y < self.size * 2 - 1

    def __create_winner_window(self):
        window = Tk()
        window.resizable(False, False)
        window.geometry("400x200")
        window.grab_set()
        winner_label = Label(window, text=f"Победил {self._move_side.value} игрок!", font=('Roboto', 20))
        winner_label.place(x=50, y=80)

    def run(self) -> None:
        while self._running:
            self.__draw_field()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    self.__handle_mouse_click(mouse_x, mouse_y)
            pygame.display.flip()
        pygame.quit()

        self.__create_winner_window()
