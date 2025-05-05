import time
import sys

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
            return start_state, { 'num_reached': 0 }

        frontier = Queue()
        reached = set()
        frontier.enqueue(start_state)
        reached.add(start_state)

        def get_metrics() -> dict:
            return { 'num_reached': len(reached) }

        while not frontier.is_empty:
            current_state = frontier.dequeue()
            for next in graph_instance.get_neighbors(current_state):
                if next not in reached:
                    # validate solution
                    if search_condition(next):
                        print('NUM REACHED', len(reached), '\n\n')
                        return next, get_metrics()

                    frontier.enqueue(next)
                    reached.add(next)
                    apply_to_reached(next)
                    print('NUM REACHED', len(reached), end='\r', flush=True)

        print('NUM REACHED', len(reached), '\n\n')
        return None, get_metrics()
    
    @staticmethod
    def DFS(graph_instance: ISearchGraph, start_state, apply_to_reached, search_condition, depth_limit: int = sys.maxsize, search_minimum: bool = False):
        if search_condition(start_state):
            return start_state, { 'num_reached': 0 }
        
        frontier = Stack()
        frontier_level = Stack()
        reached = set()
        frontier.push(start_state)
        frontier_level.push(0)
        reached.add(start_state)

        minimum_solution = None
        minimum_level = depth_limit + 1

        def get_metrics() -> dict:
            return { 'num_reached': len(reached) }

        while not frontier.is_empty:
            current_state = frontier.pop()
            current_level = frontier_level.pop()

            if current_level >= depth_limit:
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
                            return next, get_metrics()

                    frontier.push(next)
                    frontier_level.push(current_level + 1)
                    reached.add(next)
                    apply_to_reached(next)
                    print('NUM REACHED', len(reached), end='\r', flush=True)

        print('NUM REACHED', len(reached), '\n\n')
        return minimum_solution, get_metrics()

    
    @staticmethod
    def A_star(
        graph_instance: ISearchGraph,
        start_state, 
        apply_to_reached,
        search_condition, 
        depth_limit: int = sys.maxsize,
        heuristic = None
    ):
        # start_time = time.time()
        # ref_num_reached_time = 0
        # ref_num_reached = 100000

        if not callable(heuristic):
            heuristic = BoxesToGoalsManhattan.min_manhattan_heuristic
        if search_condition(start_state):
            return start_state, { 'num_reached': 0 }
        
        start_state.total_cost = start_state.path_cost + heuristic(start_state)

        frontier = PriorityInsertStack()
        reached = set()
        frontier.put(start_state.total_cost, (start_state, 0))
        reached.add(start_state)

        def get_metrics() -> dict:
            return { 'num_reached': len(reached) }

        while not frontier.is_empty:
            current_state, current_level = frontier.pop()

            # validate solution
            if search_condition(current_state):
                print(
                    'NUM REACHED', len(reached), 
                    # '\nREF {num} REACHED AT {time}'.format(num=ref_num_reached, time=ref_num_reached_time),
                    '\n\n'
                )
                return current_state, get_metrics()

            if current_level >= depth_limit:
                continue

            for next in graph_instance.get_neighbors(current_state):
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
        return None, get_metrics()

    
    @staticmethod
    def IDA_star(
        graph_instance: ISearchGraph,
        start_state, 
        apply_to_reached,
        search_condition, 
        start_depth_limit: int = 15, 
        increment_depth_limit: int = 10, 
        max_depth_limit: int = sys.maxsize, 
        heuristic = None
    ):
        final_node = None
        metrics_dict = {}
        solved = False
        depth_limit = start_depth_limit

        def get_metrics() -> dict:
            metrics_dict.update({ 'depth_limit': depth_limit })

            return metrics_dict

        while not solved:
            final_node, metrics_dict = GraphSearch._IDA_star_iteration(
                graph_instance, 
                start_state, 
                apply_to_reached,
                search_condition,
                depth_limit=depth_limit,
                heuristic=heuristic
            )
            solved = final_node is not None and search_condition(final_node)
            depth_limit += increment_depth_limit

            if depth_limit > max_depth_limit:
                break

        depth_limit -= increment_depth_limit

        return final_node, get_metrics()
    
    @staticmethod
    def _IDA_star_iteration(
        graph_instance: ISearchGraph,
        start_state, 
        apply_to_reached,
        search_condition, 
        depth_limit: int = sys.maxsize,
        heuristic = None
    ):
        # start_time = time.time()
        # ref_num_reached_time = 0
        # ref_num_reached = 100000

        if not callable(heuristic):
            heuristic = BoxesToGoalsManhattan.min_manhattan_heuristic
        if search_condition(start_state):
            return start_state, { 'num_reached': 0 }
        
        start_state.total_cost = start_state.path_cost + heuristic(start_state)

        frontier = PriorityInsertStack()
        reached = set()
        frontier.put(start_state.total_cost, (start_state, 0))
        reached.add(start_state)

        def get_metrics() -> dict:
            return { 'num_reached': len(reached) }

        while not frontier.is_empty:
            current_state, current_level = frontier.pop()

            print('CURRENT: COST', current_state.total_cost, current_state.path_cost, current_state.total_cost - current_state.path_cost)
            # validate solution
            if search_condition(current_state):
                print(
                    'NUM REACHED', len(reached), 
                    # '\nREF {num} REACHED AT {time}'.format(num=ref_num_reached, time=ref_num_reached_time),
                    '\n\n'
                )
                return current_state, get_metrics()

            if current_state.total_cost >= depth_limit:
                continue   

            for next in graph_instance.get_neighbors(current_state):
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
        return None, get_metrics()

