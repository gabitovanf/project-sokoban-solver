import math
from structure.array.FactorArray import FactorArray
from structure.array.VectorArray import VectorArray
from structure.array.IArray import IArray


# To reduce memory usage
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

        if (self.__highestPriority < 0 
            or index_new_or_old > self.__priorityArray.size() - 1
            or (self.__priorityArray.get(index_new_or_old) is not None 
                and newPriority != self.__priorityArray.get(index_new_or_old).get(0)
                )
            ):
            queueArray = FactorArray()
            pairArray = VectorArray(None, 2)
            pairArray.put(newPriority)
            pairArray.put(queueArray)
            self.__priorityArray.add(pairArray, index_new_or_old)

            if self.__highestPriority < newPriority:
                self.__highestPriority = newPriority
        else:
            print(index_new_or_old, self.__priorityArray.size())
            pairArray = self.__priorityArray.get(index_new_or_old)
            queueArray = pairArray.get(1)

        return queueArray


    def dequeue(self): # -> T
        if self.__highestPriority < 0:
            return None

        # Get last item - the highest priority
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
    def _binary_search(array: IArray, new_value: int, start: int = -1, end: int = -1) -> int:
        if start < 0: start = 0
        if end < 0: end = array.size() - 1


        if end <= start:
            if array.size() < 1:
                return 0
            if new_value > array.get(start).get(0):
                return start + 1
            # We'll use item that we already have
            if new_value == array.get(start).get(0):
                return start
    
            return start
            
        mid = int(math.ceil((start + end) / 2))
        if new_value >= array.get(mid).get(0):
            return PriorityInsertQueue._binary_search(array, new_value, start=mid, end=end)
        
        return PriorityInsertQueue._binary_search(array, new_value, start=start, end=mid - 1)
        

    def __str__(self) -> str:
        return ('PriorityInsertQueue: [' + ', \n'.join(list(map(
            lambda x: '[{p}, {val}]'.format(p=x.get(0), val=x.get(1)),
            # lambda x: str(x),
            self.__priorityArray
        ))) + ']')

