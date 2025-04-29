from structure.queue.IPriorityQueue import IPriorityQueue
from structure.array.FactorArray import FactorArray


class PriorityArrayQueue(IPriorityQueue):

    def __init__(self):
        self.__prioritySortedList = FactorArray()


    def enqueue(self, priority: int, item):
        queueArrayRecord = None

        index, needsAdd = self.__findIndexOfPriority(priority)

        if needsAdd:
            queueArrayRecord = [None] * 2
            queueArrayRecord[0] = priority
            queueArrayRecord[1] = FactorArray()

            self.__prioritySortedList.add(queueArrayRecord, index)
        else:
            queueArrayRecord = self.__prioritySortedList.get(index)

        queueArrayRecord[1].put(item)


    def __findIndexOfPriority(self, priority: int):
        size1 = self.__prioritySortedList.size() - 1

        if size1 < 0:
            return 0, True

        if priority > self.__prioritySortedList.get(size1)[0]:
            return size1 + 1, True

        if priority < self.__prioritySortedList.get(0)[0]:
            return 0, True

        start = 0
        end = size1
        index = start + (end - start) // 2

        while end - start > 0:
            itemPriority = self.__prioritySortedList.get(index)[0]

            if itemPriority > priority: 
                end = index - 1
            elif itemPriority < priority:
                start = index + 1
            else:
                return index, False
                break

            index = start + (end - start) // 2

        itemPriority = self.__prioritySortedList.get(index)[0]

        if itemPriority < priority:
            index += 1

        return index, self.__prioritySortedList.get(index)[0] != priority


    def dequeue(self): # -> T
        size1 = self.__prioritySortedList.size() - 1

        if size1 < 0:
            return None

        queueArray = self.__prioritySortedList.get(size1)[1]

        if queueArray.size() < 2:  
            self.__prioritySortedList.remove(size1)

        return queueArray.remove(0)
    

    @property
    def is_empty(self):
        return self.__prioritySortedList.size() - 1 < 0


    def __str__(self) -> str:
        return 'PriorityArrayQueue: ' + str(FactorArray(map(lambda x: '{p}, {val}'.format(p=x[0], val =x[1]), self.__prioritySortedList)))
    