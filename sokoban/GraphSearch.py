from structure.queue.Queue import Queue
from structure.Stack import Stack
from sokoban.ISearchGraph import ISearchGraph


class GraphSearch:
    def __init__(self):
        pass
    
    @staticmethod
    def BFS(graph_instance: ISearchGraph, start_state, apply_to_reached, search_condition):
        if search_condition(start_state):
            return start_state

        frontier = Queue()
        reached = set()
        frontier.enqueue(start_state)
        reached.add(start_state)

        while not frontier.is_empty:
            current_state = frontier.dequeue()
            for next in graph_instance.get_neighbors(current_state):
                if next not in reached:
                    # validate solution
                    if search_condition(next):
                        return next

                    frontier.enqueue(next)
                    reached.add(next)
                    apply_to_reached(next)

        return None
    
    @staticmethod
    def DFS(graph_instance: ISearchGraph, start_state, apply_to_reached, search_condition, max_level: int = 1 << 50, search_minimum: bool = False):
        if search_condition(start_state):
            return start_state
        
        frontier = Stack()
        frontier_level = Stack()
        reached = set()
        frontier.push(start_state)
        frontier_level.push(0)
        reached.add(start_state)

        minimum_solution = None
        minimum_level = max_level + 1

        while not frontier.is_empty:
            current_state = frontier.pop()
            current_level = frontier_level.pop()

            if current_level >= max_level:
                continue

            for next in graph_instance.get_neighbors(current_state):
                if next not in reached:
                    # validate solution
                    if search_condition(next):
                        if search_minimum: 
                            if current_level + 1 < minimum_level:
                                minimum_solution = next
                                minimum_level = current_level + 1
                        else:
                            return next

                    frontier.push(next)
                    frontier_level.push(current_level + 1)
                    reached.add(next)
                    apply_to_reached(next)

        return minimum_solution

