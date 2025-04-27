from sokoban.control.AbstractSequencePlayer import AbstractSequencePlayer
from sokoban.SokobanBoard import SokobanBoard


class SokobanSinglePlayerMode:
    def __init__(self, player: AbstractSequencePlayer, board: SokobanBoard):
        self._player = player
        self._board = board

    def fill_queue(self, sequence: str):
        self._parse_single_agent_positions(sequence)

    def update(self):
        move = self._player.sequence_queue.dequeue()
        self._board.player_position = self._board.element_index(move[0], move[1])

    def _parse_single_agent_positions(self, sequence: str):
        i = (sequence
             .strip()
             .find(','))
        while len(sequence) > 0 and i > 0:
            point_str = sequence[0:i]
            sequence = sequence[(i + 1):].strip()
            i = sequence.find(',')

            if not ' ' in point_str:
                continue

            j = point_str.find(' ')
            x = float(point_str[0:j].strip())
            y = float(point_str[j:].strip())

            self._player.sequence_queue.enqueue((x, y))
            
