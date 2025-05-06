from abc import ABC, abstractmethod

class UploaderInterface(ABC):
    @abstractmethod
    def upload_from_url(self, url: str, destination_blob_name: str) -> None:
        """Sube un archivo desde una URL remota directamente a GCS."""
        pass