from structure.matrix.ListMatrix import ListMatrix
from utility_algorithms.AssignmentProblem import AssignmentProblem
from sokoban.board.ISokobanBoard import ISokobanBoard
from sokoban.solver.BoardStateNode import BoardStateNode


class BoxesToGoalsManhattan:
    def __init__(self, board: ISokobanBoard):
        self._board = board
        self._goals_positions = []
        self._boxes_positions = []


    def simple_manhattan_heuristic(self, state_node) -> int:
        elements, _, _, _ = state_node.state_stamp
        goals_positions, boxes_positions = self._get_positions(elements)

        return BoxesToGoalsManhattan._get_simple_manhattan(self._board, boxes_positions, goals_positions)


    def min_manhattan_heuristic(self, state_node) -> int:
        elements, _, _, _ = state_node.state_stamp
        goals_positions, boxes_positions = self._get_positions(elements)

        return BoxesToGoalsManhattan._get_minimum_manhattan(self._board, boxes_positions, goals_positions)


    def _get_positions(self, elements) -> tuple:
        if len(self._goals_positions) < 1:
            BoxesToGoalsManhattan._update_goals_positions(self._board, self._goals_positions)

        if len(self._goals_positions) < 1:
            return 0

        boxes_positions = self._boxes_positions
        while len(boxes_positions) > 0:
            boxes_positions.pop()

        BoxesToGoalsManhattan._update_boxes_positions(self._board, elements, boxes_positions)

        return self._goals_positions, boxes_positions


    @staticmethod
    def _get_simple_manhattan(board: ISokobanBoard, from_positions: list, to_positions: list) -> list:
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
    def _get_minimum_manhattan(board: ISokobanBoard, from_positions: list, to_positions: list) -> list:
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
    def _update_goals_positions(board: ISokobanBoard, target_list: list):
        while len(target_list) > 0:
            target_list.pop()

        for index in range(0, board.size, 1):
            if board.is_goal(index):
                target_list.append(index)
        

    @staticmethod
    def _update_boxes_positions(board: ISokobanBoard, elements: list, target_list: list):
        while len(target_list) > 0:
            target_list.pop()

        for index in range(0, board.size, 1):
            if board.is_box_element(elements[index]):
                target_list.append(index)

