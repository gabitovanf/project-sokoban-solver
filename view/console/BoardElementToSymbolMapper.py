from view.IValueMapper import IValueMapper
from view.IBoardData import IBoardData
from sokoban.board.ISokobanBoard import ISokobanBoard


class BoardElementToSymbolMapper(IValueMapper):
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
    
    def get_view_at_index(self, source: IBoardData, index):
        board = self._board
        player_is_on = 1 if index == source.player_position else 0
        symbols = [BoardElementToSymbolMapper.EMPTY, BoardElementToSymbolMapper.PLAYER]

        if board._is_box_on_goal(index):
            symbols = [BoardElementToSymbolMapper.BOX_ON_GOAL, BoardElementToSymbolMapper.BOX_ON_GOAL]
        elif board._is_wall(index):
            symbols = [BoardElementToSymbolMapper.WALL, BoardElementToSymbolMapper.PLAYER_ON_WALL]
        elif board._is_box(index):
            symbols = [BoardElementToSymbolMapper.BOX, BoardElementToSymbolMapper.PLAYER_ON_BOX]
        elif board.is_goal(index):
            symbols = [BoardElementToSymbolMapper.GOAL, BoardElementToSymbolMapper.PLAYER_ON_GOAL]

        # add some space with ' ' 
        return symbols[player_is_on] + ' '
