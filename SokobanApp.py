from pynput import keyboard
from time import sleep

from view.console.ConsoleBoardView import ConsoleBoardView
from view.console.SokobanCellValueMapper import SokobanCellValueMapper
from view.helper.BoardViewTesterData import BoardViewTesterData
from utils.Ticker import Ticker
from sokoban.SokobanBoard import SokobanBoard


level_str = 'ew0KICAiQm9hcmQiOiBbDQogICIgICAjIyMiLA0KICAiICAjIyAjICMjIyMiLA0KICAiICMjICAjIyMgICMiLA0KICAiIyMgJCAgICAgICMiLA0KICAiIyAgIEAkICMgICMiLA0KICAiIyMjICQjIyMgICMiLA0KICAiICAjICAjLi4gICMiLA0KICAiICMjICMjLiMgIyMiLA0KICAiICMgICAgICAjIyIsDQogICIgIyAgICAgIyMiLA0KICAiICMjIyMjIyMiDQogIF0sDQogICJMZXZlbCBTZXQiOiAiU29sdmVyIFN0YXRpc3RpY3MgTGV2ZWwiLA0KICAiTGV2ZWwgVGl0bGUiOiAiU2FzcXVhdGNoIHwgTGV2ZWwgMSIsDQogICJMZXZlbCBOby4iOiAxDQp9'


def main():
    ticker = Ticker(10, True)
    board_tester = BoardViewTesterData(10, 10)
    board_sokoban = SokobanBoard.create_from_json_encoded(level_str)
    board_view = ConsoleBoardView(board_sokoban, SokobanCellValueMapper())

    print('\n')
    board_view.render()

    def update():
        # board_tester.update()
        board_view.render()

    ticker.register_observer_func(update)

    ticker.start()
    
# START:
keyboard.Listener.start
main()

# cd project-sokoban-solver
# python3 SokobanApp.pynt= ' 'r r alse  
 