class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    @property
    def is_empty(self):
        return len(self._items) < 1
    
    def __str__(self):
        return str(self._items)
