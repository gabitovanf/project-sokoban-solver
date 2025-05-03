from sokoban.board.AbstractBoard import AbstractBoard

class ISokobanBoard(AbstractBoard):
    def __init__(self, width, height, fill_with=0):
        super().__init__(width, height, fill_with)

    def can_move(self, direction: int) -> bool:
        pass

    def move(self, direction: int):
        pass

    def is_solution(self, stamp: tuple) -> bool:
        pass

    def _set_empty(self, index):
        pass

    def _set_wall(self, index):
        pass
    
    def _set_goal(self, index, hard = False):
        pass
    
    def _set_box(self, index):
        pass
    
    def _set_dead_cell(self, index):
        pass
    
    def _set_active_cell(self, index):
        pass
    
    # def _clear_box(self, index):
    #     pass
    
    # Elements states check
    def _is_goal_element(self, element) -> bool:
        pass

    def is_box_element(self, element) -> bool:
        pass

    def _is_wall(self, index):
        pass
    
    def is_goal(self, index): # TODO: hard = False hard ???
        pass
    
    def _is_box(self, index):
        pass
    
    def _is_box_on_goal(self, index):
        pass
    
    def _is_box_on_goal_2(self, element):
        pass
    
    def _is_box_or_wall(self, index):
        pass
    
    def _is_active(self, index):
        pass
    
    def _is_dead_cell(self, index):
        pass

    # The number of specific cells
    @property
    def num_boxes(self):
        pass
    
    @property
    def num_goals(self):
        pass
    
    @property
    def num_boxes_on_goals(self):
        pass
    
    def _get_goals_positions(self, target_list: list = None):
        pass
    
    def _get_boxes_positions(self, state_stamp: tuple, target_list: list = None):
        pass
    
    def _get_boxes_not_on_goals_positions(self, state_stamp: tuple, target_list: list = None):
        pass
    
    def _count_and_update_boxes_and_goals(self) -> dict:
        pass

    def get_state_stamp(self) -> tuple:
        pass

    def state_stamp_equal(self) -> bool:
        pass

    def restore_state_from_stamp(self, stamp: tuple):
        pass

    def get_neighbors(self, element_index) -> list:
        # elements = super().get_neighbors(element_index)
        # for index in elements:
        #     if self._is_wall(index):
        #         elements.discard(index)

        elements = []

        if not self.is_top_edge(element_index) and not self._is_wall(element_index - self._width):
            elements.append(element_index - self._width)
        if not self.is_right_edge(element_index) and not self._is_wall(element_index + 1):
            elements.append(element_index + 1)
        if not self.is_bottom_edge(element_index) and not self._is_wall(element_index + self._width):
            elements.append(element_index + self._width)
        if not self.is_left_edge(element_index) and not self._is_wall(element_index - 1): 
            elements.append(element_index - 1)

        return elements
