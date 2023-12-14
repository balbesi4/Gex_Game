from Enums.move_side_enum import Side


class HexagonalCell:
    def __init__(self, hexagon: list[tuple[float, float]], is_start: bool,
                 is_final: bool, side: Side = Side.NEUTRAL) -> None:
        self.hexagon = hexagon
        self.side = side
        self.is_start = is_start
        self.is_final = is_final

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
