from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabla intermedia para la relación Menú-Ingrediente
menu_ingrediente = Table(
    'menu_ingrediente',
    Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
    Column('cantidad', Integer, nullable=False)  # Cantidad del ingrediente requerido
)

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255))
    ingredientes = relationship("Ingrediente", secondary=menu_ingrediente, back_populates="menus")

class Ingrediente(Base):
    __tablename__ = 'ingredientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    tipo = Column(String(50))  # Ejemplo: Vegetal, Proteína, etc.
    cantidad = Column(Integer, nullable=False)  # Cantidad disponible
    unidad = Column(String(20))  # Ejemplo: Unidades, Gramos, etc.
    menus = relationship("Menu", secondary=menu_ingrediente, back_populates="ingredientes")


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Cliente(nombre='{self.nombre}', correo_electronico='{self.correo_electronico}')>"
