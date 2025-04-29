from structure.Stack import Stack


class AbstractSequencePlayer:
    def __init__(self):
        self._sequence_stack = Stack()

    def play(self, record):
        pass

    def update(self):
        pass

    def next(self):
        return self._sequence_stack.pop()

    def push(self, item):
        return self._sequence_stack.push(item)

    def from_stack(self, record):
        self._sequence_stack = record

    @property
    def is_empty(self):
        return self._sequence_stack.is_empty
            
    def clear(self):
        while not self._sequence_stack.is_empty:
            self._sequence_stack.pop()
