import sys
from structure.Stack import Stack
from structure.queue.Queue import Queue
from sokoban.GraphSearch import GraphSearch
from sokoban.board.SokobanBoard import SokobanBoard
from sokoban.solver.SokobanGraph import SokobanGraph
from sokoban.solver.SokobanGraphNodeGenerator import SokobanGraphNodeGenerator
# from sokoban.board.MoveDirection import MoveDirection
from sokoban.solver.BoardStateNode import BoardStateNode
from sokoban.solver.array_board_heuristic.BoxesToGoalsManhattan import BoxesToGoalsManhattan


class SokobanSolver():
    HEURISTIC_SIMPLE_MANHATTAN = 'HEURISTIC_SIMPLE_MANHATTAN'
    HEURISTIC_MINIMUM_MANHATTAN = 'HEURISTIC_MINIMUM_MANHATTAN'
    HEURISTIC_MID_PLAYER_TO_BOXES_MANHATTAN = 'HEURISTIC_MID_PLAYER_TO_BOXES_MANHATTAN'

    def __init__(self):
        super().__init__()

        self._graph = None

    def BFS(self, board: SokobanBoard, depth_limit: int = sys.maxsize, save_graph_nodes = True):
        graph = SokobanGraph(board) if save_graph_nodes else SokobanGraphNodeGenerator(board)
        self._graph = graph

        final_node = GraphSearch.BFS(
            graph, 
            graph.root, 
            lambda x: False, 
            lambda node: board.is_solution(node.state_stamp) or node.level > depth_limit
        )

        return self._get_result_tuple(board, final_node, depth_limit)

    def DFS_first_node_met(self, board: SokobanBoard, depth_limit: int = sys.maxsize, save_graph_nodes = True):
        return self._DFS(
            board, 
            depth_limit, 
            save_graph_nodes=save_graph_nodes, 
            search_minimum=False
        )
    
    def DFS(self, board: SokobanBoard, depth_limit: int = sys.maxsize, save_graph_nodes = True):
        return self._DFS(
            board, 
            depth_limit, 
            save_graph_nodes=save_graph_nodes, 
            search_minimum=True
        )
    
    def _DFS(self, board: SokobanBoard, depth_limit: int = sys.maxsize, save_graph_nodes: bool = True, search_minimum: bool = False):
        graph = SokobanGraph(board) if save_graph_nodes else SokobanGraphNodeGenerator(board)
        self._graph = graph

        final_node = GraphSearch.DFS(
            graph, 
            graph.root, 
            lambda x: False, 
            lambda node: board.is_solution(node.state_stamp),
            depth_limit=depth_limit,
            search_minimum=search_minimum
        )

        return self._get_result_tuple(board, final_node, depth_limit)
 
    def A_star(self, board: SokobanBoard, depth_limit: int = sys.maxsize, save_graph_nodes: bool = True, heuristic=None):
        graph = SokobanGraph(board) if save_graph_nodes else SokobanGraphNodeGenerator(board)
        self._graph = graph

        heuristic_function = SokobanSolver._get_heuristic(board, heuristic)

        final_node = GraphSearch.A_star(
            graph, 
            graph.root, 
            lambda x: False, 
            lambda node: board.is_solution(node.state_stamp),
            depth_limit=depth_limit,
            heuristic=heuristic_function
        )

        print('IS SOLUTION', board.is_solution(final_node.state_stamp), final_node.state_stamp)

        return self._get_result_tuple(board, final_node, depth_limit)
 
    def IDA_star(
            self,
            board: SokobanBoard, 
            start_depth_limit: int = 15, 
            increment_depth_limit: int = 10, 
            max_depth_limit: int = sys.maxsize, 
            save_graph_nodes: bool = True, 
            heuristic=None
        ):
        graph = SokobanGraph(board) if save_graph_nodes else SokobanGraphNodeGenerator(board)
        self._graph = graph

        heuristic_function = SokobanSolver._get_heuristic(board, heuristic)

        final_node = None
        solved = False
        depth_limit = start_depth_limit

        while not solved:
            final_node = GraphSearch.A_star(
                graph, 
                graph.root, 
                lambda x: False, 
                lambda node: board.is_solution(node.state_stamp),
                depth_limit=depth_limit,
                heuristic=heuristic_function
            )
            solved = board.is_solution(final_node.state_stamp)
            depth_limit += increment_depth_limit

            if depth_limit > max_depth_limit:
                break

        if not final_node:
            print('NO NODE FOUND')

        print('IS SOLUTION', board.is_solution(final_node.state_stamp), final_node.state_stamp)
        print('Depth limit:', depth_limit, 'of {start} + i * {delta}\n\n'.format(start=start_depth_limit, delta= increment_depth_limit))

        return self._get_result_tuple(board, final_node, depth_limit)
    
    @staticmethod
    def _get_heuristic(board: SokobanBoard, heuristic=None):
        heuristic_instance = BoxesToGoalsManhattan(board)

        if isinstance(heuristic, list):
            return heuristic_instance.combine(
                list(map(lambda h: SokobanSolver._get_heuristic(board, h), heuristic))
            )

        heuristic_function = heuristic_instance.simple_manhattan_heuristic  # Default

        if heuristic == SokobanSolver.HEURISTIC_MINIMUM_MANHATTAN:
            heuristic_function = heuristic_instance.min_manhattan_heuristic

        elif heuristic == SokobanSolver.HEURISTIC_MID_PLAYER_TO_BOXES_MANHATTAN:
            # heuristic_function = heuristic_instance.mid_player_to_boxes_manhattan_heuristic
            heuristic_function = heuristic_instance.mid_player_to_free_boxes_manhattan_heuristic

        return heuristic_function

    def _reconstruct_result_from_node(self, board: SokobanBoard, final_node: BoardStateNode) -> tuple:
        result_action_stack = Stack()
        result_player_position_str = ''

        node = final_node
        while node:
            _, player_position, _, _ = node.state_stamp

            if len(result_player_position_str) > 0:
                result_player_position_str += ', '
            result_player_position_str += str(board.element_x(player_position)) + ' ' + str(board.element_y(player_position))
            
            result_action_stack.push(node.action)

            node = node.parent_node

        return result_action_stack, result_player_position_str
    
    def _result_from_records(self, board: SokobanBoard, path_actions: Queue, path_state_stamps: Queue) -> tuple:
        result_player_position_str = ''
        result_action_stack = Stack()

        for i in range(len(path_actions) - 1, -1, -1):
            result_action_stack.push(path_actions[i])

        for i in range(0, len(path_state_stamps), 1):
            _, player_position, _, _ = path_state_stamps[i]

            if len(result_player_position_str) > 0:
                result_player_position_str += ', '
            result_player_position_str += str(board.element_x(player_position)) + ' ' + str(board.element_y(player_position))

        return result_action_stack, result_player_position_str
    
    def _get_result_tuple(self, board: SokobanBoard, final_node: BoardStateNode, depth_limit: int) -> tuple:
        if final_node is None:
            return False, Stack(), '', depth_limit
        
        result = (self._result_from_records(board, final_node.path_actions, final_node.path_state_stamps) 
                  if final_node.has_path_records 
                  else self._reconstruct_result_from_node(board, final_node))
        
        if final_node.level > depth_limit and not board.is_solution(final_node.state_stamp):
            return (False,) + result + (final_node.level,)

        return (True,) + result + (final_node.level,)



        
