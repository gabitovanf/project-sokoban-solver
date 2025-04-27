from structure.Queue import Queue


class AbstractSequencePlayer:
    def __init__(self):
        self._sequence_queue = Queue()

    def play(self, sequence: str):
        pass

    def update(self):
        pass

    @property
    def sequence_queue(self):
        return self._sequence_queue
            
    def clear_queue(self):
        while not self._sequence_queue.is_empty:
            self._sequence_queue.dequeue()
