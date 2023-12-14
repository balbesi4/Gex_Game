from Enums.move_side_enum import MoveSide
from hexagonal_cell import HexagonalCell
import math
import pygame


class Field:
    def __init__(self, size: int = 11) -> None:
        self.size: int = size
        self.move_side: MoveSide = MoveSide.BLUE
        self._cells: list[list[HexagonalCell]] = [[None for _ in range(self.size * 2 - 1)] for _ in range(self.size * 2 - 1)] # noqa

    def __create(self) -> None:
        cell_indexes = [len(self._cells) // 2]
        for row_index in range(len(self._cells) // 2 + 1):
            row_1 = self._cells[row_index]
            row_2 = self._cells[self.size - row_index - 1]
            new_cell_indexes = []
            for cell_index in cell_indexes:
                row_1[cell_index] = HexagonalCell(self.__create_hexagon())
                row_2[cell_index] = HexagonalCell(self.__create_hexagon())
                new_cell_indexes.append(cell_index - 1)
                new_cell_indexes.append(cell_index + 1)

    def __create_hexagon(self, center_x: int, center_y: int, size: int) -> list[tuple[float, float]]:
        angles = [30 + 60 * i for i in range(6)]
        hexagon_points = [
            (center_x + size * math.cos(math.radians(angle)),
             center_y + size * math.sin(math.radians(angle)))
            for angle in angles
        ]
        return hexagon_points
