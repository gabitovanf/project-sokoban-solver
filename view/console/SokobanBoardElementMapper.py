from view.AbstractValueMapper import AbstractValueMapper
from view.AbstractBoardData import AbstractBoardData
from sokoban.board.ISokobanBoard import ISokobanBoard


class SokobanBoardElementMapper(AbstractValueMapper):
    # EMPTY = ' '
    EMPTY = '.'
    WALL = '#'
    BOX = '*'
    GOAL = 'o'
    PLAYER = 'Y'
    PLAYER_ON_GOAL = 'ẙ'
    BOX_ON_GOAL = '¤'

    # Errors:
    PLAYER_ON_BOX = 'X'
    PLAYER_ON_WALL = '¥'

    def __init__(self, board: ISokobanBoard):
        super().__init__()
        self._board = board
    
    def get_view_at_index(self, source: AbstractBoardData, index):
        board = self._board
        player_is_on = 1 if index == source.player_position else 0
        symbols = [SokobanBoardElementMapper.EMPTY, SokobanBoardElementMapper.PLAYER]

        if board._is_box_on_goal(index):
            symbols = [SokobanBoardElementMapper.BOX_ON_GOAL, SokobanBoardElementMapper.BOX_ON_GOAL]
        elif board._is_wall(index):
            symbols = [SokobanBoardElementMapper.WALL, SokobanBoardElementMapper.PLAYER_ON_WALL]
        elif board._is_box(index):
            symbols = [SokobanBoardElementMapper.BOX, SokobanBoardElementMapper.PLAYER_ON_BOX]
        elif board.is_goal(index):
            symbols = [SokobanBoardElementMapper.GOAL, SokobanBoardElementMapper.PLAYER_ON_GOAL]

        # add some space with ' ' 
        return symbols[player_is_on] + ' '
