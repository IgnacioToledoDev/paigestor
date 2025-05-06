# services/gcs_uploader.py
import os
from google.cloud import storage
from paigestor.interfaces.uploader_interface import UploaderInterface

class GcsUploader(UploaderInterface):
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_directory(self, path: str) -> None:
        for file in os.listdir(path):
            if file.endswith(".parquet"):
                blob = self.bucket.blob(file)
                full_path = os.path.join(path, file)
                print(f"Subiendo {file} a GCS...")
                blob.upload_from_filename(full_path)
