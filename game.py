from Enums.move_side_enum import Side
from Enums.game_mode_enum import GameMode
from hexagonal_cell import HexagonalCell
from constants import *
import math
import pygame


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
        self.move_side: Side = Side.BLUE
        self._cells: list[list[HexagonalCell]] = [[None for _ in range(self.size * 2 - 1)] for _ in range(self.size * 2 - 1)] # noqa
        self.__create_hexagons()

    def __create_field(self):
        hexagons = self.__create_hexagons()
        hexagon_index = 0
        cell_indexes = [self.size // 2]
        for row_index in range(self.size):
            cell_in_row = 0
            new_cell_indexes = []
            for cell_index in cell_indexes:
                self._cells[row_index][cell_index] = HexagonalCell(hexagons[hexagon_index])
                hexagon_index += 1
                cell_in_row += 1
                if cell_index + 1 < self.size:
                    new_cell_indexes.append(cell_index + 1)
                if cell_index - 1 >= 0:
                    new_cell_indexes.append(cell_index - 1)
            cell_indexes = new_cell_indexes

    def __create_hexagons(self) -> list[list[tuple[float, float]]]:
        hexagons = []
        vertical_distance = self._hex_size * math.sqrt(3)
        spacing_offset = 0.2
        spacing = self._hex_size * spacing_offset
        max_hexagons_in_middle = self.size
        total_width = (1.5 * self._hex_size + spacing) * (max_hexagons_in_middle - 1) + self._hex_size
        start_x = (self._screen_size - total_width) / 2

        for row in range(2 * self.size - 1):
            hexagons_in_row = max_hexagons_in_middle - abs(self.size - row - 1)
            for col in range(hexagons_in_row):
                offset_x = abs(self.size - row - 1) * (self._hex_size * 0.75 + spacing / 2)
                center_x = start_x + offset_x + col * (1.5 * self._hex_size + spacing) + self._hex_size
                center_y = (row + 1) * (vertical_distance / 2 + spacing * 3) + self._hex_size
                hexagon = self.__create_hexagon(center_x, center_y, self._hex_size)
                hexagons.append(hexagon)
        return hexagons

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
                if cell and cell.is_point_in_hexagon((mouse_x, mouse_y)):
                    # закраска + переход хода
                    pass

    def run(self) -> None:
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    self.__handle_mouse_click(mouse_x, mouse_y)
            pygame.display.flip()
        pygame.quit()
