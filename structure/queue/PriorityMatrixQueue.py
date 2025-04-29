from structure.queue.IPriorityQueue import IPriorityQueue
from structure.array.FactorArray import FactorArray
from structure.array.VectorArray import VectorArray


class PriorityMatrixQueue(IPriorityQueue):
    
    def __init__(self):
        self.__priorityArray = VectorArray()
        self.__highestPriority = -1


    def enqueue(self, priority: int, item):
        queueArray = self.__priorityArray.get(priority)

        if queueArray is None:
            queueArray = self.__appendNewAt(priority)

        queueArray.put(item)


    def __appendNewAt(self, newPriority: int):
        queueArray = FactorArray()

        if newPriority < self.__priorityArray.size():

            self.__priorityArray.set(queueArray, newPriority)

            if self.__highestPriority < newPriority:
                self.__highestPriority = newPriority

        else:

            while newPriority > self.__priorityArray.size():
                self.__priorityArray.put(None)

            self.__priorityArray.put(queueArray)
            self.__highestPriority = newPriority
            
        return queueArray


    def dequeue(self): # -> T
        if self.__highestPriority < 0:
            return None

        queueArray = self.__priorityArray.get(self.__highestPriority)

        if queueArray.size() < 2:
            self.__priorityArray.set(None, self.__highestPriority)

            index = self.__highestPriority - 1
            while index > -1 and self.__priorityArray.get(index) is None:
                index -= 1

            self.__highestPriority = index
            

        return queueArray.remove(0)


    @property
    def is_empty(self):
        return self.__highestPriority < 0


    def __str__(self) -> str:
        return ('PriorityMatrixQueue: [' + ', \n'.join(list(map(
            lambda x: '[{p}, {val}]'.format(p=x[0], val=x[1]),
            # lambda x: str(x),
            enumerate(self.__priorityArray)
        ))) + ']')
