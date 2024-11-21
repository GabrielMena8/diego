from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'

    ci = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    clave = Column(String, nullable=False) 
    ultima_vez_conectado = Column(DateTime, default=datetime.datetime.utcnow)

    transacciones = relationship('Transaccion', order_by='Transaccion.id_transaccion', back_populates='usuario')
    vehiculos = relationship('Vehiculo', order_by='Vehiculo.placa', back_populates='usuario')
    wallets = relationship('Wallet', order_by='Wallet.id', back_populates='usuario')
    
    def __repr__(self):
        return f'<Usuario(nombre={self.nombre}, ci={self.ci}, email={self.email}, ultima_vez_conectado={self.ultima_conexion})>'

class Transaccion(Base):
    __tablename__ = 'transaccion'

    id_transaccion = Column(Integer, primary_key=True, autoincrement=True)
    usuario_ci = Column(Integer, ForeignKey('usuario.ci'))
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)

    usuario = relationship('Usuario', back_populates='transaccion')

    def __repr__(self):
        return f'<Transaccion(usuario_ci={self.usuario_ci}, monto={self.monto})>'


class Vehiculo(Base):
    __tablename__ = 'vehiculo'

    placa = Column(String, primary_key=True)  # Placa como clave primaria
    usuario_ci = Column(String, ForeignKey('usuario.ci'), nullable=False)  # Relación con Usuario usando ci como clave foránea
    year = Column(Integer, nullable=False)  # Año del vehículo
    marca = Column(String, nullable=False)  # Marca del vehículo
    nombre_dueno = Column(String, nullable=False)  # Nombre del dueño

    usuario = relationship('Usuario', back_populates='vehiculos')

    def __repr__(self):
        return f'<Vehiculo(placa={self.placa}, anio={self.anio}, marca={self.marca}, nombre_dueno={self.nombre_dueno})>'

# Actualizamos la relación en el modelo Usuario
Usuario.vehiculos = relationship('Vehiculo', order_by=Vehiculo.placa, back_populates='usuario')

class Wallet(Base):
    __tablename__='wallet'

    id = Column(Integer, primary_key=True, autoincrement=True) # ID como clave primaria 
    usuario_ci = Column(String, ForeignKey('usuarios.ci'), nullable=False) # Relación con Usuario usando ci como clave foránea 
    saldo = Column(Float, nullable=False) # Saldo actual 
    usuario = relationship('Usuario', back_populates='wallets')
    codigo_qr = Column(String, unique=True, nullable=True)
    
    def __repr__(self): return f'<Wallet(id={self.id}, usuario_ci={self.usuario_ci}, saldo={self.saldo})>'
