from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

# Crear una instancia de la clase base para los modelos de SQLAlchemy
Base = declarative_base()

# Definir el modelo de la tabla Usuario
class Usuario(Base):
    __tablename__ = 'usuario'

    # Definir las columnas de la tabla Usuario
    ci = Column(Integer, primary_key=True)  # Clave primaria
    nombre = Column(String, nullable=False)  # Nombre del usuario
    email = Column(String, nullable=False, unique=True)  # Email del usuario, debe ser único
    clave = Column(String, nullable=False)  # Clave del usuario
    ultima_vez_conectado = Column(DateTime, default=datetime.datetime.utcnow)  # Última vez que el usuario se conectó

    # Definir las relaciones con otras tablas
    transacciones = relationship('Transaccion', order_by='Transaccion.id_transaccion', back_populates='usuario')
    vehiculos = relationship('Vehiculo', order_by='Vehiculo.placa', back_populates='usuario')
    wallets = relationship('Wallet', order_by='Wallet.id', back_populates='usuario')
    
    def __repr__(self):
        return f'<Usuario(nombre={self.nombre}, ci={self.ci}, email={self.email}, ultima_vez_conectado={self.ultima_vez_conectado})>'

# Definir el modelo de la tabla Transaccion
class Transaccion(Base):
    __tablename__ = 'transaccion'

    # Definir las columnas de la tabla Transaccion
    id_transaccion = Column(Integer, primary_key=True, autoincrement=True)  # Clave primaria, autoincremental
    usuario_ci = Column(Integer, ForeignKey('usuario.ci'))  # Clave foránea que referencia a la tabla Usuario
    monto = Column(Float, nullable=False)  # Monto de la transacción
    fecha = Column(DateTime, default=datetime.datetime.utcnow)  # Fecha de la transacción

    # Definir la relación con la tabla Usuario
    usuario = relationship('Usuario', back_populates='transacciones')

    def __repr__(self):
        return f'<Transaccion(usuario_ci={self.usuario_ci}, monto={self.monto})>'

# Definir el modelo de la tabla Vehiculo
class Vehiculo(Base):
    __tablename__ = 'vehiculo'

    # Definir las columnas de la tabla Vehiculo
    placa = Column(String, primary_key=True)  # Placa como clave primaria
    usuario_ci = Column(Integer, ForeignKey('usuario.ci'), nullable=False)  # Clave foránea que referencia a la tabla Usuario
    year = Column(Integer, nullable=False)  # Año del vehículo
    marca = Column(String, nullable=False)  # Marca del vehículo

    # Definir la relación con la tabla Usuario
    usuario = relationship('Usuario', back_populates='vehiculos')

    def __repr__(self):
        return f'<Vehiculo(placa={self.placa}, usuario_ci={self.usuario_ci}, year={self.year}, marca={self.marca})>'

# Definir el modelo de la tabla Wallet
class Wallet(Base):
    __tablename__ = 'wallet'

    # Definir las columnas de la tabla Wallet
    id = Column(Integer, primary_key=True, autoincrement=True)  # Clave primaria, autoincremental
    usuario_ci = Column(Integer, ForeignKey('usuario.ci'), nullable=False)  # Clave foránea que referencia a la tabla Usuario
    balance = Column(Float, nullable=False)  # Balance de la wallet

    # Definir la relación con la tabla Usuario
    usuario = relationship('Usuario', back_populates='wallets')

    def __repr__(self):
        return f'<Wallet(usuario_ci={self.usuario_ci}, balance={self.balance})>'