from pynput import keyboard
from time import sleep

from view.console.ConsoleBoardView import ConsoleBoardView
from view.console.SokobanCellValueAndStateMapper import SokobanCellValueAndStateMapper
from view.helper.BoardViewTesterData import BoardViewTesterData
from utils.Ticker import Ticker
from sokoban.SokobanBoard import SokobanBoard
from sokoban.SokobanSolver import SokobanSolver
from sokoban.control.SokobanMoveSequencePlayer import SokobanMoveSequencePlayer


# level_json_str = 'ew0KICAiQm9hcmQiOiBbDQogICIgICAjIyMiLA0KICAiICAjIyAjICMjIyMiLA0KICAiICMjICAjIyMgICMiLA0KICAiIyMgJCAgICAgICMiLA0KICAiIyAgIEAkICMgICMiLA0KICAiIyMjICQjIyMgICMiLA0KICAiICAjICAjLi4gICMiLA0KICAiICMjICMjLiMgIyMiLA0KICAiICMgICAgICAjIyIsDQogICIgIyAgICAgIyMiLA0KICAiICMjIyMjIyMiDQogIF0sDQogICJMZXZlbCBTZXQiOiAiU29sdmVyIFN0YXRpc3RpY3MgTGV2ZWwiLA0KICAiTGV2ZWwgVGl0bGUiOiAiU2FzcXVhdGNoIHwgTGV2ZWwgMSIsDQogICJMZXZlbCBOby4iOiAxDQp9'
level_str = '\n'.join([
    '##########',
    '#--------#',
    '#-@----$-#',
    '#--------#',
    '#-------.#',
    '##########'
])

def main():
    # board_tester = BoardViewTesterData(10, 10)
    # board_sokoban = SokobanBoard.create_from_json_encoded(level_str)
    board_sokoban = SokobanBoard.create_from_str(level_str)

    if isinstance(board_sokoban, str):
        print(board_sokoban)

        return False
    
    # board_sokoban.store_state()

    ticker = Ticker(10, True)
    board_view = ConsoleBoardView(board_sokoban, SokobanCellValueAndStateMapper())
    solver = SokobanSolver(board_sokoban)
    move_player = SokobanMoveSequencePlayer(board_sokoban)

    solver.a_star(board_sokoban.element_index(9, 5))

    print('\n')
    board_view.render()
    # move_player.play('1 1, 1 2, 2 2, 2 3, 3 3, 3 4, 4 4')

    def update():
        # board_tester.update()
        move_player.update()
        board_view.render()

    ticker.register_observer_func(update)

    ticker.start()
    
# START:
keyboard.Listener.start
main()

# cd project-sokoban-solver
# python3 SokobanApp.py  
 