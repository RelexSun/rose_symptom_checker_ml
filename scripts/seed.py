import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, inspect
from rose_symptom_checker.db.base import Base
from rose_symptom_checker.db.models import User, Diagnosis
from rose_symptom_checker.core.config import get_settings
from rose_symptom_checker.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


def drop_all_tables(engine):
    """Drop all existing tables"""
    logger.warning("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("✓ All tables dropped")


def create_all_tables(engine):
    """Create all tables from models"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ All tables created successfully")


def check_tables_exist(engine):
    """Check which tables exist in database"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        logger.info(f"Existing tables: {', '.join(tables)}")
        return tables
    else:
        logger.info("No tables found in database")
        return []


def seed_sample_data(engine):
    """Add sample data for testing"""
    from sqlalchemy.orm import sessionmaker
    import json
    from datetime import datetime
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        logger.info("Seeding sample data...")
        
        # Create sample users
        sample_users = [
            {
                "email": "admin@rosecheck.com",
                "username": "admin",
                "password": "admin123456"
            },
            {
                "email": "demo@example.com",
                "username": "demo_user",
                "password": "demo123456"
            },
            {
                "email": "test@test.com",
                "username": "testuser",
                "password": "test123456"
            }
        ]
        
        created_users = []
        for user_data in sample_users:
            # Check if user already exists
            existing = session.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    hashed_password=get_password_hash(user_data["password"]),
                    is_active=True
                )
                session.add(user)
                created_users.append(user)
                logger.info(f"  ✓ Created user: {user_data['username']}")
            else:
                logger.info(f"  - User already exists: {user_data['username']}")
                created_users.append(existing)
        
        session.commit()
        
        # Refresh to get IDs
        for user in created_users:
            session.refresh(user)
        
        # Create sample diagnoses
        sample_diagnoses = [
            {
                "user_idx": 0,  # admin
                "symptoms": ["dark_spots_on_leaves", "yellowing_leaves", "leaf_drop"],
                "disease": "Black Spot",
                "confidence": 0.95,
                "recommendations": [
                    "Remove and destroy infected leaves immediately",
                    "Apply fungicide every 7-14 days",
                    "Improve air circulation by pruning"
                ]
            },
            {
                "user_idx": 0,  # admin
                "symptoms": ["white_powdery_coating", "distorted_leaves"],
                "disease": "Powdery Mildew",
                "confidence": 0.88,
                "recommendations": [
                    "Spray with neem oil or sulfur-based fungicide",
                    "Increase air circulation",
                    "Remove infected plant parts"
                ]
            },
            {
                "user_idx": 1,  # demo_user
                "symptoms": ["orange_rust_spots", "leaf_underside_pustules"],
                "disease": "Rust",
                "confidence": 0.92,
                "recommendations": [
                    "Remove infected leaves and debris",
                    "Apply fungicide containing myclobutanil",
                    "Improve air circulation"
                ]
            },
            {
                "user_idx": 2,  # testuser
                "symptoms": [],
                "disease": "Healthy",
                "confidence": 0.98,
                "recommendations": [
                    "Continue regular maintenance",
                    "Monitor for early signs of disease",
                    "Maintain proper watering schedule"
                ]
            }
        ]
        
        for diag_data in sample_diagnoses:
            diagnosis = Diagnosis(
                user_id=created_users[diag_data["user_idx"]].id,
                symptoms=json.dumps(diag_data["symptoms"]),
                disease_predicted=diag_data["disease"],
                confidence_score=diag_data["confidence"],
                recommendations=json.dumps(diag_data["recommendations"])
            )
            session.add(diagnosis)
        
        session.commit()
        logger.info(f"✓ Created {len(sample_diagnoses)} sample diagnoses")
        
        logger.info("\n" + "="*50)
        logger.info("Sample User Credentials:")
        logger.info("="*50)
        for user_data in sample_users:
            logger.info(f"Email: {user_data['email']}")
            logger.info(f"Password: {user_data['password']}")
            logger.info("-"*50)
        
    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def init_database(drop_existing=False, seed_data=False):
    """
    Main function to initialize database
    
    Args:
        drop_existing: If True, drop all tables before creating
        seed_data: If True, add sample data after creating tables
    """
    logger.info("="*60)
    logger.info("Rose Symptom Checker - Database Initialization")
    logger.info("="*60)
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    logger.info("")
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL, echo=False)
    
    # Check existing tables
    existing_tables = check_tables_exist(engine)
    
    # Drop tables if requested
    if drop_existing and existing_tables:
        confirm = input("\n⚠️  This will DELETE all existing data. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            drop_all_tables(engine)
        else:
            logger.info("Operation cancelled by user")
            return
    
    # Create tables
    create_all_tables(engine)
    
    # Verify tables created
    created_tables = check_tables_exist(engine)
    logger.info(f"\n✓ Database initialized with {len(created_tables)} tables")
    
    # Seed data if requested
    if seed_data:
        seed_sample_data(engine)
    
    logger.info("\n" + "="*60)
    logger.info("Database initialization complete!")
    logger.info("="*60)