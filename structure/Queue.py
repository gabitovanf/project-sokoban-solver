class Queue:
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        return self._items.pop(0)

    @property
    def is_empty(self):
        return len(self._items) < 1
    
    def __str__(self):
        return str(self._items)
