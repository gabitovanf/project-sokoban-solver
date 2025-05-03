import time

from structure.queue.Queue import Queue
from structure.Stack import Stack
from structure.PriorityInsertStack import PriorityInsertStack
from sokoban.ISearchGraph import ISearchGraph
from sokoban.solver.array_board_heuristic.BoxesToGoalsManhattan import BoxesToGoalsManhattan


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
                        print('NUM REACHED', len(reached), '\n\n')
                        return next

                    frontier.enqueue(next)
                    reached.add(next)
                    apply_to_reached(next)
                    print('NUM REACHED', len(reached), end='\r', flush=True)

        print('NUM REACHED', len(reached), '\n\n')
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
                            print('NUM REACHED', len(reached), '\n\n')
                            return next

                    frontier.push(next)
                    frontier_level.push(current_level + 1)
                    reached.add(next)
                    apply_to_reached(next)
                    print('NUM REACHED', len(reached), end='\r', flush=True)

        print('NUM REACHED', len(reached), '\n\n')
        return minimum_solution

    
    @staticmethod
    def A_star(
        graph_instance: ISearchGraph,
        start_state, 
        apply_to_reached,
        search_condition, 
        max_level: int = 1 << 50,
        heuristic = None
    ):
        # start_time = time.time()
        # ref_num_reached_time = 0
        # ref_num_reached = 100000

        if not callable(heuristic):
            heuristic = BoxesToGoalsManhattan.min_manhattan_heuristic
        if search_condition(start_state):
            return start_state
        
        start_state.total_cost = start_state.path_cost + heuristic(start_state)

        frontier = PriorityInsertStack()
        reached = set()
        frontier.put(start_state.total_cost, (start_state, 0))
        reached.add(start_state)

        while not frontier.is_empty:
            current_state, current_level = frontier.pop()

            if current_level >= max_level:
                continue

            for next in graph_instance.get_neighbors(current_state):
                # validate solution
                if search_condition(next):
                    print(
                        'NUM REACHED', len(reached), 
                        # '\nREF {num} REACHED AT {time}'.format(num=ref_num_reached, time=ref_num_reached_time),
                        '\n\n'
                    )
                    return next
            
                previous_total_cost = next.total_cost
                next.total_cost = next.path_cost + heuristic(next)
                # Uncomment to check a factor of total cost
                print('TOTAL COST', next.total_cost, next.path_cost, heuristic(next))

                if next not in reached:
                    frontier.put(next.total_cost, (next, current_level + 1))
                    reached.add(next)
                    apply_to_reached(next)

                    # if len(reached) == ref_num_reached:
                    #     ref_num_reached_time = time.time() - start_time

                    print(
                        'NUM REACHED', len(reached), 
                        # '\nREF {num} REACHED AT {time}'.format(num=ref_num_reached, time=ref_num_reached_time), 
                        end='\n', 
                        flush=True
                    )
                    
                elif previous_total_cost > next.total_cost:
                    frontier.replace_item(previous_total_cost, next.total_cost, next)



        print(
            'NUM REACHED', len(reached), 
            # '\nREF {num} REACHED AT {time}'.format(num=ref_num_reached, time=ref_num_reached_time),
            '\n\n'
        )
        return None

