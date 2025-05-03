# from pynput import keyboard
import time

from view.console.ConsoleBoardView import ConsoleBoardView
from view.console.SokobanCellValueAndStateMapper import SokobanCellValueAndStateMapper
from view.console.SokobanBoardElementMapper import SokobanBoardElementMapper
from view.helper.BoardViewTesterData import BoardViewTesterData
from utils.Ticker import Ticker
from sokoban.board.SokobanBoard import SokobanBoard
from sokoban.board.SokobanIntMasksBoard import SokobanIntMasksBoard
from sokoban.board.CreateSokobanBoard import create_from_str, create_from_json_encoded
from sokoban.board.MoveDirection import MoveDirection
from sokoban.solver.SokobanSolver import SokobanSolver
from sokoban.control.SokobanMoveSequencePlayer import SokobanMoveSequencePlayer
from structure.Stack import Stack

# A-star + simple heuristic:
# REF 10000 REACHED AT 2.2786099910736084 - list-board
# REF 100000 REACHED AT 113.67122483253479 - list-board
# REF 10000 REACHED AT 1.7212588787078857 - bit-board
# REF 100000 REACHED AT 116.42463803291321, 109.74020385742188 - bit-board
# level_json_str = 'ew0KICAiQm9hcmQiOiBbDQogICIgICAjIyMiLA0KICAiICAjIyAjICMjIyMiLA0KICAiICMjICAjIyMgICMiLA0KICAiIyMgJCAgICAgICMiLA0KICAiIyAgIEAkICMgICMiLA0KICAiIyMjICQjIyMgICMiLA0KICAiICAjICAjLi4gICMiLA0KICAiICMjICMjLiMgIyMiLA0KICAiICMgICAgICAjIyIsDQogICIgIyAgICAgIyMiLA0KICAiICMjIyMjIyMiDQogIF0sDQogICJMZXZlbCBTZXQiOiAiU29sdmVyIFN0YXRpc3RpY3MgTGV2ZWwiLA0KICAiTGV2ZWwgVGl0bGUiOiAiU2FzcXVhdGNoIHwgTGV2ZWwgMSIsDQogICJMZXZlbCBOby4iOiAxDQp9'
# level_json_str = 'ew0KICAiQm9hcmQiOiBbDQogICIgIyMgIyMjIyMiLA0KICAiIyMgIyMgLiAjIiwNCiAgIiMgIyMgJC4gIyIsDQogICIgIyMgJCAgICMiLA0KICAiIyMgJEAgIyMjIiwNCiAgIiMgJCAgIyMiLA0KICAiIy4uICMjICMjIiwNCiAgIiMgICAjICMjIiwNCiAgIiMjIyMjICMiDQogIF0sDQogICJMZXZlbCBTZXQiOiAiU29sdmVyIFN0YXRpc3RpY3MgTGV2ZWwiLA0KICAiTGV2ZWwgVGl0bGUiOiAiU2FzcXVhdGNoIHwgTGV2ZWwgMiIsDQogICJMZXZlbCBOby4iOiAyDQp9'

# SUPER SIMPLE MAZE. ONE BOX
# level_str = '\n'.join([
#     '##########',
#     '#-------@#',
#     '#-------$#',
#     '#--------#',
#     '#-------.#',
#     '##########'
# ])

# SIMPLE I. ONE BOX
# level_str = '\n'.join([
#     '##########',
#     '#--------#',
#     '#-@----$-#',
#     '#--------#',
#     '#-------.#',
#     '##########'
# ])

# SIMPLE II. ONE BOX
# level_str = '\n'.join([
#     '##########',
#     '#--------#',
#     '#-@----$-#',
#     '#------#-#',
#     '#------#.#',
#     '##########'
# ])

# SIMPLE III.v1. ONE BOX
# BFS failed - 15 attempt levels
# DFS failed - 15 attempt levels
# A_star waited for 13 attempt levels
# A_star + simple manhattan + "mid player to boxes" heuristic - 17 attempt levels, NUM REACHED 161438, TIME ELAPSED 200.00371408462524
# -- result: [2, 2, -1, -2, -1, -1, -2, 1, -2, -1, 2, 2, 1, 2, 2, 2, 2, 0] 2 2, 3 2, 4 2, 5 2, 6 2, 6 1, 7 1, 8 1, 8 2, 7 2, 7 1, 6 1, 6 2, 6 3, 5 3, 5 4, 6 4, 7 4
# A_star + minimum manhattan + "mid player to boxes" heuristic - 17 attempt levels, NUM REACHED 161438, TIME ELAPSED 208.52746438980103
# level_str = '\n'.join([
#     '##########',
#     '#--------#',
#     '#-@----$-#',
#     '#------###',
#     '#-------.#',
#     '##########'
# ])

# SIMPLE III.v2. ONE BOX
# BFS succeeded - 10 attempt levels
# DFS succeeded - 14 attempt levels
# A_star succeeded - 10 attempt levels, NUM REACHED 1166
# IDA_star succeeded - 10 attempt levels, NUM REACHED 766, TIME ELAPSED 0.08143186569213867, Depth limit: 20 of 10 + i * 10
# level_str = '\n'.join([
#     '##########',
#     '#-------@#',
#     '#------$-#',
#     '#------###',
#     '#-------.#',
#     '##########'
# ])

# SIMPLE III.v3. ONE BOX
# A_star succeeded - 13 attempt levels, NUM REACHED 28198 (до отладки простой эвристики 61857; простая и минимальная эвристики одинаковые для одной коробки)
level_str = '\n'.join([
    '##########',
    '#----@---#',
    '#------$-#',
    '#------###',
    '#-------.#',
    '##########'
])

# SIMPLE. IV.v1. TOW BOXS
# BFS failed - 15 attempt levels
# A_star + simple manhattan heuristic succeeded - 15 attempt levels, NUM REACHED 13114, TIME ELAPSED 2.428982973098755
# A_star + minimum manhattan heuristic succeeded - 15 attempt levels, NUM REACHED 7298, TIME ELAPSED 1.3173191547393799
# A_star + simple manhattan heuristic succeeded + Bit Board - 15 attempt levels, NUM REACHED 13114, TIME ELAPSED 2.1312520503997803
# A_star + minimum manhattan heuristic succeeded + Bit Board - 15 attempt levels, NUM REACHED 7298, TIME ELAPSED 1.1381828784942627
# A_star + simple manhattan + "mid player to boxes" heuristic succeeded + Bit Board - 15 attempt levels, NUM REACHED 3744, TIME ELAPSED 0.4002370834350586
# A_star + minimum manhattan + "mid player to boxes" heuristic succeeded + Bit Board - 15 attempt levels, NUM REACHED 1913, TIME ELAPSED 0.24763798713684082
# A_star + minimum manhattan + "mid player to free boxes" heuristic succeeded + Bit Board - 15 attempt levels, NUM REACHED 2182, TIME ELAPSED 0.21687817573547363
# level_str = '\n'.join([
#     '##########',
#     '#--------#',
#     '#-@----$-#',
#     '#--$----.#',
#     '#-------.#',
#     '##########'
# ])

# SIMPLE. IV.v2. TOW BOXS
# Not solved yet
# level_str = '\n'.join([
#     '##########',
#     '#--------#',
#     '#------$-#',
#     '#-@----###',
#     '#--$----.#',
#     '#-------.#',
#     '##########'
# ])
test_player_moves = '1 1, 1 2, 2 2, 2 3, 3 3, 3 4, 4 4'

def main():
    # board_tester = BoardViewTesterData(10, 10) # elements

    # BOARD OPTIONS:
    # board_sokoban = create_from_json_encoded(level_json_str, SokobanBoard)
    # board_sokoban = create_from_str(level_str, SokobanBoard)
    # board_sokoban = create_from_json_encoded(level_json_str, SokobanIntMasksBoard)
    board_sokoban = create_from_str(level_str, SokobanIntMasksBoard)

    if isinstance(board_sokoban, str):
        print(board_sokoban)

        return False
    
    # VIEW 
    # depending on board implementation:
    # - array board
    # board_view = ConsoleBoardView(board_sokoban, SokobanCellValueAndStateMapper())
    # - bit operator board
    board_view = ConsoleBoardView(board_sokoban, SokobanBoardElementMapper(board_sokoban))

    ticker = Ticker(5, True)
    solver = SokobanSolver()
    move_player = SokobanMoveSequencePlayer(board_sokoban)

    # Store InitialState
    ## BEFORE SOLVER >> 
    board_sokoban.store_state()
    start_time = time.time()

    # SOLVER OPTIONS:
    # success, actions_stack, result_player_position_str, result_level = solver.BFS(board_sokoban, 15)
    # success, actions_stack, result_player_position_str, result_level = solver.DFS_first_node_met(board_sokoban, 20)
    # success, actions_stack, result_player_position_str, result_level = solver.DFS(board_sokoban, 20)

    # A*:
    # success, actions_stack, result_player_position_str, result_level = solver.A_star(
    #     board_sokoban, 
    #     20, 
    #     save_graph_nodes=False,
    #     heuristic=SokobanSolver.HEURISTIC_SIMPLE_MANHATTAN
    # )
    success, actions_stack, result_player_position_str, result_level = solver.A_star(
        board_sokoban, 
        30, 
        save_graph_nodes=False,
        heuristic=SokobanSolver.HEURISTIC_MINIMUM_MANHATTAN
    )
    # success, actions_stack, result_player_position_str, result_level = solver.A_star(
    #     board_sokoban, 
    #     20, 
    #     save_graph_nodes=False,
    #     heuristic=[SokobanSolver.HEURISTIC_SIMPLE_MANHATTAN, SokobanSolver.HEURISTIC_MID_PLAYER_TO_BOXES_MANHATTAN]
    # )
    # success, actions_stack, result_player_position_str, result_level = solver.A_star(
    #     board_sokoban, 
    #     20, 
    #     save_graph_nodes=False,
    #     heuristic=[SokobanSolver.HEURISTIC_MINIMUM_MANHATTAN, SokobanSolver.HEURISTIC_MID_PLAYER_TO_BOXES_MANHATTAN]
    # )

    # IDA*:
    # success, actions_stack, result_player_position_str, result_level = solver.IDA_star(
    #     board_sokoban, 
    #     start_depth_limit=10,
    #     increment_depth_limit=10,
    #     max_depth_limit=100, 
    #     save_graph_nodes=False,
    #     heuristic=SokobanSolver.HEURISTIC_MINIMUM_MANHATTAN
    # )
    # success, actions_stack, result_player_position_str, result_level = solver.IDA_star(
    #     board_sokoban, 
    #     start_depth_limit=10,
    #     increment_depth_limit=10,
    #     max_depth_limit=100, 
    #     save_graph_nodes=False,
    #     heuristic=[SokobanSolver.HEURISTIC_MINIMUM_MANHATTAN, SokobanSolver.HEURISTIC_MID_PLAYER_TO_BOXES_MANHATTAN]
    # )

    ## AFTER SOLVER >> 
    time_elapsed = time.time() - start_time
    board_sokoban.restore_state()

    # TEST static state:
    # board_sokoban.restore_state_from_stamp(([18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 24, 24, 24, 24, 24, 24, 24, 8, 18, 18, 24, 24, 24, 24, 24, 24, 24, 24, 18, 18, 24, 24, 24, 24, 24, 24, 24, 24, 18, 18, 24, 24, 24, 24, 24, 24, 24, 13, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18], 38, 3, 2))
    # board_sokoban.restore_state_from_stamp(([18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 24, 24, 24, 24, 24, 24, 24, 24, 18, 18, 24, 8, 24, 24, 24, 24, 24, 24, 18, 18, 24, 24, 24, 24, 24, 24, 24, 24, 18, 18, 24, 24, 24, 24, 24, 24, 24, 13, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18], 38, 4095, 9))

    # SAVED RESULT TO PLAY
    # success = True
    # path_actions = [2, 2, -1, -2, -1, -1, -2, 1, -2, -1, 2, 2, 1, 2, 2, 2, 2, 0] 
    # result_player_position_str = '2 2, 3 2, 4 2, 5 2, 6 2, 6 1, 7 1, 8 1, 8 2, 7 2, 7 1, 6 1, 6 2, 6 3, 5 3, 5 4, 6 4, 7 4' 
    # result_level = 17
    # actions_stack = Stack()
    # for i in range(0, len(path_actions), 1):
    #     actions_stack.push(path_actions[i])

    # RUSULT PLAYING:
    print('\nSUCCESS' if success else 'FAILED')
    print(actions_stack, result_player_position_str)
    print('FOUND AT LEVEL', result_level)
    print('TIME ELAPSED', time_elapsed)
    print('\n')
    board_view.render()
    move_player.play(actions_stack, SokobanMoveSequencePlayer.MODE_ACTION)

    # TEST STATIC VIEW
    board_view.render()
    # TEST player's moves only
    # move_player.play(result_player_position_str)

    def update():
        # board_tester.update()

        # TEST moving
        # move = MoveDirection.RIGHT
        # if board_sokoban.can_move(move):
        #     board_sokoban.move(move)

        # Invalidate player:
        move_player.update()

        # Render:
        board_view.render()

    ticker.register_observer_func(update)

    ticker.start()

# START:
main()

# cd project-sokoban-solver
# python3 SokobanApp.py  
 