from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import Base, Usuario, Transaccion, Vehiculo, Wallet

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Si usas Render, la URL será algo como:
# postgresql://user:password@host:5432/database_name

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para eliminar las tablas existentes
def drop_tables():
    Base.metadata.drop_all(bind=engine)

# Función para inicializar la base de datos y crear las tablas
def init_db():
    Base.metadata.create_all(bind=engine)