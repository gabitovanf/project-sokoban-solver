from sokoban.control.modes.IPlayerMode import IPlayerMode
from sokoban.control.AbstractSequencePlayer import AbstractSequencePlayer
from sokoban.board.SokobanBoard import SokobanBoard


class SokobanPlayerPositionMode(IPlayerMode):
    def __init__(self, player: AbstractSequencePlayer, board: SokobanBoard):
        super().__init__(player, board)
        self._player = player
        self._board = board

    def setup(self, sequence):
        self._parse_single_agent_positions(str(sequence))

    def update(self):
        if self._player.is_empty:
            return
        
        move = self._player.next()
        self._board.player_position = self._board.element_index(move[0], move[1])

    def _parse_single_agent_positions(self, sequence: str):
        i = (sequence
             .strip()
             .rfind(','))
        while len(sequence) > 0 and i > 0:
            point_str = sequence[(i + 1):].strip()
            sequence = sequence[0:i].strip()
            i = sequence.rfind(',')

            if not ' ' in point_str:
                continue

            j = point_str.find(' ')
            x = float(point_str[0:j].strip())
            y = float(point_str[j:].strip())

            self._player.push((x, y))
            
