from sokoban.SokobanBoard import SokobanBoard
from sokoban.control.modes.SokobanSinglePlayerMode import SokobanSinglePlayerMode
from sokoban.control.AbstractSequencePlayer import AbstractSequencePlayer
from structure.Queue import Queue


class SokobanMoveSequencePlayer(AbstractSequencePlayer):
    MODE_SINGLE_AGENT_POSITION = 'single'

    def __init__(self, board: SokobanBoard):
        super().__init__()
        self._board = board
        self._mode = 'none'
        self._mode_helper = None

    def play(self, sequence: str, mode: str = 'single'):
        super(SokobanMoveSequencePlayer, self).play(sequence)
        self.clear_queue()

        if mode != self._mode:
            self._mode = mode

            if mode == SokobanMoveSequencePlayer.MODE_SINGLE_AGENT_POSITION:
                self._mode_helper = SokobanSinglePlayerMode(self, self._board)

        self._mode_helper.fill_queue(sequence)

    def update(self):
        self._mode_helper.update()

