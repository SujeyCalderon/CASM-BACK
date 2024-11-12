# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Cadena de conexión de PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:calmar5@localhost/CASM"

# Crea el motor y la sesión
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)  # pool_pre_ping ayuda a evitar problemas de conexión inactiva
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base para tus modelos
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
