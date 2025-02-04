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

# Test ChromaDB logging
try:
    import chromadb
    logger.info("ChromaDB is working!")
except ImportError:
    logger.error("ChromaDB import failed. Install it using: pip install chromadb")
