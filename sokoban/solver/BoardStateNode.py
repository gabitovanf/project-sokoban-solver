class BoardStateNode:
    def __init__(self, state_stamp, action, level: int = 0, path_cost: int = 0, total_cost: int = 0):
        self._state_stamp = state_stamp
        self._level = level
        self._action = action
        self._path_cost = path_cost
        self._total_cost = total_cost
        self._parent_node = None

        self._children = []

    def append(self, node):
        node.parent_node = self
        self._children.append(node)

    @property
    def state_stamp(self):
        return self._state_stamp

    @property
    def level(self):
        return self._level

    @property
    def action(self):
        return self._action

    @property
    def children(self):
        return self._children

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, node):
        self._parent_node = node

    @property
    def path_cost(self):
        return self._path_cost

    @path_cost.setter
    def path_cost(self, value):
        self._path_cost = value

    @property
    def total_cost(self):
        return self._total_cost

    @total_cost.setter
    def total_cost(self, value):
        self._total_cost = value

    @property
    def has_path_records(self):
        return False


    
     
