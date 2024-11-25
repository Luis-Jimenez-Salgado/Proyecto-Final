from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Cliente(nombre='{self.nombre}', correo_electronico='{self.correo_electronico}')>"

class Ingrediente(Base):
    __tablename__ = 'ingredientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=False, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(float, nullable=False)
    unidad = Column(String, nullable=False)
 