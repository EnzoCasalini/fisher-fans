from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion SQLite
DATABASE_URL = "sqlite:///./fisher_fans.db"

# Crée un moteur de base de données
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session pour les interactions avec la BDD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base: DeclarativeMeta = declarative_base()