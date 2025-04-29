import math
from structure.array.FactorArray import FactorArray
from structure.array.VectorArray import VectorArray
from structure.array.IArray import IArray


class PriorityInsertQueue:
    def __init__(self):
        self.__priorityArray = VectorArray()
        self.__highestPriority = -1


    def enqueue(self, priority: int, item):
        queueArray = self.__getOrAppendNewAt(priority)

        queueArray.put(item)


    def __getOrAppendNewAt(self, newPriority: int):
        queueArray = None
        pairArray = None

        index_new_or_old = PriorityInsertQueue._binary_search(self.__priorityArray, newPriority)

        if newPriority != self.__priorityArray.get(index_new_or_old):
            queueArray = FactorArray()
            pairArray = VectorArray(None, 2)
            pairArray.put(newPriority)
            pairArray.put(queueArray)
            self.__priorityArray.add(pairArray, index_new_or_old)

            if self.__highestPriority < newPriority:
                self.__highestPriority = newPriority
        else:
            pairArray = self.__priorityArray.get(index_new_or_old)
            queueArray = pairArray.get(1)

        return queueArray


    def dequeue(self): # -> T
        if self.__highestPriority < 0:
            return None

        # Get last item - highest priority
        priorityArraySize = self.__priorityArray.size()
        pairArray = self.__priorityArray.get(priorityArraySize - 1)
        queueArray = pairArray.get(1)

        if queueArray.size() < 2:
            self.__priorityArray.remove(priorityArraySize - 1)
            priorityArraySize -= 1

            if priorityArraySize < 1:
                self.__highestPriority = -1
            else:
                pairArray = self.__priorityArray.get(priorityArraySize - 1)
                self.__highestPriority = pairArray.get(0)
            
        return queueArray.remove(0)


    @property
    def is_empty(self):
        return self.__highestPriority < 0


    @staticmethod
    def _binary_search(array: IArray, priority: int, start: int = -1, end: int = -1) -> int:
        if start < 0: start = 0
        if end < 0: end = array.size() - 1

        if end <= start:
            if priority > array.get(start):
                return start + 1
            # We'll use item that we already have
            elif priority == array.get(start):
                return start
            else:
                return start
            
        mid = int(math.ceil((start + end) / 2))
        if priority >= array.get(mid):
            return PriorityInsertQueue._binary_search(array, priority, start=mid, end=end)
        
        return PriorityInsertQueue._binary_search(array, priority, start=start, end=mid - 1)
        

    def __str__(self) -> str:
        return ('PriorityMatrixQueue: [' + ', \n'.join(list(map(
            lambda x: '[{p}, {val}]'.format(p=x[0], val=x[1]),
            # lambda x: str(x),
            enumerate(self.__priorityArray)
        ))) + ']')

