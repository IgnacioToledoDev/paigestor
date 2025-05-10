# setup.py
from setuptools import setup, find_packages

setup(
    name="paigestor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "beautifulsoup4",
        "google-cloud-storage",
        "tqdm"
    ],
    entry_points={
        "console_scripts": [
            "paigestor=paigestor.cli:main",
        ],
    },
    author="@IgnacioToledoDev",
    description="Herramienta CLI para scrapear archivos .parquet y subirlos a GCS",
    python_requires=">=3.12",
)
