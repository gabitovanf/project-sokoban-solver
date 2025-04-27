
class ReadFileIterator:
    def __init__(self, filepath=None, file=None):
        self._file = None
        self._closed = False
        self.__new_file(filepath=filepath, file=file)

    def __iter__(self):
        return self

    def __next__(self):
        if self._file is None or self._closed:
            raise StopIteration

        line = self._file.readline()

        if not line:
            self.close()
            raise StopIteration
        else:
            return line

    def close(self):
        if self._closed:
            return

        self._file.close()
        self._closed = True

    @property
    def file(self):
        return self._file

    @property
    def closed(self):
        return self._closed

    def __new_file(self, filepath=None, file=None):
        if file is None and isinstance(filepath, str):
            file = open(filepath, 'r')

        self._file = file
        self._closed = False
