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
        children = []
        children_level = current.level + 1
        path_cost = current.path_cost

        if children_level > SokobanGraph.MAX_LEVEL:
            return children

        backward_move = MoveDirection.reversed(current.action)
        for move in MOVE_ACTIONS:
            if move == backward_move:
                continue

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
            current.append(new_node)
            # children.append(new_node)

        # print('LEVEL', children_level, end='\r', flush=True)
        return current.children






        

        
