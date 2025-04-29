from structure.array.SingleArray import SingleArray
from structure.array.VectorArray import VectorArray
from structure.array.IArray import IArray


class MatrixArray(IArray):
    def __init__(self, vector: int = 10):
        self.__vector = vector
        self.__array = SingleArray()
        self.__size = 0


    def __resize(self):
        self.__array.put(VectorArray(vector=self.__vector))


    def __cutdown(self):
        self.__array.remove(self.__array.size() - 1)

    
    def put(self, item):
        if (self.__size >= self.__array.size() * self.__vector):
            self.__resize()

        self.__array.get(self.__size // self.__vector).put(item)
        self.__size += 1

        return self


    def add(self, item, index: int):
        if (self.__size >= self.__array.size() * self.__vector):
            self.__resize()

        i = index // self.__vector
        imax = (self.__size - 1) // self.__vector

        for j in range(imax, i, -1):
            self.__array.get(j).add(self.__array.get(j - 1).remove(self.__vector - 1), 0)

        self.__array.get(i).add(item, index % self.__vector)
        self.__size += 1

        return self


    def get(self, index: int):
        i = index // self.__vector
        if i < 0 or i > self.__array.size() - 1: return None

        return self.__array.get(i).get(index % self.__vector)


    def remove(self, index: int): # -> T
        i = index // self.__vector
        imax = (self.__size - 1) // self.__vector

        val = self.__array.get(i).remove(index % self.__vector)

        for j in range(i, imax):
            self.__array.get(j).put(self.__array.get(j + 1).remove(0))

        self.__size -= 1

        if ((self.__size - 1) // self.__vector < self.__array.size() - 1):
            self.__cutdown()

        return val


    def size(self) -> int:
        return self.__size


    def isEmpty(self) -> bool:
        return self.__size < 1


    # TO TEST ONLY
    def copy(self) -> bool:
        arr = MatrixArray(vector=self.__vector)
        arr.__size = self.__size
        arr.__array = SingleArray(map(lambda vec: vec.copy(), self.__array))

        return arr


    def __str__(self) -> str:
        s = '['
        num = self.__size // self.__vector

        for i in range(0, num):
            s += str(self.__array.get(i))[1:-1]
            s += ', '

        for i in range(0, self.__size % self.__vector):
            s += str(self.__array.get(num).get(i))
            s += ', '

        s = s[:-2]
        s += ']'

        return s
        