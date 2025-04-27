from sokoban.AbstractBoard import AbstractBoard


class SokobanBoard(AbstractBoard):
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
    def create_from_str(input_str):
        from sokoban.SokobanSolver import SokobanSolver

        lines = list(filter(lambda l: '#' in l, input_str.split('\n')))

        height = len(lines)
        width = max(*map(lambda l: len(l), lines))
        size = width * height

        if width < 3 or height < 3:
             return 'No valid board'

        board = SokobanBoard(width, height)
        player_position = None

        for (y_index, line) in enumerate(lines):
            # Fill the rest part of a line:
            if len(line) < width:
                line += ' ' * (width - len(line))

            for x_index in range(width):
                elem_index = board.element_index(x_index, y_index);
                symbol = line[x_index]

                elem_player_position = SokobanBoard._treat_element_symbol(board, elem_index, symbol)

                if elem_player_position is not None:
                    player_position = elem_player_position

        board.player_position = player_position

        if -1 == player_position:
            return 'Board does not contain a player!'
        
        # TODO: check available cells (active) first

        searcher = SokobanSolver(board)
        searcher.bfs(player_position, lambda reached_position: board._set_active_cell(reached_position))

        # Count boxes and goals:
        board._count_boxes_and_goals(update_all=True)

        if board.num_boxes < 0:
            return 'There is no box on the puzzle'

        if board.num_goals < 0:
            return 'There is no goal on the puzzle'

        if board.num_boxes != board.num_goals:
            return 'The Number of boxes and goals don\'t match! boxes: {0} but goals: {1}'.format(board.num_boxes, board.num_goals)

        return board

    @staticmethod
    def create_from_json_encoded(input_str: str):
        decoded_json_dict = AbstractBoard.parse_json_encoded(input_str)

        board = SokobanBoard.create_from_str('\n'.join(decoded_json_dict.get('Board', [])))

        board.title = decoded_json_dict.get('Level Title', 'No Name')
        board.level = decoded_json_dict.get('Level No.', 0)
        board.level_set = decoded_json_dict.get('Level Set', 'No Name')

        return board
    
    @staticmethod
    def _treat_element_symbol(board, index: int, symbol: str):
        player_position = None

        if symbol == '#':
            board._set_wall(index)

        elif symbol == '$':
            board._set_box(index)

        elif symbol == '*':
            board._set_box(index)
            board._set_goal(index)

        elif symbol == '.':
            board._set_goal(index, hard=True)

        elif symbol == '@':
            board._set_element(index, 8)
            player_position = index

        elif symbol == '+':
            board._set_goal(index, hard=True)
            player_position = index

        # ' ' or '-' or any else symbol:
        else:
            board._set_element(index, 16)

        return player_position
    
    def _reset_boxes_and_goals(self):
        self._num_boxes = 0
        self._num_goals = 0
        self._num_boxes_on_goals = 0
    
    def _count_boxes_and_goals(self, update_all = False):
        num_boxes = 0
        num_goals = 0
        num_boxes_on_goals = 0

        # TODO: check if cell is available
        for elem_index in range(self.size):
            if self._is_box_on_goal(elem_index):
                num_boxes_on_goals += 1
                num_boxes += 1
                num_goals += 1

                continue

            if not update_all:
                continue

            if self._is_box(elem_index):
                num_boxes += 1
                
                continue

            if self._is_goal(elem_index):
                num_goals += 1
                
                continue


        self._num_boxes_on_goals = num_boxes_on_goals
        if update_all:
            self._num_boxes = num_boxes
            self._num_goals = num_goals

    
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
    
    # Elements states check
    def _is_wall(self, index):
        return (self._elements[index] & 2) != 0
    
    def _is_goal(self, index, hard = False):
        return (self._elements[index] & 4) != 0
    
    def _is_box(self, index):
        return (self._elements[index] & 1) != 0
    
    def _is_box_on_goal(self, index):
        mask = 0
        mask |= 1 # box
        mask |= 4 # goal
        return (self._elements[index] & mask) == mask
    
    def _is_box_or_wall(self, index):
        mask = 0
        mask |= 1 # box
        mask |= 2 # wall
        return (self._elements[index] & mask) != 0
    
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
    
    def get_neighbors(self, element_index):
        # elements = super().get_neighbors(element_index)
        # for index in elements:
        #     if self._is_wall(index):
        #         elements.discard(index)

        elements = set()

        if not self.is_top_edge(element_index) and not self._is_wall(element_index + self._width):
            elements.add(element_index + self._width)
        if not self.is_right_edge(element_index) and not self._is_wall(element_index + 1):
            elements.add(element_index + 1)
        if not self.is_bottom_edge(element_index) and not self._is_wall(element_index - self._width):
            elements.add(element_index - self._width)
        if not self.is_left_edge(element_index) and not self._is_wall(element_index - 1): 
            elements.add(element_index - 1)

        return elements

        return elements
    
