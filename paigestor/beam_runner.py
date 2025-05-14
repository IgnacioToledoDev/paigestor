import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from paigestor.gcs_uploader import GcsUploader
from paigestor.scrapper import Scrapper
from typing import Iterator, Optional, Any
from apache_beam import DoFn, ParDo

class UploadParquetDoFn(DoFn):
    def __init__(self, bucket_name: str, *unused_args: Any, **unused_kwargs: Any):
        super().__init__(*unused_args, **unused_kwargs)
        self.bucket_name = bucket_name
        self.uploader: Optional[GcsUploader] = None  # <- declaración anticipada

    def setup(self) -> None:
        self.uploader = GcsUploader(self.bucket_name)

    def process(self, url: str, *args: Any, **kwargs: Any) -> Iterator[str]:
        try:
            self.uploader.upload_from_url(url)
            yield f"✅ Subido: {url}"
        except Exception as e:
            yield f"❌ Error en {url}: {e}"

def run_beam_pipeline(scraper: Scrapper, bucket_name: str):
    urls = scraper.get_file_urls()
    options = PipelineOptions(runner='DirectRunner')
    step: ParDo = ParDo(UploadParquetDoFn(bucket_name))
    with beam.Pipeline(options=options) as p:
        (
            p
            | "Cargar URLs" >> beam.Create(urls)
            | "Subir a GCS" >> step
            | "Mostrar resultado" >> beam.Map(print)
        )
