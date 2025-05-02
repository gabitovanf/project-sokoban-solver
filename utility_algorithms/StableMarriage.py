import math
from structure.matrix.ListMatrix import ListMatrix
from structure.queue.Queue import Queue
from structure.array.IArray import IArray
from structure.array.ListArrayAdapter import ListArrayAdapter


class StableMarriage:
    @staticmethod
    def GaleShapley(matrix: ListMatrix, comparizon_function=None):
        # Default comparizon_function leads to a maximum result

        if not callable(comparizon_function):
            comparizon_function = lambda a, b: a - b
            
        acceptor_temp_decision = [(-1, None)] * matrix.cols
        proposal_table = [None] * matrix.rows

        # 1. Fill in proposal table
        for proposal_i in range(0, matrix.rows, 1):
            proposals_sorted = ListArrayAdapter()
            proposals_sorted_queue = Queue()
            proposal_table[proposal_i] = proposals_sorted_queue

            for acceptor_i in range(0, matrix.cols, 1):
                cost = matrix.get(acceptor_i, proposal_i)
                item = (acceptor_i, cost)
                index = StableMarriage._binary_search(
                    proposals_sorted, 
                    item,
                    comparizon_function = lambda a, b: -1 * comparizon_function(a[1], b[1])
                )
                proposals_sorted.add(item, index)

            for i in range(0, proposals_sorted.size(), 1):
                proposals_sorted_queue.enqueue(proposals_sorted.get(i))

        # print('proposal_table')
        # for proposal_i in range(0, matrix.rows, 1):
        #     print(proposal_table[proposal_i])
            

        queue = Queue()

        # 2. Rounds:

        # - queue for the first round
        for proposal_i in range(0, matrix.rows, 1):
            queue.enqueue(proposal_i)
        
        while not queue.is_empty:
            proposal_i = queue.dequeue()
            acceptors_queue = proposal_table[proposal_i]
            if acceptors_queue.is_empty:
                print('Failed. List of Proposal {i} is empty'.format(i=proposal_i))
                
                for i, decision in enumerate(acceptor_temp_decision):
                    print(i, '>', decision)
                
                return None

            to_acceptor, _ = acceptors_queue.dequeue()
            
            # Make a proposal
            cost = matrix.get(to_acceptor, proposal_i)
            prev_index, prev_cost = acceptor_temp_decision[to_acceptor]
            if prev_index < 0:
                acceptor_temp_decision[to_acceptor] = (proposal_i, cost)

            elif comparizon_function(cost, prev_cost) > 0:
                queue.enqueue(prev_index)
                acceptor_temp_decision[acceptor_i] = (proposal_i, cost)
            else:
                queue.enqueue(proposal_i)
            # else acceptor rejects

        # 3. Format result pairs info

        # i.e. <row index>, <col index>, <value chosen>
        return list(map(lambda d_tuple: (d_tuple[1][0], d_tuple[0], d_tuple[1][1]), enumerate(acceptor_temp_decision)))


    @staticmethod
    def _binary_search(array: IArray, new_value: int, start: int = -1, end: int = -1, comparizon_function=None) -> int:
        if not callable(comparizon_function):
            comparizon_function = lambda a, b: a - b

        if start < 0: start = 0
        if end < 0: end = array.size() - 1

        if end <= start:
            if array.size() < 1:
                return 0
            if comparizon_function(new_value, array.get(start)) >= 0:
                return start + 1
    
            return start
            
        mid = int(math.ceil((start + end) / 2))
        if comparizon_function(new_value, array.get(mid)) >= 0:
            return StableMarriage._binary_search(array, new_value, start=mid, end=end, comparizon_function=comparizon_function)
        
        return StableMarriage._binary_search(array, new_value, start=start, end=mid - 1, comparizon_function=comparizon_function)