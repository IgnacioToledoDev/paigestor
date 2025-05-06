import click
from paigestor.scrapper import Scrapper
from paigestor.orchestrator import ScrapeAndUploadOrchestrator
from paigestor.gcs_uploader import GcsUploader

@click.command(help="""
Scrapea una URL en busca de archivos .parquet, los descarga localmente y opcionalmente los sube a Google Cloud Storage.

Ejemplos de uso:
  - Solo descargar archivos:
      paigestor --url "https://example.com/data" --only-scraper

  - Descargar y subir a GCS:
      paigestor --url "https://example.com/data" --bucket "mi-bucket"
""")
@click.option('--url', required=True, help='URL base para buscar archivos .parquet')
@click.option('--bucket', required=False, help='Bucket GCS (opcional si usas --only-scraper)')
@click.option('--temp-dir', default='downloads', help='Directorio temporal para guardar archivos')
@click.option('--only-scraper', is_flag=True, help='Ejecuta solo el scraper, sin subir a GCS')
def main(url, bucket, temp_dir, only_scraper):
    scraper = Scrapper(url)

    if only_scraper:
        print("🕷️ Ejecutando solo el scraper...")
        urls = scraper.get_file_urls()

        if bucket:
            print(f"☁️ Subiendo directamente a GCS: {bucket}")
            uploader = GcsUploader(bucket)
            scraper.upload_files_directly(urls, uploader)
        else:
            print("💾 Descargando archivos localmente...")
            scraper.download_files(urls, temp_dir)
    else:
        if not bucket:
            raise click.UsageError("Debe especificar --bucket si no usas --only-scraper.")

        uploader = GcsUploader(bucket)
        orchestrator = ScrapeAndUploadOrchestrator(scraper, uploader, temp_dir)
        orchestrator.execute()

if __name__ == '__main__':
    main()
