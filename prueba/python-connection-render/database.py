from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from models import Base, Usuario, Transaccion, Vehiculo, Wallet

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
# Ejemplo de URL para Render:
# postgresql://user:password@host:5432/database_name

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una sesión local para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase base para los modelos de SQLAlchemy
Base = declarative_base()

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