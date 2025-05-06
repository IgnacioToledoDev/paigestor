import os
import requests
from google.cloud import storage
from urllib.parse import urlparse

class GcsUploader:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_from_url(self, url: str, destination_blob_name: str = None) -> None:
        if not destination_blob_name:
            destination_blob_name = os.path.basename(urlparse(url).path)

        if self.bucket.blob(destination_blob_name).exists(self.client):
            print(f"⚠️ Ya existe en GCS, se omite: {destination_blob_name}")
            return

        print(f"☁️ Subiendo: {destination_blob_name} desde {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_file(response.raw, rewind=True)

        print(f"✅ Subido: gs://{self.bucket.name}/{destination_blob_name}")
