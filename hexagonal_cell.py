from typing import Any
from Enums.move_side_enum import Side
from constants import *


class HexagonalCell:
    def __init__(self, hexagon: list[tuple[float, float]], x: int, y: int,
                 is_red_start: bool, is_red_final: bool,
                 is_blue_start: bool, is_blue_final: bool,
                 side: Side = Side.NEUTRAL) -> None:
        self.hexagon = hexagon
        self.x: int = x
        self.y: int = y
        self.side: Side = side
        self.color = GRAY
        self._is_red_start: bool = is_red_start
        self._is_red_final: bool = is_red_final
        self._is_blue_start: bool = is_blue_start
        self._is_blue_final: bool = is_blue_final

    def is_point_in_hexagon(self, point: tuple[float, float]) -> bool:
        x, y = point
        intersects = 0
        for i in range(len(self.hexagon)):
            x1, y1 = self.hexagon[i]
            x2, y2 = self.hexagon[(i + 1) % len(self.hexagon)]
            if y1 == y2 and y == y1:
                if min(x1, x2) <= x <= max(x1, x2):
                    return True
                else:
                    continue
            if y1 < y2:
                if y < y1 or y > y2:
                    continue
            else:
                if y > y1 or y < y2:
                    continue
            intersect_x = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if intersect_x > x:
                intersects += 1
        return intersects % 2 != 0

    def is_final(self, move_side: Side) -> bool:
        return (move_side == Side.RED and self._is_red_final) or \
            (move_side == Side.BLUE and self._is_blue_final)

    def is_start(self, move_side: Side) -> bool:
        return (move_side == Side.RED and self._is_red_start) or \
            (move_side == Side.BLUE and self._is_blue_start)

    def try_change_color(self, move_side: Side) -> bool:
        if self.color == RED or self.color == BLUE:
            return False
        if move_side == Side.RED:
            self.color = RED
        else:
            self.color = BLUE
        self.side = move_side
        return True

    def make_neutral(self):
        self.color = GRAY
        self.side = Side.NEUTRAL
