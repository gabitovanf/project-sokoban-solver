from structure.queue.Queue import Queue
from sokoban.solver.BoardStateNode import BoardStateNode


class BoardStateAndPathNode(BoardStateNode):
    def __init__(self, parent_node, state_stamp, action, level: int = 0, path_cost: int = 0, total_cost: int = 0):
        super().__init__(state_stamp, action, level, path_cost, total_cost)

        path_actions = []
        path_state_stamps = []

        if parent_node is not None:
            for i in range(0, len(parent_node.path_actions), 1):
                path_actions.append(parent_node.path_actions[i])
                path_state_stamps.append(parent_node.path_state_stamps[i])

        path_actions.append(action)
        path_state_stamps.append(state_stamp)

        self._path_actions = path_actions
        self._path_state_stamps = path_state_stamps

    @property
    def path_state_stamps(self):
        return self._path_state_stamps

    @property
    def path_actions(self):
        return self._path_actions

    @property
    def has_path_records(self):
        return True
    
