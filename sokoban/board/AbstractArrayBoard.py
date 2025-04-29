import json
from sokoban.utils.UrlStringEncoder import UrlStringEncoder
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
    
    def get_state_stamp(self):
        return self._elements.copy(), self._player_position, self._move_id, self._move_level
    
    def restore_state_from_stamp(self, state_tuple):
        elements, player_postion, move_id, move_level = state_tuple

        if self._move_id == move_id:
            # print('DO NOT CHANGE BOARD. MOVE ID:', move_id)
            return

        self._player_position = player_postion
        for (index, item) in enumerate(elements):
            self._elements[index] = item

        # Helper
        self._move_id = move_id
        # Statistics
        self._move_level = move_level

    def _get_next_move_id(self):
        self._last_move_id += 1

        return self._last_move_id
    