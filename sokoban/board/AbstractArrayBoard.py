from sokoban.board.AbstractBoard import AbstractBoard

class AbstractArrayBoard(AbstractBoard):
    def __init__(self, width: int, height: int, fill_with=0):
        super().__init__(width, height, fill_with)

        size = self._size
        self._elements = [] if size < 1 else list(map(lambda a: fill_with, range(size)))
        self._move_level = 0
        self._move_id = 0
        self._last_move_id = 0
    
    @property
    def elements(self):
        return self._elements
    
    def _copy_state_from_to(self, from_board, to_board):
        to_board.player_position = from_board.player_position
        for (i, elem) in enumerate(from_board._elements):
            to_board._elements[i] = elem
    
    