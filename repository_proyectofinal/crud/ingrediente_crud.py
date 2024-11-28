from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from ..models import Ingrediente  # Asegúrate de tener modelos adecuados para Ingrediente 

class IngredienteCRUD:
    @staticmethod
    def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: float, unidad: str):
        """
        Crea un nuevo ingrediente si no existe uno con el mismo nombre y tipo.
        """
        try:
            # Validar unicidad por nombre y tipo
            ingrediente_existente = db.query(Ingrediente).filter_by(nombre=nombre, tipo=tipo).first()
            if ingrediente_existente:
                 # Si ya existe, sumamos la cantidad al ingrediente existente
                ingrediente_existente.cantidad += cantidad
                db.commit()
                db.refresh(ingrediente_existente)
                return ingrediente_existente  # Devolver el ingrediente actualizado
            
            nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
            db.add(nuevo_ingrediente)
            db.commit()
            db.refresh(nuevo_ingrediente)
            return nuevo_ingrediente
        
        except IntegrityError:
            db.rollback()
            raise ValueError("Error al guardar el ingrediente. Verifique los datos ingresados.")
        except Exception as e:
            db.rollback()
            raise ValueError(str(e))

    @staticmethod
    def leer_ingredientes(db: Session):
        """
        Devuelve todos los ingredientes con sus detalles:nombre, tipo, cantidad y unidad.
        """
        try:
            ingredientes = db.query(Ingrediente).all()
            # Visualización de ingredientes en un formato entendible
            return [
                {
                    'nombre': ingrediente.nombre,
                    'tipo': ingrediente.tipo,
                    'cantidad': ingrediente.cantidad,
                    'unidad': ingrediente.unidad
                }
                for ingrediente in ingredientes
            ]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al leer los ingredientes: {e}")

    @staticmethod
    def actualizar_ingrediente(db: Session, ingrediente_id: int, cantidad: float = None, tipo: str = None):
        """
        Actualiza la cantidad o el tipo de un ingrediente existente.
        """
        try:
            ingrediente = db.query(Ingrediente).filter_by(id=ingrediente_id).first()
            if not ingrediente:
                raise ValueError("El ingrediente no existe.")

            if cantidad is not None:
                ingrediente.cantidad = cantidad
            if tipo is not None:
                ingrediente.tipo = tipo

            db.commit()
            db.refresh(ingrediente)
            return ingrediente
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Error al actualizar el ingrediente: {e}")

    @staticmethod
    def eliminar_ingrediente(db: Session, ingrediente_id: int):
        """
        Elimina un ingrediente.
        """
        try:           
            ingrediente = db.query(Ingrediente).filter_by(id=ingrediente_id).first()
            if not ingrediente:
                
                raise ValueError("El ingrediente no existe.")
            db.delete(ingrediente)
            db.commit()
            return {"mensaje": "Ingrediente eliminado con éxito."}
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Error al eliminar el ingrediente: {e}")
