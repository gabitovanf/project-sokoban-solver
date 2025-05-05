import sys
import colorama
from view.AbstractBoardView import AbstractBoardView
from view.IBoardData import IBoardData
from view.IValueMapper import IValueMapper

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

    def __init__(self, source: IBoardData, value_mapper: IValueMapper=None, *args, **kwargs):
        super(ConsoleBoardView, self).__init__(source, value_mapper=value_mapper, *args, **kwargs)

    def render(self):
        # The size of the board must not change!

        w = self._source.width
        h = self._source.height
        output = []

        for i in range(0, self._source.size, 1):
            output.append(self._value_mapper.get_view_at_index(self._source, i))
            
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
    