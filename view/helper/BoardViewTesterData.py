from view.IBoardData import IBoardData

class BoardViewTesterData(IBoardData):
    def __init__(self, width: int, height: int):
        length = width * height
        self._width = width
        self._height = height
        self._elements = [] if length < 1 else list(map(lambda a: 0, range(length)))
        self._elements[width] = 2

    def update(self):
        self._elements.insert(0, self._elements.pop())

    @property
    def elements(self):
        return self._elements

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
