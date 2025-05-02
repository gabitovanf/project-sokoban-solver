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

    def is_goal(self, position) -> bool:
        pass

    def is_box_element(self, element) -> bool:
        pass

    def get_state_stamp(self) -> tuple:
        pass

    def restore_state_from_stamp(self, stamp: tuple):
        pass

    @property
    def width(self):
        pass

    @property
    def height(self):
        pass

    @property
    def size(self):
        pass

    def element_x(self, index: int) -> int:
        pass

    def element_y(self, index: int) -> int:
        pass
