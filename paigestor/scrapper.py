import os
from abc import ABC
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List
from paigestor.interfaces.scrapper_interface import ScrapperInterface

class Scrapper(ScrapperInterface, ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_file_urls(self) -> List[str]:
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, "html.parser")
        return [
            urljoin(self.base_url, a['href'])
            for a in soup.find_all('a', href=True)
            if a['href'].endswith('.parquet')
        ]

    def download_files(self, urls: List[str], output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)
        for url in urls:
            filename = os.path.join(output_dir, os.path.basename(url))
            print(f"Descargando {url}")
            r = requests.get(url)
            with open(filename, "wb") as f:
                f.write(r.content)