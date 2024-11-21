from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import database
from database import init_db, get_db, drop_tables
from models import Usuario, Transaccion, Vehiculo, Wallet
from pydantic import BaseModel
import logging
from typing import List
import datetime

# Configurar el registro de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Evento de inicio de la aplicación para inicializar la base de datos e insertar datos iniciales
@app.on_event("startup")
def on_startup():
    logger.info("Initializing database")
    drop_tables()  # Eliminar las tablas existentes
    init_db()  # Crear las tablas nuevamente
    insert_initial_data()

# Función para insertar datos iniciales en las tablas
def insert_initial_data():
    db = database.SessionLocal()
    try:
        logger.info("Inserting initial data")
        
        # Insertar datos en la tabla Usuario
        user1 = Usuario(ci=1, nombre="Alice", email="alice@example.com", clave="password123")
        user2 = Usuario(ci=2, nombre="Bob", email="bob@example.com", clave="password123")
        db.add(user1)
        db.add(user2)
        
        # Insertar datos en la tabla Transaccion
        trans1 = Transaccion(usuario_ci=1, monto=100.0)
        trans2 = Transaccion(usuario_ci=2, monto=200.0)
        db.add(trans1)
        db.add(trans2)
        
        # Insertar datos en la tabla Vehiculo
        veh1 = Vehiculo(placa="ABC123", usuario_ci=1, year=2020, marca="Toyota")
        veh2 = Vehiculo(placa="XYZ789", usuario_ci=2, year=2019, marca="Honda")
        db.add(veh1)
        db.add(veh2)
        
        # Insertar datos en la tabla Wallet
        wallet1 = Wallet(usuario_ci=1, balance=1000.0)
        wallet2 = Wallet(usuario_ci=2, balance=2000.0)
        db.add(wallet1)
        db.add(wallet2)
        
        db.commit()
        logger.info("Initial data inserted")
    except Exception as e:
        logger.error(f"Error inserting initial data: {e}")
    finally:
        db.close()

# Ruta para probar la conexión a la base de datos
@app.get("/test")
def test_db(db: Session = Depends(get_db)):
    try:
        logger.info("Testing database connection")
        result = db.execute(text('SELECT * FROM usuario'))
        return {"message": "Conexión exitosa", "data": [dict(row) for row in result]}
    except Exception as e:
        logger.error(f"Error testing database connection: {e}")
        return {"error": str(e)}

# Ruta para listar todas las tablas en la base de datos
@app.get("/tables")
def list_tables(db: Session = Depends(get_db)):
    try:
        logger.info("Listing tables")
        result = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        tables = [row[0] for row in result]  # Accede al primer elemento de cada fila
        return {"tables": tables}
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        return {"error": str(e)}

# Modelo Pydantic para la creación de un nuevo usuario
class UsuarioCreate(BaseModel):
    ci: int
    nombre: str
    email: str
    clave: str

# Ruta para crear un nuevo usuario en la tabla Usuario
@app.post("/usuarios")
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating user: {usuario.nombre}, {usuario.email}")
        db_usuario = Usuario(ci=usuario.ci, nombre=usuario.nombre, email=usuario.email, clave=usuario.clave)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Ruta para obtener todos los usuarios de la tabla Usuario
@app.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all users")
        usuarios = db.query(Usuario).all()
        return usuarios
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return {"error": str(e)}

# Modelo Pydantic para la creación de una nueva transacción
class TransaccionCreate(BaseModel):
    usuario_ci: int
    monto: float

# Ruta para crear una nueva transacción en la tabla Transaccion
@app.post("/transacciones")
def create_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating transaction for user: {transaccion.usuario_ci}, amount: {transaccion.monto}")
        db_transaccion = Transaccion(usuario_ci=transaccion.usuario_ci, monto=transaccion.monto)
        db.add(db_transaccion)
        db.commit()
        db.refresh(db_transaccion)
        return db_transaccion
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Ruta para obtener todas las transacciones de la tabla Transaccion
@app.get("/transacciones")
def get_transacciones(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all transactions")
        transacciones = db.query(Transaccion).all()
        return transacciones
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        return {"error": str(e)}

# Modelo Pydantic para la creación de un nuevo vehículo
class VehiculoCreate(BaseModel):
    placa: str
    usuario_ci: int
    year: int
    marca: str

# Ruta para crear un nuevo vehículo en la tabla Vehiculo
@app.post("/vehiculos")
def create_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Creating vehicle: {vehiculo.placa}, user: {vehiculo.usuario_ci}")
        db_vehiculo = Vehiculo(placa=vehiculo.placa, usuario_ci=vehiculo.usuario_ci, year=vehiculo.year, marca=vehiculo.marca)
        db.add(db_vehiculo)
        db.commit()
        db.refresh(db_vehiculo)
        return db_vehiculo
    except Exception as e:
        logger.error(f"Error creating vehicle: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Ruta para obtener todos los vehículos de la tabla Vehiculo
@app.get("/vehiculos")
def get_vehiculos(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all vehicles")
        vehiculos = db.query(Vehiculo).all()
        return vehiculos
    except Exception as e:
        logger.error(f"Error fetching vehicles: {e}")
        return {"error": str(e)}

# Modelo Pydantic para la respuesta del Wallet
class WalletResponse(BaseModel):
    id: int
    balance: float

    class Config:
        orm_mode = True

# Modelo Pydantic para la respuesta del Usuario con Wallet
class UsuarioWithWalletResponse(BaseModel):
    ci: int
    nombre: str
    email: str
    ultima_vez_conectado: datetime.datetime
    wallets: List[WalletResponse]

    class Config:
        orm_mode = True

# Ruta para obtener un usuario con su wallet
@app.get("/usuarios/{ci}", response_model=UsuarioWithWalletResponse)
def get_usuario_with_wallet(ci: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching user with ci: {ci}")
        usuario = db.query(Usuario).filter(Usuario.ci == ci).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except Exception as e:
        logger.error(f"Error fetching user with wallet: {e}")
        raise HTTPException(status_code=400, detail=str(e))