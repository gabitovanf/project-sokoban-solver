from sokoban.ISearchGraph import ISearchGraph
from sokoban.board.ISokobanBoard import ISokobanBoard
from sokoban.board.MoveDirection import MoveDirection, MOVE_ACTIONS
from sokoban.solver.BoardStateNode import BoardStateNode


class SokobanGraph(ISearchGraph):
    MAX_LEVEL = 1 << 50

    def __init__(self, board: ISokobanBoard):
        super().__init__()

        self._board = board
        self._root_node = BoardStateNode(board.get_state_stamp(), MoveDirection.NO, 0)

    @property
    def root(self) -> BoardStateNode:
        return self._root_node
    
    def get_neighbors(self, current: BoardStateNode) -> list:
        children_level = current.level + 1
        path_cost = current.path_cost

        if children_level > SokobanGraph.MAX_LEVEL:
            return []

        backward_move = MoveDirection.reversed(current.action)
        # OPTION 1
        # for i in range(0, len(MOVE_ACTIONS), 1):
        #     # Omit backward move
        #     move = MOVE_ACTIONS[i]
        #     if move == backward_move:
        #         continue
        # OPTION 2
        # for i in range(0, len(MOVE_ACTIONS) + 1, 1):
        #     # Backward move make last
        #     move = 0
        #     if i > len(MOVE_ACTIONS) - 1:
        #         move = backward_move
        #     else:
        #         move = MOVE_ACTIONS[i]
        #         if move == backward_move:
        #             continue

        # OPTION 3
        for i in range(0, len(MOVE_ACTIONS), 1):
            move = MOVE_ACTIONS[i]
            
            self._board.restore_state_from_stamp(current.state_stamp)

            if not self._board.can_move(move):
                continue

            self._board.move(move)

            new_node = BoardStateNode(
                self._board.get_state_stamp(),
                move, 
                children_level, 
                path_cost=path_cost + 1
            )

            # OPTION 3: Cut Backward move if it is the same as the previous state (before the current)
            if (current.parent_node is not None 
                and self._board.state_stamp_equal(current.parent_node.state_stamp, new_node.state_stamp)):
                continue

            current.append(new_node)

        # print('LEVEL', children_level, end='\r', flush=True)
        return current.children






        

        
