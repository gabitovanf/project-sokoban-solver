import json
from utils.file.read.ReadFileIterator import ReadFileIterator


class ReadFile:
    @staticmethod
    def content(filepath) -> str:
        if not ReadFile.__validate_path(filepath):
            return ''

        text = ''
        try:
            with open(filepath, 'r') as f:
                text = f.read()
        except Exception as e:
            print(e)

        return text

    @staticmethod
    def line_iterator(filepath):
        if not ReadFile.__validate_path(filepath):
            return None

        return iter(ReadFileIterator(filepath=filepath))

    @staticmethod
    def lines(filepath) -> list:
        if not ReadFile.__validate_path(filepath):
            return []

        lines = []
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            print(e)

        return lines

    @staticmethod
    def json(filepath):
        if not ReadFile.__validate_path(filepath):
            return None

        data = None
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(e)

        return data

    @staticmethod
    def __validate_path(filepath) -> bool:
        return isinstance(filepath, str)
