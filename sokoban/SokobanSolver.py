from sokoban.AbstractSearch import AbstractSearch
from sokoban.SokobanBoard import SokobanBoard


class SokobanSolver(AbstractSearch):
    def __init__(self, board: SokobanBoard):
        super().__init__(board)

    # Get active board cells (elements), i.e. inner not-wall elements
    # def bfs(self, start_position: int):
    #    super

    # Move the man from the current position to another position
    def a_star(self, target_position: int):
        player_position = self._board.player_position

        
