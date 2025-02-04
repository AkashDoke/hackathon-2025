import logging
import sqlite3
import os
import urllib.request
import zipfile
import logging

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


# Define the new SQLite version
SQLITE_VERSION = "3.42.0"  # Change this to the latest available version
SQLITE_DOWNLOAD_URL = f"https://www.sqlite.org/2023/sqlite-tools-linux-x86-{SQLITE_VERSION}.zip"
SQLITE_EXTRACT_PATH = os.path.join(os.getcwd(), "sqlite3_new")

def download_and_extract_sqlite():
    """Downloads and extracts SQLite to a local folder."""
    try:
        if not os.path.exists(SQLITE_EXTRACT_PATH):
            os.makedirs(SQLITE_EXTRACT_PATH)

        zip_path = os.path.join(SQLITE_EXTRACT_PATH, "sqlite.zip")

        logger.info("Downloading SQLite...")
        urllib.request.urlretrieve(SQLITE_DOWNLOAD_URL, zip_path)
        
        logger.info("Extracting SQLite...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(SQLITE_EXTRACT_PATH)

        logger.info(f"SQLite extracted to: {SQLITE_EXTRACT_PATH}")

    except Exception as e:
        logger.error(f"Error downloading or extracting SQLite: {e}")

# Run the download function
download_and_extract_sqlite()



SQLITE_NEW_PATH = os.path.join(os.getcwd(), "sqlite3_new")

# Force Python to use the new SQLite
try:
    os.environ["LD_LIBRARY_PATH"] = SQLITE_NEW_PATH + ":" + os.environ.get("LD_LIBRARY_PATH", "")
    os.environ["PATH"] = SQLITE_NEW_PATH + ":" + os.environ["PATH"]

    logger.info("Using updated SQLite path.")
except Exception as e:
    logger.error(f"Failed to update SQLite path: {e}")

# Verify SQLite version
try:
    sqlite_version = sqlite3.sqlite_version
    logger.info(f"Updated SQLite version: {sqlite_version}")
except Exception as e:
    logger.error(f"Error verifying SQLite version: {e}")

# Test SQLite version logging
try:
    sqlite_version = sqlite3.sqlite_version
    logger.info(f"SQLite version: {sqlite_version}")
except Exception as e:
    logger.error(f"Error fetching SQLite version: {e}")

# Test ChromaDB logging
try:
    import chromadb
    logger.info("ChromaDB is working!")
except ImportError:
    logger.error("ChromaDB import failed. Install it using: pip install chromadb")
