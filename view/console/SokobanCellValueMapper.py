from view.AbstractValueMapper import AbstractValueMapper
from view.AbstractBoardData import AbstractBoardData


class SokobanCellValueMapper(AbstractValueMapper):
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

    def __init__(self):
        super().__init__()

    def value_to_view(self, cell_value_tuple):
        value, player_is_on = cell_value_tuple
        symbols = [SokobanCellValueMapper.EMPTY, SokobanCellValueMapper.PLAYER]

        if value & 5 == 5:
            symbols = [SokobanCellValueMapper.BOX_ON_GOAL, SokobanCellValueMapper.BOX_ON_GOAL]
        elif value & 2 != 0:
            symbols = [SokobanCellValueMapper.WALL, SokobanCellValueMapper.PLAYER_ON_WALL]
        elif value & 1 != 0:
            symbols = [SokobanCellValueMapper.BOX, SokobanCellValueMapper.PLAYER_ON_BOX]
        elif value & 4 != 0:
            symbols = [SokobanCellValueMapper.GOAL, SokobanCellValueMapper.PLAYER_ON_GOAL]

        # add some space with ' ' 
        return symbols[player_is_on] + ' '
    
    def get_view_at_index(self, source: AbstractBoardData, index):
        return self.value_to_view((
            source.elements[index], 
            1 if index == source.player_position else 0
        ))
