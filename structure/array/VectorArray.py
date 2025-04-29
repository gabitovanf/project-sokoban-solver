from structure.array.IArray import IArray


class VectorArray(IArray):
    def __init__(self, iterator = None, vector: int = 10):
        self.__vector = vector
        self.__array = [None] * self.__vector 
        self.__size = 0

        if iterator is not None:
            self.__generate(iterator)


    def __resize(self):
        newarray = [None] * (len(self.__array) + self.__vector)

        for i in range(0, self.size()):
            newarray[i] = self.__array[i]

        self.__array = newarray


    def __cutdown(self):
        newarray = [None] * (len(self.__array) - self.__vector)

        for i in range(0, self.size()):
            newarray[i] = self.__array[i]

        self.__array = newarray


    def put(self, item):
        if self.size() >= len(self.__array):
            self.__resize()

        self.__array[self.__size] = item
        self.__size += 1

        return self


    def add(self, item, index: int):
        if self.size() >= len(self.__array):
            self.__resize()

        for i in range(self.size() - 1, index - 1, -1):
            self.__array[i + 1] = self.__array[i]

        self.__size += 1

        self.__array[index] = item

        return self


    def get(self, index: int):
        if index < 0 or index > self.size() - 1: return None
        return self.__array[index]


    def set(self, item, index: int):
        if index < 0 or index > self.size() - 1: return self

        self.__array[index] = item
        return self
        

    def remove(self, index: int): # -> T
        val = self.__array[index]

        for i in range(index, self.size() - 1):
            self.__array[i] = self.__array[i + 1]

        self.__array[self.size() - 1] = None
        self.__size -= 1

        if self.size() <= len(self.__array) - self.__vector:
            self.__cutdown()

        return val


    def size(self) -> int:
        return self.__size


    def isEmpty(self) -> bool:
        return self.__size < 1


    # TO TEST ONLY
    def copy(self) -> bool:
        arr = VectorArray(vector=self.__vector)
        arr.__size = self.__size
        return arr.__copy(self.__array)

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
        return '[' + ', '.join(list(map(lambda x: str(x), self.__array[0:self.__size]))) + ']'
