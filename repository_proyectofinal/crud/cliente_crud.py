import re
import customtkinter as ctk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Cliente

# Funciones CRUD fuera de la clase GestionClientes
def crear_cliente(db: Session, nombre: str, correo_electronico: str):
    # Verificar si el nombre o correo ya existen en la base de datos
    cliente_existente_nombre = db.query(Cliente).filter(Cliente.nombre == nombre).first()
    if cliente_existente_nombre:
        raise ValueError("El nombre ya está registrado.")
    
    cliente_existente_correo = db.query(Cliente).filter(Cliente.correo_electronico == correo_electronico).first()
    if cliente_existente_correo:
        raise ValueError("El correo electrónico ya está registrado.")
    
    # Crear el nuevo cliente si no existe duplicado
    nuevo_cliente = Cliente(nombre=nombre, correo_electronico=correo_electronico)
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

def obtener_todos_clientes(db: Session):
    return db.query(Cliente).all()

def actualizar_cliente(db: Session, cliente_id: int, nombre: str = None, correo_electronico: str = None):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise ValueError("Cliente no encontrado.")
    
    # Verificar si el nombre o correo son únicos antes de actualizarlos
    if nombre and nombre != cliente.nombre:
        cliente_existente_nombre = db.query(Cliente).filter(Cliente.nombre == nombre).first()
        if cliente_existente_nombre:
            raise ValueError("El nombre ya está registrado.")
        cliente.nombre = nombre
    
    if correo_electronico and correo_electronico != cliente.correo_electronico:
        cliente_existente_correo = db.query(Cliente).filter(Cliente.correo_electronico == correo_electronico).first()
        if cliente_existente_correo:
            raise ValueError("El correo electrónico ya está registrado.")
        cliente.correo_electronico = correo_electronico

    db.commit()
    db.refresh(cliente)
    return cliente

def eliminar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise ValueError("Cliente no encontrado.")
    
    db.delete(cliente)
    db.commit()
    return True

# Función para validar el formato de correo electrónico
def es_correo_valido(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo) is not None

# Clase para la interfaz gráfica de gestión de clientes
class GestionClientes(ctk.CTkFrame):
    def __init__(self, master, crear_cliente, obtener_todos_clientes, actualizar_cliente, eliminar_cliente, **kwargs):
        super().__init__(master, **kwargs)
        self.db: Session = SessionLocal()
        self.create_widgets()
        self.crear_cliente = crear_cliente
        self.obtener_todos_clientes = obtener_todos_clientes
        self.actualizar_cliente = actualizar_cliente
        self.eliminar_cliente = eliminar_cliente
        self.cargar_clientes()

    def create_widgets(self):
        # Frame para los campos de entrada
        self.frame_entrada = ctk.CTkFrame(self)
        self.frame_entrada.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Campos de entrada
        self.label_nombre = ctk.CTkLabel(self.frame_entrada, text="Nombre:")
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_nombre = ctk.CTkEntry(self.frame_entrada)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.label_correo = ctk.CTkLabel(self.frame_entrada, text="Correo Electrónico:")
        self.label_correo.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_correo = ctk.CTkEntry(self.frame_entrada)
        self.entry_correo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Frame para los botones
        self.frame_botones = ctk.CTkFrame(self)
        self.frame_botones.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Botones
        self.boton_crear = ctk.CTkButton(self.frame_botones, text="Crear Cliente", command=self.crear_cliente_gui)
        self.boton_crear.grid(row=0, column=0, padx=10, pady=10)

        self.boton_actualizar = ctk.CTkButton(self.frame_botones, text="Actualizar Cliente", command=self.actualizar_cliente_gui)
        self.boton_actualizar.grid(row=0, column=1, padx=10, pady=10)

        self.boton_eliminar = ctk.CTkButton(self.frame_botones, text="Eliminar Cliente", command=self.eliminar_cliente_gui)
        self.boton_eliminar.grid(row=0, column=2, padx=10, pady=10)

        # Treeview para mostrar los clientes
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # Crear el Treeview sin barra de desplazamiento
        self.tree = ttk.Treeview(self.tree_frame, columns=("Nombre", "Correo Electrónico"), show="headings", height=20)
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # El Treeview se expande en todo el espacio disponible
        self.tree.heading("Nombre", text="Nombre", anchor="w")
        self.tree.heading("Correo Electrónico", text="Correo Electrónico", anchor="w")

        # Ajustar el ancho de las columnas
        self.tree.column("Nombre", width=300)  # Aumenta el ancho de la columna Nombre
        self.tree.column("Correo Electrónico", width=350)  # Aumenta el ancho de la columna Correo Electrónico

        # Aseguramos que las filas y columnas se expanda adecuadamente
        self.grid_rowconfigure(0, weight=1)  # Hace que la primera fila (campos de entrada) se expanda
        self.grid_rowconfigure(1, weight=0)  # La segunda fila (botones) no se expande
        self.grid_rowconfigure(2, weight=1)  # La tercera fila (Treeview) se expande
        self.grid_columnconfigure(0, weight=1)  # La columna 0 (principal) se expande para ocupar todo el espacio

        # Configuración de expansión para el Treeview y su contenedor
        self.tree_frame.grid_rowconfigure(0, weight=1)  # El frame del Treeview se expande
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Agregar la función de selección de cliente en el Treeview
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def cargar_clientes(self):
        # Limpiar el Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Obtener los clientes de la base de datos
        clientes = self.obtener_todos_clientes(self.db)
        for cliente in clientes:
            self.tree.insert("", "end", values=(cliente.nombre, cliente.correo_electronico), iid=str(cliente.id))

    def crear_cliente_gui(self):
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()

        # Validación de nombre
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        # Validación de correo electrónico
        if not correo:
            messagebox.showerror("Error", "El correo electrónico no puede estar vacío.")
            return
        if not es_correo_valido(correo):
            messagebox.showerror("Error", "El correo electrónico no tiene un formato válido.")
            return

        try:
            self.crear_cliente(self.db, nombre, correo)
            messagebox.showinfo("Éxito", "Cliente creado exitosamente.")
            self.cargar_clientes()
            self.limpiar_campos()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def actualizar_cliente_gui(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, selecciona un cliente para actualizar.")
            return

        cliente_id = int(seleccion[0])
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()

        # Validación de nombre
        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return

        # Validación de correo electrónico
        if not correo:
            messagebox.showerror("Error", "El correo electrónico no puede estar vacío.")
            return
        if not es_correo_valido(correo):
            messagebox.showerror("Error", "El correo electrónico no tiene un formato válido.")
            return

        try:
            self.actualizar_cliente(self.db, cliente_id, nombre, correo)
            messagebox.showinfo("Éxito", "Cliente actualizado exitosamente.")
            self.cargar_clientes()
            self.limpiar_campos()
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def eliminar_cliente_gui(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, selecciona un cliente para eliminar.")
            return

        cliente_id = int(seleccion[0])
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este cliente?")
        if confirm:
            try:
                self.eliminar_cliente(self.db, cliente_id)
                messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
                self.cargar_clientes()
                self.limpiar_campos()
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))

    def on_treeview_select(self, event):
        seleccion = self.tree.selection()  # Obtener la selección actual
        if seleccion:  # Si se ha seleccionado un elemento
            cliente_id = int(seleccion[0])  # Convertir el iid de la selección a entero (el id del cliente)
            
            # Obtener el cliente desde la base de datos usando el cliente_id
            cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
            
            if cliente:  # Si se encontró el cliente
                # Llenar los campos con la información del cliente
                self.entry_nombre.delete(0, ctk.END)
                self.entry_nombre.insert(0, cliente.nombre)
                self.entry_correo.delete(0, ctk.END)
                self.entry_correo.insert(0, cliente.correo_electronico)

    def limpiar_campos(self):
        self.entry_nombre.delete(0, ctk.END)
        self.entry_correo.delete(0, ctk.END)
