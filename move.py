from Enums.move_side_enum import Side
from hexagonal_cell import HexagonalCell


class Move:
    def __init__(self, side: Side, cell: HexagonalCell):
        self.move_side = side
        self.cell: HexagonalCell = cell

    def undo(self):
        self.cell.make_neutral()

    def redo(self):
        self.cell.try_change_color(self.move_side)
