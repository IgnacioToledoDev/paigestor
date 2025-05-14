import click
from paigestor.scrapper import Scrapper
from paigestor.orchestrator import ScrapeAndUploadOrchestrator
from paigestor.gcs_uploader import GcsUploader

@click.command(help="""
Scrapea una URL en busca de archivos .parquet, los descarga localmente y opcionalmente los sube a Google Cloud Storage.

Ejemplos de uso:
  - Solo descargar archivos:
      paigestor --only-scraper

  - Descargar y subir a GCS directamente:
      paigestor --bucket "mi-bucket"
      
  - Descargar y subir a GCS usando Apache Beam:
      paigestor --bucket "mi-bucket" --use-beam
""")
# @click.option('--url', required=True, help='URL base para buscar archivos .parquet')
@click.option('--bucket', required=False, help='Bucket GCS (opcional si usas --only-scraper)')
@click.option('--temp-dir', default='downloads', help='Directorio temporal para guardar archivos')
@click.option('--only-scraper', is_flag=True, help='Ejecuta solo el scraper, sin subir a GCS')
@click.option('--debug', is_flag=True, help='Activa modo debug')
@click.option('--use-beam', is_flag=True, help='Usa Apache Beam para subir directamente a GCS')
def main(bucket, temp_dir, only_scraper, use_beam, enabled_debug_mode=False):
    DEFAULT_URL = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    scraper = Scrapper(DEFAULT_URL, enabled_debug_mode)

    if only_scraper:
        print("🕷️ Ejecutando solo el scraper...")
        urls = scraper.get_file_urls()

        if bucket:
            if use_beam:
                print("☁️ Subiendo con Apache Beam...")
                from paigestor.beam_runner import run_beam_pipeline
                run_beam_pipeline(scraper, bucket)
            else:
                print(f"☁️ Subiendo directamente a GCS: {bucket}")
                uploader = GcsUploader(bucket)
                scraper.upload_files_directly(urls, uploader)
        else:
            print("💾 Descargando archivos localmente...")
            scraper.download_files(urls, temp_dir)
    else:
        if not bucket:
            raise click.UsageError("Debe especificar --bucket si no usas --only-scraper.")

        if use_beam:
            print("🚀 Ejecutando pipeline con Apache Beam...")
            from paigestor.beam_runner import run_beam_pipeline
            run_beam_pipeline(scraper, bucket)
        else:
            uploader = GcsUploader(bucket)
            orchestrator = ScrapeAndUploadOrchestrator(scraper, uploader, temp_dir)
            orchestrator.execute()

if __name__ == '__main__':
    main()
