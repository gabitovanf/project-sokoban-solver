from sokoban.control.AbstractSequencePlayer import AbstractSequencePlayer
from sokoban.board.ISokobanBoard import ISokobanBoard


class IPlayerMode:
    def __init__(self, player: AbstractSequencePlayer, board: ISokobanBoard):
        pass

    def setup(self, sequence):
        pass

    def update(self):
        pass