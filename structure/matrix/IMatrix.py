class IMatrix:
    def get(self, col_index, row_index):
        pass

    def set(self, col_index, row_index, value):
        pass

    def row(self) -> list:
        pass

    def clone(self):
        pass

    def is_zero(self):
        pass

    @property
    def rows(self):
        pass

    @property
    def cols(self):
        pass