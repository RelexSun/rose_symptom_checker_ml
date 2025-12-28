from rose_symptom_checker.db.base import Base
from rose_symptom_checker.db.session import engine
from rose_symptom_checker.db.models import User, Diagnosis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Create all database tables"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database tables created successfully!")


if __name__ == "__main__":
    init_db()