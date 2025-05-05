import math
from structure.matrix.ListMatrix import ListMatrix
from utility_algorithms.AssignmentProblem import AssignmentProblem
from sokoban.board.ISokobanBoard import ISokobanBoard
from sokoban.solver.BoardStateNode import BoardStateNode


class BoxesToGoalsManhattan:
    def __init__(self, board: ISokobanBoard):
        self._board = board
        self._goals_positions = []
        self._boxes_positions = []

    def combine(self, heuristic_list: list):
        def sum_combination(state_node) -> int:
            positions = self._get_positions(state_node)
            sum = 0

            for i in range(0, len(heuristic_list), 1):
                sum += heuristic_list[i](state_node, positions_updated=positions)

            return sum

        return sum_combination


    def simple_manhattan_heuristic(self, state_node, positions_updated=None) -> int:
        goals_positions, boxes_positions = self._get_positions(state_node) if positions_updated is None else positions_updated

        return BoxesToGoalsManhattan._get_simple_manhattan(self._board, boxes_positions, goals_positions)


    def min_manhattan_heuristic(self, state_node, positions_updated=None) -> int:
        goals_positions, boxes_positions = self._get_positions(state_node) if positions_updated is None else positions_updated

        return BoxesToGoalsManhattan._get_minimum_manhattan(self._board, boxes_positions, goals_positions)


    def mid_player_to_boxes_manhattan_heuristic(self, state_node, positions_updated=None) -> int:
        _, player_position, _, _ = state_node.state_stamp
        _, boxes_positions = self._get_positions(state_node) if positions_updated is None else positions_updated

        return BoxesToGoalsManhattan._get_mid_to_position(self._board, boxes_positions, player_position)


    def mid_player_to_free_boxes_manhattan_heuristic(self, state_node, positions_updated=None) -> int:
        _, player_position, _, _ = state_node.state_stamp
        
        boxes_positions = self._board._get_boxes_not_on_goals_positions(state_node.state_stamp)

        return BoxesToGoalsManhattan._get_mid_to_position(self._board, boxes_positions, player_position)
    
    
    def min_manhattan_include_player_heuristic(self, state_node, positions_updated=None) -> int:
        goals_positions, boxes_positions = self._get_positions(state_node) if positions_updated is None else positions_updated
        _, player_position, _, _ = state_node.state_stamp
        player_x = self._board.element_x(player_position)
        player_y = self._board.element_y(player_position)

        min_combination_list = BoxesToGoalsManhattan._get_minimum_manhattan_combination(self._board, boxes_positions, goals_positions)

        boxes_positions = self._board._get_boxes_not_on_goals_positions(state_node.state_stamp)
        
        sum = 0
        min_to_player = self._board.size
        exclude_min_to_goal = 0
        for i in range(0, len(min_combination_list), 1):
            # Starts from min manhattan for boxes and goals
            # Add player to closest free box 
            # and Add the rest min manhattan for boxes and goals (add twice and substract closest)
            
            sum += min_combination_list[i][2]

            if min_combination_list[i][2] == 0:
                continue

            x = self._board.element_x(min_combination_list[i][0])
            y = self._board.element_y(min_combination_list[i][0])

            manhattan = abs(x - player_x) + abs(y - player_y)
            if manhattan < min_to_player:
                min_to_player = manhattan
                exclude_min_to_goal = min_combination_list[i][2]

        if sum == 0:
            return sum

        sum += sum - exclude_min_to_goal
        sum += min_to_player

        return sum


    def _get_positions(self, state_node) -> tuple:
        if len(self._goals_positions) < 1:
            self._goals_positions = self._board._get_goals_positions(self._goals_positions)

        if len(self._goals_positions) < 1:
            return 0

        self._boxes_positions = self._board._get_boxes_positions(state_node.state_stamp, self._boxes_positions)

        return self._goals_positions, self._boxes_positions


    @staticmethod
    def _get_simple_manhattan(board: ISokobanBoard, from_positions: list, to_positions: list) -> int:
        sum = 0
        for i in range(0, len(from_positions), 1):
            p_i = from_positions[i]
            min_manhattan = board.size
            for j in range(0, len(to_positions), 1):
                p_j = to_positions[j]
                manhattan = abs(board.element_x(p_j) - board.element_x(p_i)) + abs(board.element_y(p_j) - board.element_y(p_i))
                if manhattan < min_manhattan:
                    min_manhattan = manhattan
            sum += min_manhattan

        return sum


    @staticmethod
    def _get_minimum_manhattan(board: ISokobanBoard, from_positions: list, to_positions: list) -> int:
        sum = 0

        # Fill Matrix
        mx = ListMatrix(len(from_positions), len(to_positions))
        for i in range(0, len(from_positions), 1):
            p_i = from_positions[i]
            for j in range(0, len(to_positions), 1):
                p_j = to_positions[j]
                manhattan = abs(board.element_x(p_j) - board.element_x(p_i)) + abs(board.element_y(p_j) - board.element_y(p_i))
                mx.set(i, j, manhattan)

        # print(mx)
        # Find minimum sun
        result_list = AssignmentProblem.HungarianAlgorithm(mx)
        # print(result_list)

        sum = 0
        for i in range(0, len(result_list), 1):
            sum += result_list[i][2]

        return sum

    @staticmethod
    def _get_minimum_manhattan_combination(board: ISokobanBoard, from_positions: list, to_positions: list) -> int:
        # Fill Matrix
        mx = ListMatrix(len(from_positions), len(to_positions))
        for i in range(0, len(from_positions), 1):
            p_i = from_positions[i]
            for j in range(0, len(to_positions), 1):
                p_j = to_positions[j]
                manhattan = abs(board.element_x(p_j) - board.element_x(p_i)) + abs(board.element_y(p_j) - board.element_y(p_i))
                mx.set(i, j, manhattan)

        # print(mx)
        # Find minimum sun
        result_list = AssignmentProblem.HungarianAlgorithm(mx)
        # print(result_list)

        return result_list


    @staticmethod
    def _get_minimum_manhattan(board: ISokobanBoard, from_positions: list, to_positions: list) -> int:
        sum = 0

        # Find minimum sun
        result_list = BoxesToGoalsManhattan._get_minimum_manhattan_combination(board, from_positions, to_positions)
        # print(result_list)

        sum = 0
        for i in range(0, len(result_list), 1):
            sum += result_list[i][2]

        return sum
    

    @staticmethod
    def _get_mid_to_position(board: ISokobanBoard, from_positions: list, to_position: int) -> int:
        if len(from_positions) < 1: return 0
        
        sum = 0
        
        for i in range(0, len(from_positions), 1):
            p_i = from_positions[i]
            p_j = to_position
            sum += abs(board.element_x(p_j) - board.element_x(p_i)) + abs(board.element_y(p_j) - board.element_y(p_i))
            
        return int(math.ceil(sum / len(from_positions)))

    @staticmethod
    def _update_goals_positions(board: ISokobanBoard, target_list: list):
        return board._get_goals_positions(target_list)
        

    @staticmethod
    def _update_boxes_positions(board: ISokobanBoard, state_node: BoardStateNode, target_list: list):
        return board._get_boxes_positions(state_node.state_stamp, target_list)

