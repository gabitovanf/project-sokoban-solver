from view.console.ConsoleBoardView import ConsoleBoardView
from view.console.SokobanCellValueMapper import SokobanCellValueMapper


class SokobanCellValueAndStateMapper(SokobanCellValueMapper):
    def __init__(self):
        super().__init__()

    def value_to_view(self, cell_value_tuple):
        value, player_is_on = cell_value_tuple
        symblol = super(SokobanCellValueAndStateMapper, self).value_to_view(cell_value_tuple)

        change_color_if_active = ''
        reset_color_if_active = ''
        
        # Make active elements BLUE
        # change_color_if_active = ConsoleBoardView.set_text_color_cmd(ConsoleBoardView.BLUE) if value & 8 != 0 else ''
        # reset_color_if_active = ConsoleBoardView.REST_COLORS_CMD if value & 8 != 0 else ''

        # add some space with ' ' 
        return change_color_if_active + symblol + reset_color_if_active
