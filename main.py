from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db.database import engine, Base, SessionLocal
from routes import (
    directory_routes,
    favorites_routes,
    notes_routes,
    publications_routes,
    role_routes,
    user_routes
)

# Importa los modelos para que se puedan crear las tablas
from models import directory, favorites, LoginRequest, LoginResponse, notes, publications, role, user

app = FastAPI()

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()

# Incluye las rutas de la aplicación (sin login_routes)
app.include_router(directory_routes.router)
app.include_router(favorites_routes.router)
app.include_router(notes_routes.router)
app.include_router(publications_routes.router)
app.include_router(role_routes.router)
app.include_router(user_routes.router) 


# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a FastAPI con PostgreSQL!"}
