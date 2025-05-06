from abc import ABC, abstractmethod
from typing import List

class ScrapperInterface(ABC):
    @abstractmethod
    def get_file_urls(self) -> List[str]:
        pass

    @abstractmethod
    def download_files(self, urls: List[str], output_dir: str) -> None:
        pass
