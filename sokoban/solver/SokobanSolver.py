from structure.Stack import Stack
from structure.queue.Queue import Queue
from sokoban.GraphSearch import GraphSearch
from sokoban.board.SokobanBoard import SokobanBoard
from sokoban.solver.SokobanGraph import SokobanGraph
from sokoban.solver.SokobanGraphNodeGenerator import SokobanGraphNodeGenerator
# from sokoban.board.MoveDirection import MoveDirection
from sokoban.solver.BoardStateNode import BoardStateNode


class SokobanSolver():
    def __init__(self):
        super().__init__()

        self._graph = None

    def BFS(self, board: SokobanBoard, max_levels: int = 15, save_graph_nodes = True):
        graph = SokobanGraph(board) if save_graph_nodes else SokobanGraphNodeGenerator(board)
        self._graph = graph

        final_node = GraphSearch.BFS(
            graph, 
            graph.root, 
            lambda x: False, 
            lambda node: board.is_solution(node.state_stamp) or node.level > max_levels
        )

        return self._get_result_tuple(board, final_node, max_levels)

    def DFS_first_node_met(self, board: SokobanBoard, max_levels: int = 15, save_graph_nodes = True):
        return self._DFS(
            board, 
            max_levels, 
            save_graph_nodes=save_graph_nodes, 
            search_minimum=False
        )
    
    def DFS(self, board: SokobanBoard, max_levels: int = 15, save_graph_nodes = True):
        return self._DFS(
            board, 
            max_levels, 
            save_graph_nodes=save_graph_nodes, 
            search_minimum=True
        )
    
    def _DFS(self, board: SokobanBoard, max_levels: int = 15, save_graph_nodes: bool = True, search_minimum: bool = False):
        graph = SokobanGraph(board) if save_graph_nodes else SokobanGraphNodeGenerator(board)
        self._graph = graph

        final_node = GraphSearch.DFS(
            graph, 
            graph.root, 
            lambda x: False, 
            lambda node: board.is_solution(node.state_stamp),
            max_level=max_levels,
            search_minimum=search_minimum
        )

        return self._get_result_tuple(board, final_node, max_levels)
 
    def A_star(self, board: SokobanBoard):
        # player_position = self._board.player_position
        pass

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
    
    def _result_from_queues(self, board: SokobanBoard, path_actions_queue: Queue, path_state_stamps_queue: Queue) -> tuple:
        result_player_position_str = ''
        result_action_stack = Stack()

        queue = Queue()
        while not path_actions_queue.is_empty:
            queue.enqueue(path_actions_queue.dequeue())
        while not queue.is_empty:
            result_action_stack.push(queue.dequeue())
            
        while not path_state_stamps_queue.is_empty:
            queue.enqueue(path_actions_queue.dequeue())
        while not queue.is_empty:
            _, player_position, _, _ = queue.dequeue()

            if len(result_player_position_str) > 0:
                result_player_position_str += ', '
            result_player_position_str += str(board.element_x(player_position)) + ' ' + str(board.element_y(player_position))

        return result_action_stack, result_player_position_str
    
    def _get_result_tuple(self, board: SokobanBoard, final_node: BoardStateNode, max_levels: int) -> tuple:
        if final_node is None:
            return False, Stack(), '', max_levels
        
        result = (self._result_from_queues(board, final_node.path_actions_queue, final_node.path_state_stamps_queue) 
                  if final_node.has_path_queues 
                  else self._reconstruct_result_from_node(board, final_node))
        
        if final_node.level > max_levels and not board.is_solution(final_node.state_stamp):
            return (False,) + result + (final_node.level,)

        return (True,) + result + (final_node.level,)



        
