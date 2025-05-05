from sokoban.control.modes.IPlayerMode import IPlayerMode
from sokoban.control.AbstractSequencePlayer import AbstractSequencePlayer
from sokoban.board.ISokobanBoard import ISokobanBoard
from sokoban.board.MoveDirection import MoveDirection


class SokobanActionMode(IPlayerMode):
    def __init__(self, player: AbstractSequencePlayer, board: ISokobanBoard):
        super().__init__(player, board)
        self._player = player
        self._board = board

    def setup(self, record_stack):
        self._player.from_stack(record_stack)

    def update(self):
        if self._player.is_empty:
            return
        
        move = self._player.next()

        if move == MoveDirection.NO:
            return

        if not self._board.can_move(move):
            player_position = self._board.player_position
            print('Incorrect action {0} recorded when player at ({1}, {2})'.format(move, self._board.element_x(player_position), self._board.element_y(player_position)))
        self._board.move(move)

            
