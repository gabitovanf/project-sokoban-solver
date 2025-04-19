import json
from sokoban.utils.UrlStringEncoder import UrlStringEncoder

class AbstractBoard:
    def __init__(self, width: int, height: int, fill_with=0):
        size = width * height
        self._width = width
        self._height = height
        self._size = size
        self._elements = [] if size < 1 else list(map(lambda a: fill_with, range(size)))

        # Optional to use
        self._player_position = -1

        # INFO
        self._title = 'No Name'
        self._level = 0
        self._level_set = 'No Name'

    @staticmethod
    def create_from_str(input_str: str):
        pass

    @staticmethod
    def create_from_json_encoded(input_str: str):
        decoded_json_dict = AbstractBoard.parse_json_encoded(input_str)

        return AbstractBoard.create_from_str(decoded_json_dict.get('Board', ''))

    @staticmethod
    def parse_json_encoded(input_str: str):
        decoded_str = UrlStringEncoder.decode(input_str)
        decoded_json_dict = json.loads(decoded_str)

        return decoded_json_dict

    def element_index(self, x_index: int, y_index: int) -> int:
        return y_index * self.width + x_index

    @property
    def elements(self):
        return self._elements

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def size(self):
        return self._size

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def level_set(self):
        return self._level_set

    @level_set.setter
    def level_set(self, value):
        self._level_set = value

    @property
    def player_position(self):
        return self._player_position

    @player_position.setter
    def player_position(self, value):
        self._player_position = value

    @property
    def is_solved(self) -> bool:
        pass
    