import logging
from db.connections.session import engine
from db.connections.base import Base

# Import all models here so that Base.metadata learns about them
import db.models.transactions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    logger.info("Creating tables in the database...")
    # This will create all tables defined across all imported models
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
