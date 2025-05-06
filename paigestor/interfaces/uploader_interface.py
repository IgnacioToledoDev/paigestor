from abc import ABC, abstractmethod

class UploaderInterface(ABC):
    @abstractmethod
    def upload_directory(self, path: str) -> None:
        pass