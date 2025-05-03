from sokoban.board.ISokobanBoard import ISokobanBoard
from sokoban.board.AbstractArrayBoard import AbstractArrayBoard
from sokoban.board.MoveDirection import MoveDirection


class SokobanBoard(ISokobanBoard, AbstractArrayBoard):
    def __init__(self, width, height):
        super().__init__(width, height, 16)
        self._num_boxes = 0
        self._num_goals = 0
        self._num_boxes_on_goals = 0

    def clone(self):
        board = super(SokobanBoard, self).clone()
        board._num_boxes = self._num_boxes
        board._num_goals = self._num_goals
        board._num_boxes_on_goals = self._num_boxes_on_goals

        return board

    def restore_state(self):
        result = super(SokobanBoard, self).restore_state()

        if result:
            clone = self._stored_state_clone
            self._num_boxes = clone._num_boxes
            self._num_goals = clone._num_goals
            self._num_boxes_on_goals = clone._num_boxes_on_goals

        return result

    @staticmethod
    # def create_from_str(input_str):
    #     from sokoban.GraphSearch import GraphSearch

    #     lines = list(filter(lambda l: '#' in l, input_str.split('\n')))

    #     height = len(lines)
    #     width = max(*map(lambda l: len(l), lines))
    #     size = width * height

    #     if width < 3 or height < 3:
    #          return 'No valid board'

    #     board = SokobanBoard(width, height)
    #     player_position = None

    #     for (y_index, line) in enumerate(lines):
    #         # Fill the rest part of a line:
    #         if len(line) < width:
    #             line += ' ' * (width - len(line))

    #         for x_index in range(width):
    #             elem_index = board.element_index(x_index, y_index)
    #             symbol = line[x_index]

    #             elem_player_position = SokobanBoard._treat_element_symbol(board, elem_index, symbol)

    #             if elem_player_position is not None:
    #                 player_position = elem_player_position

    #     board.player_position = player_position

    #     if -1 == player_position:
    #         return 'Board does not contain a player!'
        
    #     edge_is_not_reachable = True
    #     def check_if_edge_reached_and_set_active(reached_position):
    #         nonlocal edge_is_not_reachable

    #         board._set_active_cell(reached_position)

    #         if edge_is_not_reachable and board.is_edge(reached_position):
    #             edge_is_not_reachable = False

    #     GraphSearch.BFS(board, player_position, check_if_edge_reached_and_set_active, lambda x: False)

    #     if not edge_is_not_reachable:
    #         return 'Player may walk outside the board'

    #     # Count boxes and goals:
    #     result = board._count_and_update_boxes_and_goals(count_box_on_goal_only=True)
    #     num_boxes = result.get('boxes')
    #     num_goals = result.get('goals')

    #     if num_boxes < 0:
    #         return 'There is no box on the puzzle'

    #     if num_goals < 0:
    #         return 'There is no goal on the puzzle'

    #     if num_boxes != num_goals:
    #         return 'The Number of boxes and goals don\'t match! boxes: {0} but goals: {1}'.format(num_boxes, num_goals)

    #     return board
    
    # @staticmethod
    # def _treat_element_symbol(board, index: int, symbol: str):
    #     player_position = None

    #     if symbol == '#':
    #         board._set_wall(index)

    #     elif symbol == '$':
    #         board._set_box(index)

    #     elif symbol == '*':
    #         board._set_box(index)
    #         board._set_goal(index)

    #     elif symbol == '.':
    #         board._set_goal(index, hard=True)

    #     elif symbol == '@':
    #         board._set_element(index, 8)
    #         player_position = index

    #     elif symbol == '+':
    #         board._set_goal(index, hard=True)
    #         player_position = index

    #     # ' ' or '-' or any else symbol:
    #     else:
    #         board._set_element(index, 16)

    #     return player_position
    
    def _reset_boxes_and_goals(self):
        self._num_boxes = 0
        self._num_goals = 0
        self._num_boxes_on_goals = 0
    
    def _count_and_update_boxes_and_goals(self, count_box_on_goal_only = False):
        num_boxes = 0
        num_goals = 0
        num_boxes_on_goals = 0

        for elem_index in range(self.size):
            if self._is_box_on_goal(elem_index):
                num_boxes_on_goals += 1
                num_boxes += 1
                num_goals += 1

                continue

            if not count_box_on_goal_only:
                continue

            if self._is_box(elem_index):
                num_boxes += 1
                
                continue

            if self.is_goal(elem_index):
                num_goals += 1
                
                continue


        self._num_boxes_on_goals = num_boxes_on_goals
        if count_box_on_goal_only:
            self._num_boxes = num_boxes
            self._num_goals = num_goals

    def _get_goals_positions(self, target_list: list = None):
        if target_list is None:
            target_list = []

        while len(target_list) > 0:
            target_list.pop()

        for index in range(0, self.size, 1):
            if self.is_goal(index):
                target_list.append(index)

        return target_list
        
    def _get_boxes_positions(self: ISokobanBoard, state_stamp: tuple, target_list: list = None):
        elements, _, _, _ = state_stamp

        if target_list is None:
            target_list = []

        while len(target_list) > 0:
            target_list.pop()

        for index in range(0, self.size, 1):
            if self.is_box_element(elements[index]):
                target_list.append(index)
                
        return target_list
    
    # Elements setters
    def _set_element(self, index, value):
        self._elements[index] = value
    
    def _set_wall(self, index):
        self._elements[index] |= 2
    
    def _set_goal(self, index, hard = False):
        if hard:
            self._elements[index] = 4
            return

        self._elements[index] |= 4
    
    def _set_box(self, index):
        self._elements[index] |= 1
    
    def _set_dead_cell(self, index):
        self._elements[index] |= 32
    
    def _set_active_cell(self, index):
        self._elements[index] |= 8
    
    def _set_empty(self, index):
        self._elements[index] = 16
    
    def _clear_box(self, index):
        self._elements[index] ^= 1
    
    # Elements states check
    def _is_goal_element(self, element) -> bool:
        return (element & 4) != 0

    def is_box_element(self, element) -> bool:
        return (element & 1) != 0

    def _is_wall(self, index):
        return (self._elements[index] & 2) != 0
    
    def is_goal(self, index, hard = False): # TODO: hard ???
        return self._is_goal_element(self._elements[index])
    
    def _is_box(self, index):
        return self.is_box_element(self._elements[index])
    
    def _is_box_on_goal(self, index):
        return self._is_box_on_goal_2(self._elements[index])
    
    def _is_box_on_goal_2(self, element):
        mask = 0
        mask |= 1 # box
        mask |= 4 # goal
        return (element & mask) == mask
    
    def _is_box_or_wall(self, index):
        mask = 0
        mask |= 1 # box
        mask |= 2 # wall
        return (self._elements[index] & mask) != 0
    
    def _is_active(self, index):
        return (self._elements[index] & 8) != 0
    
    def _is_dead_cell(self, index):
        return (self._elements[index] & 32) != 0

    # The number of specific cells
    @property
    def num_boxes(self):
        return self._num_boxes
    
    @property
    def num_goals(self):
        return self._num_goals
    
    @property
    def num_boxes_on_goals(self):
        return self._num_boxes_on_goals

    # def get_neighbors(self, element_index) -> list:
    #     # elements = super().get_neighbors(element_index)
    #     # for index in elements:
    #     #     if self._is_wall(index):
    #     #         elements.discard(index)

    #     elements = []

    #     if not self.is_top_edge(element_index) and not self._is_wall(element_index - self._width):
    #         elements.append(element_index - self._width)
    #     if not self.is_right_edge(element_index) and not self._is_wall(element_index + 1):
    #         elements.append(element_index + 1)
    #     if not self.is_bottom_edge(element_index) and not self._is_wall(element_index + self._width):
    #         elements.append(element_index + self._width)
    #     if not self.is_left_edge(element_index) and not self._is_wall(element_index - 1): 
    #         elements.append(element_index - 1)

    #     return elements
    
    def is_solution(self, stamp: tuple) -> bool:
        elements, _, _, _ = stamp
        has_box_out_of_goal = False

        for element in elements:
            if self.is_box_element(element) and not self._is_box_on_goal_2(element):
                has_box_out_of_goal = True
                break

        return not has_box_out_of_goal


    # PLAYING
    def _get_move_delta(self, direction: int):
        if direction == MoveDirection.UP:
            return -self._width
        if direction == MoveDirection.DOWN:
            return self._width
        if direction == MoveDirection.RIGHT:
            return 1
        if direction == MoveDirection.LEFT:
            return -1
        return 0
        
    def can_move(self, direction: int) -> bool:
        delta = self._get_move_delta(direction)
        # print('direction', direction, 'delta', delta)

        if abs(delta) < 1:
            return False

        new_player_position = self.player_position 
        # print(delta, 'to', new_player_position)
        new_player_position += delta

        if not self._is_active(new_player_position):
            return False

        return not (self._is_box(new_player_position) and self._is_box_or_wall(new_player_position + delta))

    # Validate move before calling move
    def move(self, direction: int):
        delta = self._get_move_delta(direction)

        new_player_position = self.player_position 
        new_player_position += delta

        if self._is_box(new_player_position):
            # Move a box
            self._clear_box(new_player_position)
            self._set_box(new_player_position + delta)

        # print('SET', new_player_position)
        self.player_position = new_player_position
        self._move_level += 1
        self._move_id = self._get_next_move_id()

    def get_state_stamp(self):
        return self._elements.copy(), self._player_position, self._move_id, self._move_level
    
    def restore_state_from_stamp(self, state_tuple):
        elements, player_postion, move_id, move_level = state_tuple

        if self._move_id == move_id:
            # print('DO NOT CHANGE BOARD. MOVE ID:', move_id)
            return

        self._player_position = player_postion
        for (index, item) in enumerate(elements):
            self._elements[index] = item

        # Helper
        self._move_id = move_id
        # Statistics
        self._move_level = move_level

    def _get_next_move_id(self):
        self._last_move_id += 1

        return self._last_move_id


