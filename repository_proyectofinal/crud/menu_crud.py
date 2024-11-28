from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from models import Menu, Ingrediente

class MenuCRUD:
    @staticmethod
    def crear_menu(db: Session, nombre: str, descripcion: str, ingredientes: list[dict]):
        """
        Crear un menú con una lista de ingredientes.
        :param db: Sesión de base de datos.
        :param nombre: Nombre del menú.
        :param descripcion: Descripción del menú.
        :param ingredientes: Lista de diccionarios {'id': id_ingrediente, 'cantidad': cantidad}.
        """
        try:
            # Verificar si el menú ya existe
            menu_existente = db.query(Menu).filter(Menu.nombre == nombre).first()
            if menu_existente:
                raise ValueError("El menú ya existe.")

            # Crear el menú
            nuevo_menu = Menu(nombre=nombre, descripcion=descripcion)
            db.add(nuevo_menu)
            db.commit()

            # Asociar ingredientes al menú
            for ing in ingredientes:
                ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ing['id']).first()
                if not ingrediente:
                    raise ValueError(f"Ingrediente con id {ing['id']} no encontrado.")

                # Verificar si la cantidad requerida está disponible
                if ingrediente.cantidad < ing['cantidad']:
                    raise ValueError(f"No hay suficiente cantidad del ingrediente {ingrediente.nombre}. Disponible: {ingrediente.cantidad}")

                # Descontar la cantidad utilizada del ingrediente
                ingrediente.cantidad -= ing['cantidad']
                db.commit()

                # Asociar el ingrediente al menú
                nuevo_menu.ingredientes.append(ingrediente)
                db.execute(
                    f"UPDATE menu_ingrediente SET cantidad = {ing['cantidad']} "
                    f"WHERE menu_id = {nuevo_menu.id} AND ingrediente_id = {ingrediente.id}"
                )

            db.commit()
            return nuevo_menu

        except IntegrityError:
            db.rollback()
            raise ValueError("Error de integridad al crear el menú.")
        except Exception as e:
            db.rollback()
            raise ValueError(str(e))

    @staticmethod
    def obtener_todos_menus(db: Session):
        """
        Obtener todos los menús registrados.
        :param db: Sesión de base de datos.
        """
        try:
            menus = db.query(Menu).all()
            return [
                {
                    "id": menu.id,
                    "nombre": menu.nombre,
                    "descripcion": menu.descripcion,
                    "ingredientes": [
                        {
                            "nombre": ing.nombre,
                            "tipo": ing.tipo,
                            "cantidad": ing.cantidad,
                            "unidad": ing.unidad,
                        }
                        for ing in menu.ingredientes
                    ],
                }
                for menu in menus
            ]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al obtener los menús: {e}")

    @staticmethod
    def actualizar_menu(db: Session, menu_id: int, nombre: str = None, descripcion: str = None, ingredientes: list[dict] = None):
        """
        Actualizar un menú existente.
        :param db: Sesión de base de datos.
        :param menu_id: ID del menú.
        :param nombre: Nuevo nombre (opcional).
        :param descripcion: Nueva descripción (opcional).
        :param ingredientes: Nueva lista de ingredientes (opcional).
        """
        try:
            menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not menu:
                raise ValueError("Menú no encontrado.")

            if nombre:
                menu.nombre = nombre
            if descripcion:
                menu.descripcion = descripcion

            if ingredientes is not None:
                # Restaurar la cantidad a los ingredientes originales
                for ing in menu.ingredientes:
                    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ing.id).first()
                    if ingrediente:
                        ingrediente.cantidad += ing.cantidad

                # Limpiar ingredientes actuales
                menu.ingredientes.clear()
                db.commit()

                # Añadir los nuevos ingredientes
                for ing in ingredientes:
                    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ing['id']).first()
                    if not ingrediente:
                        raise ValueError(f"Ingrediente con id {ing['id']} no encontrado.")

                    if ingrediente.cantidad < ing['cantidad']:
                        raise ValueError(f"No hay suficiente cantidad del ingrediente {ingrediente.nombre}. Disponible: {ingrediente.cantidad}")

                    ingrediente.cantidad -= ing['cantidad']
                    menu.ingredientes.append(ingrediente)

            db.commit()
            return menu

        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Error al actualizar el menú: {e}")

    @staticmethod
    def eliminar_menu(db: Session, menu_id: int):
        """
        Eliminar un menú.
        :param db: Sesión de base de datos.
        :param menu_id: ID del menú.
        """
        try:
            menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not menu:
                raise ValueError("Menú no encontrado.")

            # Restaurar la cantidad de los ingredientes
            for ing in menu.ingredientes:
                ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ing.id).first()
                if ingrediente:
                    ingrediente.cantidad += ing.cantidad

            db.delete(menu)
            db.commit()
            return {"mensaje": "Menú eliminado con éxito."}

        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Error al eliminar el menú: {e}")
