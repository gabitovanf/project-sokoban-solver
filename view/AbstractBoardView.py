from view.IBoardData import IBoardData
from view.IValueMapper import IValueMapper

class AbstractBoardView:
    def __init__(self, source: IBoardData, value_mapper: IValueMapper=None, *args, **kwargs):
        self._source = source
        self._value_mapper = value_mapper

    def render():
        pass