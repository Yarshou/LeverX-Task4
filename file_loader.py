from abc import ABC, abstractmethod
import json


class FileLoad(ABC):

    @abstractmethod
    def load(self, filepath):
        pass


class JSONLoad(FileLoad):

    def load(self, filepath):
        try:
            with open(filepath) as file:
                data = json.load(file)
        except FileNotFoundError as error:
            print(f'{error.filename} was not found')
            return None
        return data
