from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infra.mapper import init_mapper
from .infra.repository import metadata

SQLALCHEMY_DATABASE_URL = "sqlite:///./kaffe-chon-chan-soong.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
init_mapper()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()