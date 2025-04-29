class MoveDirection:
    UP = 1
    RIGHT = 2
    DOWN = -1
    LEFT = -2
    NO = 0

    @staticmethod
    def reversed(move):
        return -move

MOVE_ACTIONS = [MoveDirection.UP, MoveDirection.RIGHT, MoveDirection.DOWN, MoveDirection.LEFT]
