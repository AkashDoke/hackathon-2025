import logging
import sqlite3

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - %(message)s",
    level=logging.INFO,  # Change to DEBUG for more details
    handlers=[
        logging.FileHandler("streamlit_app.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ]
)

# Logger instance
logger = logging.getLogger(__name__)

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
