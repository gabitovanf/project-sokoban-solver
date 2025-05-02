from structure.matrix.IMatrix import IMatrix


class ListMatrix(IMatrix):
    def __init__(self, cols: int, rows: int, fill_with = 0):
        elements = [None] * rows

        for row_index in range(0, rows, 1):
            elements[row_index] = [fill_with] * cols

        self._elements = elements
        self._cols = cols

    def get(self, col_index, row_index):
        return self._elements[row_index][col_index]

    def row(self, row_index):
        return self._elements[row_index]

    def set(self, col_index, row_index, value):
        self._elements[row_index][col_index] = value

    def clone(self):
        clone = ListMatrix(self.cols, self.rows)
        clone._elements = list(map(lambda r: r.copy(), self._elements))

        return clone

    def is_zero(self):
        return all(list(map(lambda a: all(list(map(lambda b: b == 0, a))), self._elements)))

    # TO TEST ONLY
    # TODO: REMOVE
    def _setAll(self, elements: list):
        self._elements = elements

    @property
    def rows(self):
        return len(self._elements)

    @property
    def cols(self):
        return self._cols

    def __str__(self) -> str:
        return ('ListMatrix: [' + ', \n'.join(list(map(
            lambda x: '{index}: {row}'.format(index=x[0], row=x[1]),
            enumerate(self._elements)
        ))) + ']')