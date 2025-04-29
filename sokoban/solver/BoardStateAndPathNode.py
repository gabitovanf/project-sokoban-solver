from structure.queue.Queue import Queue
from sokoban.solver.BoardStateNode import BoardStateNode


class BoardStateAndPathNode(BoardStateNode):
    def __init__(self, parent_node, state_stamp, action, level: int = 0):
        super().__init__(state_stamp, action, level)

        path_actions_queue = Queue() if parent_node.path_actions_queue is None else parent_node.path_actions_queue
        path_state_stamps_queue = Queue() if parent_node.path_state_stamps_queue is None else parent_node.path_state_stamps_queue

        path_actions_queue.enqueue(action)
        path_state_stamps_queue.enqueue(state_stamp)

        self._path_actions_queue = path_actions_queue
        self._path_state_stamps_queue = path_state_stamps_queue

    @property
    def path_state_stamps_queue(self):
        return self._path_state_stamps_queue

    @property
    def path_actions_queue(self):
        return self._path_actions_queue

    @property
    def has_path_queues(self):
        return True
    
