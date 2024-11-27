from sqlalchemy.orm import Session
from models import Menu, Ingrediente

def crear_menu(db: Session, nombre: str, descripcion: str, ingredientes: list[dict]):
    """
    Crear un menú con una lista de ingredientes.
    :param db: Sesión de base de datos.
    :param nombre: Nombre del menú.
    :param descripcion: Descripción del menú.
    :param ingredientes: Lista de diccionarios {'id': id_ingrediente, 'cantidad': cantidad}.
    """
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
        nuevo_menu.ingredientes.append(ingrediente)
        db.execute(
            f"UPDATE menu_ingrediente SET cantidad = {ing['cantidad']} WHERE menu_id = {nuevo_menu.id} AND ingrediente_id = {ingrediente.id}"
        )

    db.commit()
    return nuevo_menu

def obtener_todos_menus(db: Session):
    """
    Obtener todos los menús registrados.
    :param db: Sesión de base de datos.
    """
    return db.query(Menu).all()

def actualizar_menu(db: Session, menu_id: int, nombre: str = None, descripcion: str = None, ingredientes: list[dict] = None):
    """
    Actualizar un menú existente.
    :param db: Sesión de base de datos.
    :param menu_id: ID del menú.
    :param nombre: Nuevo nombre (opcional).
    :param descripcion: Nueva descripción (opcional).
    :param ingredientes: Nueva lista de ingredientes (opcional).
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise ValueError("Menú no encontrado.")

    if nombre:
        menu.nombre = nombre
    if descripcion:
        menu.descripcion = descripcion

    if ingredientes is not None:
        menu.ingredientes.clear()
        for ing in ingredientes:
            ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ing['id']).first()
            if not ingrediente:
                raise ValueError(f"Ingrediente con id {ing['id']} no encontrado.")
            menu.ingredientes.append(ingrediente)
            db.execute(
                f"UPDATE menu_ingrediente SET cantidad = {ing['cantidad']} WHERE menu_id = {menu.id} AND ingrediente_id = {ingrediente.id}"
            )

    db.commit()
    return menu

def eliminar_menu(db: Session, menu_id: int):
    """
    Eliminar un menú.
    :param db: Sesión de base de datos.
    :param menu_id: ID del menú.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise ValueError("Menú no encontrado.")
    
    db.delete(menu)
    db.commit()
