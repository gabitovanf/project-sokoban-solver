from structure.Queue import Queue
from sokoban.SokobanBoard import SokobanBoard


class AbstractSearch:
    def __init__(self, board: SokobanBoard):
        self._board = board

    def bfs(self, start_position: int, apply_to_reached):
        frontier = Queue()
        reached = set()
        frontier.enqueue(start_position)
        reached.add(start_position)

        while not frontier.is_empty:
            current = frontier.dequeue()
            for next in self._board.get_neighbors(current):
                if next not in reached:
                    frontier.enqueue(next)
                    reached.add(next)
                    apply_to_reached(next)

