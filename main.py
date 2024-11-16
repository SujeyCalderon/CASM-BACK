from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db.database import engine, Base, SessionLocal
from routes import (
    directory_routes,
    favorites_routes,
    notes_routes,
    publications_routes,
    role_routes,
    referency_router,
    user_routes,
    login_routes,
    chat_routes
)

# Importa los modelos para que se creen las tablas
from models import directory, favorites, notes, role, user, referency

app = FastAPI()

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Incluye las rutas de la aplicación
app.include_router(directory_routes.router)
app.include_router(favorites_routes.router)
app.include_router(notes_routes.router)
app.include_router(publications_routes.router)
app.include_router(role_routes.router)
app.include_router(user_routes.router)
app.include_router(referency_router.router)
app.include_router(login_routes.router)
app.include_router(chat_routes.router, prefix="/chat", tags=["chat"])

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a FastAPI con PostgreSQL!"}
