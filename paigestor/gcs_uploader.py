import os
import requests
from io import BytesIO
from google.cloud import storage
from urllib.parse import urlparse
from paigestor.interfaces.uploader_interface import UploaderInterface


class GcsUploader(UploaderInterface):
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

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()

        content = BytesIO(response.content)
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_file(content, rewind=True)

        print(f"✅ Subido: gs://{self.bucket.name}/{destination_blob_name}")

    def upload_directory(self, local_dir: str) -> None:
        for filename in os.listdir(local_dir):
            if filename.endswith(".parquet"):
                local_path = os.path.join(local_dir, filename)
                blob = self.bucket.blob(filename)

                if blob.exists(self.client):
                    print(f"⚠️ Ya existe en GCS, se omite: {filename}")
                    continue

                print(f"📤 Subiendo {filename} a GCS...")
                blob.upload_from_filename(local_path)
                print(f"✅ Subido: gs://{self.bucket.name}/{filename}")
