from structure.array.IArray import IArray

class SingleArray(IArray):

    def __init__(self, iterator = None):
        self.__array = []

        if iterator is not None:
            self.__generate(iterator)


    def __resize(self):
        newarray = [None]*(self.size() + 1)

        for i in range(0, self.size()):
            newarray[i] = self.__array[i]

        self.__array = newarray


    def put(self, item):
        self.__resize()
        self.__array[self.size() - 1] = item


    def add(self, item, index: int):
        newarray = [None]*(self.size() + 1)

        for i in range(0, index):
            newarray[i] = self.__array[i]

        newarray[index] = item

        for i in range(index, self.size()):
            newarray[i + 1] = self.__array[i]

        self.__array = newarray

        return self


    def get(self, index: int):
        if index < 0 or index > self.size() - 1: return None
        return self.__array[index]


    def remove(self, index: int): # -> T
        newarray = [None]*(self.size() - 1)

        for i in range(0, index):
            newarray[i] = self.__array[i]

        val = self.__array[index]

        for i in range(index, self.size() - 1):
            newarray[i] = self.__array[i + 1]

        self.__array = newarray

        return val


    def size(self) -> int:
        return len(self.__array)


    def isEmpty(self) -> bool:
        return self.size() < 1


    # TO TEST ONLY
    def copy(self) -> bool:
        return SingleArray().__copy(self.__array)


    def __copy(self, sourcelist):
        self.__array = sourcelist.copy()

        return self


    def __generate(self, iterator):
        self.__array = list(iterator)


    def __iter__(self):
        self.__index = 0
        return self


    def __next__(self):
        size = self.size()

        if self.__index > size - 1:
            raise StopIteration

        next = self.get(self.__index)
        self.__index += 1

        return next


    def __str__(self) -> str:
        return '[' + ', '.join(list(map(lambda x: str(x), self.__array))) + ']'
        