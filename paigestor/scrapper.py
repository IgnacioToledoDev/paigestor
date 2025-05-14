import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from datetime import datetime
from typing import List
from paigestor.interfaces.scrapper_interface import ScrapperInterface

class Scrapper(ScrapperInterface):
    def __init__(self, base_url: str, enabled_debug_mode: bool, from_year: int = 2022):
        self.base_url = base_url
        self.from_year = from_year
        self.today = datetime.today()
        self.current_year = datetime.today().year
        self.enabled_debug_mode = enabled_debug_mode

    def get_file_urls(self) -> List[str]:
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, "html.parser")

        valid_urls = []

        for a in soup.find_all("a", href=True):
            raw_href = a["href"].strip()
            full_url = urljoin(self.base_url, raw_href)
            parsed = urlparse(full_url)

            if not parsed.path.endswith(".parquet") and self.enabled_debug_mode:
                print(f"⛔️ Ignorado (no parquet): {full_url}")
                continue

            if not re.search(r"(green|yellow)", parsed.path, re.IGNORECASE) and self.enabled_debug_mode:
                print(f"⛔️ Ignorado (no green/yellow): {full_url}")
                continue

            # Extrae fecha YYYY-MM o YYYY_MM
            match = re.search(r"(\d{4})[-_](\d{2})", parsed.path)
            if not match and self.enabled_debug_mode:
                print(f"⛔️ Ignorado (sin fecha): {full_url}")
                continue

            year, month = int(match.group(1)), int(match.group(2))
            file_date = datetime(year, month, 1)

            if not (datetime(self.from_year, 1, 1) <= file_date <= datetime(2024, 12, 31)):
                continue

            valid_urls.append(full_url)

        print(f"\n✅ Total archivos válidos encontrados: {len(valid_urls)}")
        return valid_urls

    def download_files(self, urls: List[str], output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)

        for url in urls:
            filename = os.path.join(output_dir, os.path.basename(urlparse(url).path))

            if os.path.exists(filename):
                print(f"⚠️ Ya existe localmente, se omite: {filename}")
                continue

            print(f"\n📥 Descargando: {url}")

            try:
                with requests.get(url, stream=True) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))

                    with open(filename, "wb") as file, tqdm(
                            total=total_size,
                            unit="B",
                            unit_scale=True,
                            unit_divisor=1024,
                            desc=os.path.basename(filename),
                            ncols=80,
                    ) as bar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                                bar.update(len(chunk))
            except Exception as e:
                print(f"❌ Error al descargar {url}: {e}")

    def upload_files_directly(self, urls: List[str], uploader) -> None:
        """
        Sube archivos .parquet directamente desde sus URLs al bucket de GCS
        sin almacenarlos en disco local.
        """
        for url in urls:
            try:
                print(f"\n☁️ Subiendo directamente: {url}")
                uploader.upload_from_url(url)
            except Exception as e:
                print(f"❌ Error al subir archivo: {e}")