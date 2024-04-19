from abc import *


class IoFile(metaclass=ABCMeta):
    def __init__(self):
        self.iter_set = None
        self.iter_get = {}

    @abstractmethod
    def get_dir_iter(self):
        pass

    @abstractmethod
    def set_dir(self, name):
        pass

    def get_value_iter(self, key):
        try:
            res = self.iter_get[key].__next__()
        except StopIteration:
            res = ''
        return res

    @abstractmethod
    def init_result(self, key):
        pass

    @abstractmethod
    def get_dir_iter(self):
        pass

    @abstractmethod
    def set_dir(self, name):
        pass

    @abstractmethod
    def create_values(self, key):
        pass

    @abstractmethod
    def create_keyword_iter(self, row):
        pass

    @abstractmethod
    def insert_keyword_iter(self, val):
        pass

    @abstractmethod
    def create_value_iter(self, row):
        pass

    @abstractmethod
    def insert_value_iter(self, val):
        pass

    @abstractmethod
    def __del__(self):
        pass


class Iterable(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass
