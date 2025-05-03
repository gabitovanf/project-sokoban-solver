from sokoban.ISearchGraph import ISearchGraph
from sokoban.board.ISokobanBoard import ISokobanBoard
from sokoban.board.MoveDirection import MoveDirection, MOVE_ACTIONS
from sokoban.solver.BoardStateAndPathNode import BoardStateAndPathNode

# get_neighbors returns similar nodes
# But Instance doesn't save graph nodes except the root
class SokobanGraphNodeGenerator(ISearchGraph):
    MAX_LEVEL = 1 << 50

    def __init__(self, board: ISokobanBoard):
        super().__init__()

        self._board = board
        self._root_node = BoardStateAndPathNode(None, board.get_state_stamp(), MoveDirection.NO, 0)

    @property
    def root(self) -> BoardStateAndPathNode:
        return self._root_node
    
    def get_neighbors(self, current: BoardStateAndPathNode) -> list:
        children = []
        children_level = current.level + 1
        path_cost = current.path_cost

        if children_level > SokobanGraphNodeGenerator.MAX_LEVEL:
            return children

        backward_move = MoveDirection.reversed(current.action)
        # for i in range(0, len(MOVE_ACTIONS) + 1, 1):
        #     # Backward move make last
        #     move = 0
        #     if i > len(MOVE_ACTIONS) - 1:
        #         move = backward_move
        #     else:
        #         move = MOVE_ACTIONS[i]
        #         if move == backward_move:
        #             continue
        for i in range(0, len(MOVE_ACTIONS), 1):
            # Omit backward move
            move = MOVE_ACTIONS[i]
            if move == backward_move:
                continue

            self._board.restore_state_from_stamp(current.state_stamp)

            if not self._board.can_move(move):
                continue

            self._board.move(move)

            new_node = BoardStateAndPathNode(
                current, 
                self._board.get_state_stamp(), 
                move, 
                children_level, 
                path_cost=path_cost + 1
            )
            # current.append(new_node)
            children.append(new_node)

        # print('LEVEL', children_level, end='\r', flush=True)
        return children






        

        
