import sys
import colorama
from view.AbstractBoardView import AbstractBoardView
from view.AbstractBoardData import AbstractBoardData
from view.AbstractValueMapper import AbstractValueMapper

colorama.init()


class ConsoleBoardView(AbstractBoardView):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    DEFAULT = 9

    REST_COLORS_CMD = '\x1b[0m'

    def __init__(self, source: AbstractBoardData, value_mapper: AbstractValueMapper=None, *args, **kwargs):
        kwargs['value_mapper'] = value_mapper
        super(ConsoleBoardView, self).__init__(source, *args, **kwargs)

        self._value_mapper = value_mapper

    def render(self):
        # The size of the board must not change!

        w = self._source.width
        h = self._source.height
        player_position = self._source.player_position
        output = list(map(lambda elem: self._value_mapper.value_to_view((elem[1], 1 if elem[0] == player_position else 0)), enumerate(self._source.elements)))
        # append colors to output

        line_break_index = len(output) - w
        while line_break_index > 0:
            output.insert(line_break_index, '\n')
            line_break_index -= w

        print(
            '\033[K' + ''.join(output) + ConsoleBoardView.REST_COLORS_CMD, 
            end='\033[F' * (h - 1), 
            flush=True
        )
    
    @staticmethod
    def set_text_color_cmd(color_index: int):
        return ConsoleBoardView.set_color_cmd(30 + color_index)
    
    @staticmethod
    def set_color_cmd(cmd_int: int):
        return '\x1b[' + str(cmd_int) + 'm'
    