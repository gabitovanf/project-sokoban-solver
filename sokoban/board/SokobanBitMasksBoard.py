from sokoban.board.ISokobanBoard import ISokobanBoard
from utility_algorithms.BitCount import BitCount
from sokoban.board.MoveDirection import MoveDirection


class SokobanBitMasksBoard(ISokobanBoard):
    def __init__(self, width, height):
        super().__init__(width, height, 0)

        size = self._size
        empty = 1 << (size + 1)
        self._mask_normalize = ~empty
        self._mask_walls = empty
        self._mask_active = empty  # Inside walls
        self._mask_box = empty
        self._mask_goal = empty

        self._move_level = 0
        self._move_id = 0
        self._last_move_id = 0

        self._num_boxes = 0
        self._num_goals = 0
        self._num_boxes_on_goals = 0

    # SETTERS
    def _set_empty(self, index):
        pass

    def _set_wall(self, index):
        # new_wall: 1 << index
        self._mask_walls = self._mask_walls | 1 << index
    
    def _set_goal(self, index, hard = False):
        self._mask_goal = self._mask_goal | 1 << index
    
    def _set_box(self, index):
        self._mask_box = self._mask_box | 1 << index
    
    def _set_dead_cell(self, index):
        pass
    
    def _set_active_cell(self, index):
        self._mask_active = self._mask_active | 1 << index
    
    def _clear_box(self, index):
        pass

    def _count_and_update_boxes_and_goals(self, count_box_on_goal_only = False):
        stamp_masks = (self._mask_box, self._mask_goal, self._mask_active)
        self._num_boxes_on_goals = SokobanBitMasksBoard._get_num_boxes_on_goals(stamp_masks)
        if count_box_on_goal_only:
            self._num_boxes = SokobanBitMasksBoard._get_num_boxes(stamp_masks)
            self._num_goals = BitCount.popcount(self._mask_goal)

    @staticmethod
    def _get_num_boxes_on_goals(stamp_masks: tuple):
        mask_box, mask_goal, _ = stamp_masks

        return BitCount.popcount(mask_box & mask_goal)

    @staticmethod
    def _get_num_boxes(stamp_masks: tuple):
        mask_box, _, _ = stamp_masks

        return BitCount.popcount(mask_box)
    
    def _get_goals_positions(self, target_list: list = None):
        if target_list is None:
            target_list = []

        while len(target_list) > 0:
            target_list.pop()

        return BitCount.get_positions(self._normalize_mask(self._mask_goal), mode=1, target_list=target_list)
        
    def _get_boxes_positions(self, state_stamp: tuple, target_list: list = None):
        if target_list is None:
            target_list = []

        while len(target_list) > 0:
            target_list.pop()

        masks, _, _, _ = state_stamp
        mask_box, _, _ = masks

        return BitCount.get_positions(self._normalize_mask(mask_box), mode=1, target_list=target_list)
        
    def _get_boxes_not_on_goals_positions(self, state_stamp: tuple, target_list: list = None):
        if target_list is None:
            target_list = []

        while len(target_list) > 0:
            target_list.pop()

        masks, _, _, _ = state_stamp
        mask_box, _, _ = masks

        mask_box = self._mask_box & (~self._mask_goal)

        return BitCount.get_positions(self._normalize_mask(mask_box), mode=1, target_list=target_list)

    # GETTERS
    # Elements states check
    def is_solution(self, stamp: tuple) -> bool:
        masks, _, _, _ = stamp
        mask_box, mask_goal, _ = masks

        mask_not_solved_boxes_and_goals = mask_box ^ mask_goal
        mask_not_solved_boxes_and_goals = self._normalize_mask(mask_not_solved_boxes_and_goals)

        return mask_not_solved_boxes_and_goals == 0

    def is_goal(self, index) -> bool:
        return self._mask_goal & 1 << index

    def is_box_element(self, element) -> bool:
        pass

    def _is_goal_element(self, element) -> bool:
        pass

    def _is_wall(self, index):
        return self._mask_walls & 1 << index
    
    def _is_box(self, index):
        return self._mask_box & 1 << index
    
    def _is_box_on_goal(self, index):
        intersection_mask = self._mask_box & self._mask_goal
        return intersection_mask & 1 << index
        # return self._is_box(index) and self.is_goal(index)
    
    # def _is_box_on_goal_2(self, element):
    #     pass
    
    def _is_box_or_wall(self, index):
        union_mask = self._mask_box | self._mask_walls
        return union_mask & 1 << index
    
    def _is_active(self, index):
        return self._mask_active & 1 << index
    
    def _is_dead_cell(self, index):
        pass

    def _normalize_mask(self, mask):
        return mask & self._mask_normalize

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

    # MOVES:
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

    def _get_moved_mask(self, mask, direction: int):
        if direction == MoveDirection.UP:
            return mask >> self._width
        if direction == MoveDirection.DOWN:
            return self._normalize_mask(mask << self._width)
        if direction == MoveDirection.RIGHT:
            return self._normalize_mask(mask << 1)
        if direction == MoveDirection.LEFT:
            return mask >> 1
        return mask
        
    def can_move(self, direction: int) -> bool:
        delta = self._get_move_delta(direction)

        if abs(delta) < 1:
            return False

        new_player_position = self.player_position 
        new_player_position += delta

        valid_moves_mask = self._mask_box | self._mask_walls  # box or wall
        # Stop if walls or boxes moved to the oppsit direction overlap some box at new player position
        # Otherwise approve a move
        valid_moves_mask = self._mask_active & (~(self._get_moved_mask(valid_moves_mask, MoveDirection.reversed(direction)) & self._mask_box))

        return valid_moves_mask & 1 << new_player_position

    def move(self, direction: int):
        delta = self._get_move_delta(direction)

        new_player_position = self.player_position 
        new_player_position += delta

        if self._is_box(new_player_position):
            # Swap box position
            swap_mask = 1 << new_player_position | 1 << (new_player_position + delta)
            self._mask_box = swap_mask ^ self._mask_box

        # print('SET', new_player_position)
        self.player_position = new_player_position
        self._move_level += 1
        self._move_id = self._get_next_move_id()

    # STATE STAMPS:
    def get_state_stamp(self):
        return (self._mask_box, self._mask_goal, self._mask_active), self._player_position, self._move_id, self._move_level
    
    def state_stamp_equal(self, stamp_a, stamp_b) -> bool:
        masks_a, player_postion_a, _, _ = stamp_a
        masks_b, player_postion_b, _, _ = stamp_b

        return masks_a == masks_b and player_postion_a == player_postion_b
    
    def restore_state_from_stamp(self, state_tuple):
        masks, player_postion, move_id, move_level = state_tuple
        mask_box, mask_goal, _ = masks

        # No need to check because the restore operation is O(1)
        # if self._move_id == move_id:
        #     # print('DO NOT CHANGE BOARD. MOVE ID:', move_id)
        #     return

        self._player_position = player_postion
        self._mask_box = mask_box
        self._mask_goal = mask_goal

        # TODO: Do we need move_id?
        # Helper
        self._move_id = move_id
        # Statistics
        self._move_level = move_level

    def _get_next_move_id(self):
        self._last_move_id += 1

        return self._last_move_id
    
    def _copy_state_from_to(self, from_board, to_board):
        to_board.player_position = from_board.player_position

        to_board._mask_normalize = from_board._mask_normalize
        to_board._mask_walls = from_board._mask_walls
        to_board._mask_active = from_board._mask_active
        to_board._mask_box = from_board._mask_box
        to_board._mask_goal = from_board._mask_goal

        to_board._move_level = from_board._move_level
        to_board._move_id = from_board._move_id
        to_board._last_move_id = from_board._last_move_id

        to_board._num_boxes = from_board._num_boxes
        to_board._num_goals = from_board._num_goals
        to_board._num_boxes_on_goals = from_board._num_boxes_on_goals