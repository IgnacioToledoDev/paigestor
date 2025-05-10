from abc import ABC, abstractmethod

class UploaderInterface(ABC):
    @abstractmethod
    def upload_from_url(self, url: str, destination_blob_name: str) -> None:
        """Sube un archivo desde una URL remota directamente a GCS."""
        pass

    @abstractmethod
    def upload_directory(self, local_dir: str) -> None:
        pass

    upload_directory