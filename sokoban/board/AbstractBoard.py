import json
from sokoban.utils.UrlStringEncoder import UrlStringEncoder
from sokoban.ISearchGraph import ISearchGraph

class AbstractBoard(ISearchGraph):
    def __init__(self, width: int, height: int, fill_with=0):
        self._width = width
        self._height = height
        self._size = width * height

        # Optional to use
        self._player_position = -1
        self._stored_state_clone = None

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

    def get_neighbors(self, element_index: int) -> int:
        elements = []

        if not self.is_top_edge(element_index):
            elements.append(element_index - self._width)
        if not self.is_right_edge(element_index):
            elements.append(element_index + 1)
        if not self.is_bottom_edge(element_index):
            elements.append(element_index + self._width)
        if not self.is_left_edge(element_index): 
            elements.append(element_index - 1)

        return elements

    def is_edge(self, element_index: int) -> int:
        return (self.is_bottom_edge(element_index)
                or self.is_top_edge(element_index)
                or self.is_left_edge(element_index) 
                or self.is_right_edge(element_index))

    def is_bottom_edge(self, element_index: int) -> int:
        return element_index > self._size - self._width - 1

    def is_top_edge(self, element_index: int) -> int:
        return element_index < self._width

    def is_left_edge(self, element_index: int) -> int:
        return self.element_x(element_index) < 1

    def is_right_edge(self, element_index: int) -> int:
        return self.element_x(element_index) > self._width - 2
    
    # def element_coords(self, index: int) -> int:
    #     return self.element_x(index), self.element_y(index)

    def element_x(self, index: int) -> int:
        return int(index % self.width)

    def element_y(self, index: int) -> int:
        return int(index / self.width)

    def clone(self):
        board = self.__class__(self.width, self.height)

        board.title = self.title
        board.level = self.level
        board.level_set = self.level_set
        self._copy_state_from_to(self, board)
        
        return board
    
    def store_state(self):
        self._stored_state_clone = self.clone()
    
    def clear_stored_state(self):
        self._stored_state_clone = None
    
    def restore_state(self):
        if self._stored_state_clone is None:
            return False
        
        self._copy_state_from_to(self._stored_state_clone, self)

        return True
    
    def _copy_state_from_to(self, from_board, to_board):
        to_board.player_position = from_board.player_position

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
    