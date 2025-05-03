from sokoban.board.ISokobanBoard import ISokobanBoard
from sokoban.board.AbstractBoard import AbstractBoard


def _treat_element_symbol(board: ISokobanBoard, index: int, symbol: str):
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
            # board._set_element(index, 8)
            board._set_active_cell(index)
            player_position = index

        elif symbol == '+':
            board._set_goal(index, hard=True)
            player_position = index

        # ' ' or '-' or any else symbol:
        else:
            board._set_empty(index)

        return player_position

def create_from_str(input_str, constructor) -> ISokobanBoard:
    from sokoban.GraphSearch import GraphSearch

    lines = list(filter(lambda l: '#' in l, input_str.split('\n')))

    height = len(lines)
    width = max(*map(lambda l: len(l), lines))
    size = width * height

    if width < 3 or height < 3:
            return 'No valid board'

    board = constructor(width, height)
    player_position = None

    for (y_index, line) in enumerate(lines):
        # Fill the rest part of a line:
        if len(line) < width:
            line += ' ' * (width - len(line))

        for x_index in range(width):
            elem_index = board.element_index(x_index, y_index)
            symbol = line[x_index]

            elem_player_position = _treat_element_symbol(board, elem_index, symbol)

            if elem_player_position is not None:
                player_position = elem_player_position

    board.player_position = player_position

    if -1 == player_position:
        return 'Board does not contain a player!'
    
    edge_is_not_reachable = True
    def check_if_edge_reached_and_set_active(reached_position):
        nonlocal edge_is_not_reachable

        board._set_active_cell(reached_position)

        if edge_is_not_reachable and board.is_edge(reached_position):
            edge_is_not_reachable = False

    # TODO: COMPLETE CHECKS
    GraphSearch.BFS(board, player_position, check_if_edge_reached_and_set_active, lambda x: False)

    if not edge_is_not_reachable:
        return 'Player may walk outside the board'

    # Count boxes and goals:
    board._count_and_update_boxes_and_goals(count_box_on_goal_only=True)
    num_boxes = board.num_boxes
    num_goals = board.num_goals

    if num_boxes < 0:
        return 'There is no box on the puzzle'

    if num_goals < 0:
        return 'There is no goal on the puzzle'

    if num_boxes != num_goals:
        return 'The Number of boxes and goals don\'t match! boxes: {0} but goals: {1}'.format(num_boxes, num_goals)

    return board

def create_from_json_encoded(input_str: str, constructor) -> ISokobanBoard:
    decoded_json_dict = AbstractBoard.parse_json_encoded(input_str)

    board = create_from_str('\n'.join(decoded_json_dict.get('Board', [])), constructor)

    board.title = decoded_json_dict.get('Level Title', 'No Name')
    board.level = decoded_json_dict.get('Level No.', 0)
    board.level_set = decoded_json_dict.get('Level Set', 'No Name')

    return board