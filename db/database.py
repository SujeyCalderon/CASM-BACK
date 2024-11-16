# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from motor.motor_asyncio import AsyncIOMotorClient


DATABASE_URL = "postgresql://nuevo@localhost/casm3"  

#Conexión a MongoDB Atlas
MONGO_DB_URL = "mongodb+srv://233291:calmar58@casmdb.jht9l.mongodb.net/?retryWrites=true&w=majority&appName=CASMDB"

client = AsyncIOMotorClient(MONGO_DB_URL)
mongo_db = client["CASM"]

publications_collection = mongo_db["publications"]
chat_collection = mongo_db["chat"]


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
