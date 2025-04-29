class ListArrayAdapter:

    def __init__(self):
        self.__list = []

    def put(self, item):
        self.__list.append(item)

        return self

    def add(self, item, index: int):
        self.__list.insert(index, item)

        return self

    def get(self, index: int):
        if index < 0 or index > self.size() - 1: return None
        return self.__list[index]

    def remove(self, index: int): # -> T
        return self.__list.pop(index)

    def size(self) -> int:
        return len(self.__list)

    def isEmpty(self) -> bool:
        return len(self.__list) < 1

    def copy(self) -> bool:
        return ListArrayAdapter().__copy(self.__list)

    def __copy(self, sourcelist):
        self.__list = sourcelist.copy()

        return self

    def __str__(self) -> str:
        return str(self.__list)
        