from sokoban.board.AbstractBoard import AbstractBoard

class ISokobanBoard(AbstractBoard):
    def __init__(self, width, height, fill_with=0):
        super().__init__(width, height, fill_with)

    def can_move(self, direction: int) -> bool:
        pass

    def move(self, direction: int):
        pass

    def is_solution(self, stamp: tuple) -> bool:
        pass

