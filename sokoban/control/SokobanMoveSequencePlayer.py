from sokoban.board.SokobanBoard import SokobanBoard
from sokoban.control.modes.SokobanSinglePlayerMode import SokobanSinglePlayerMode
from sokoban.control.modes.SokobanActionMode import SokobanActionMode
from sokoban.control.AbstractSequencePlayer import AbstractSequencePlayer


class SokobanMoveSequencePlayer(AbstractSequencePlayer):
    MODE_SINGLE_AGENT_POSITION = 'single'
    MODE_ACTION = 'action'

    def __init__(self, board: SokobanBoard):
        super().__init__()
        self._board = board
        self._mode = SokobanMoveSequencePlayer.MODE_SINGLE_AGENT_POSITION
        self._mode_helper = SokobanSinglePlayerMode(self, self._board)

    def play(self, record, mode: str = 'single'):
        super(SokobanMoveSequencePlayer, self).play(record)
        self.clear()

        if mode != self._mode:
            self._mode = mode

            if mode == SokobanMoveSequencePlayer.MODE_SINGLE_AGENT_POSITION:
                self._mode_helper = SokobanSinglePlayerMode(self, self._board)

            elif mode == SokobanMoveSequencePlayer.MODE_ACTION:
                self._mode_helper = SokobanActionMode(self, self._board)

        self._mode_helper.setup(record)

    def update(self):
        self._mode_helper.update()

