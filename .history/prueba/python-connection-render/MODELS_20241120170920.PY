from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Usuario(nombre={self.nombre}, email={self.email})>'

class Transaccion(Base):
    __tablename__ = 'transacciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    monto = Column(Float, nullable=False)
    fecha_transaccion = Column(DateTime, default=datetime.datetime.utcnow)
    tipo_transaccion = Column(String, nullable=False)

    usuario = relationship('Usuario', back_populates='transacciones')

    def __repr__(self):
        return f'<Transaccion(usuario_id={self.usuario_id}, monto={self.monto})>'

Usuario.transacciones = relationship('Transaccion', order_by=Transaccion.id, back_populates='usuario')
