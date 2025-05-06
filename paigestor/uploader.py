# orchestrator.py
from paigestor.interfaces.scrapper_interface import ScrapperInterface
from paigestor.interfaces.uploader_interface import UploaderInterface

class ScrapeAndUploadOrchestrator:
    def __init__(self, scraper: ScrapperInterface, uploader: UploaderInterface, temp_dir: str):
        self.scraper = scraper
        self.uploader = uploader
        self.temp_dir = temp_dir

    def execute(self):
        urls = self.scraper.get_file_urls()
        self.scraper.download_files(urls, self.temp_dir)
        self.uploader.upload_directory(self.temp_dir)
