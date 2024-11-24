import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


class MenuItem:
    def __init__(self, nombre, descripcion, ingredientes):
        self.nombre = nombre
        self.descripcion = descripcion
        self.ingredientes = ingredientes  # Diccionario {ingrediente: cantidad}


class MenuSystem:
    def __init__(self):
        self.menus = []  # Lista de menús

    def agregar_menu(self, menu):
        self.menus.append(menu)

    def eliminar_menu(self, index):
        if 0 <= index < len(self.menus):
            del self.menus[index]
            return True
        return False

    def obtener_menus(self):
        return self.menus


class AplicacionMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Menús")
        self.geometry("800x600")

        self.menu_system = MenuSystem()

        self.crear_pantalla()

    def crear_pantalla(self):
        # Frame de entrada
        frame_formulario = ctk.CTkFrame(self)
        frame_formulario.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(frame_formulario, text="Nombre del Menú:").pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Descripción:").pack(pady=5)
        self.entry_descripcion = ctk.CTkEntry(frame_formulario)
        self.entry_descripcion.pack(pady=5)

        ctk.CTkLabel(frame_formulario, text="Ingredientes (nombre:cantidad separados por comas):").pack(pady=5)
        self.entry_ingredientes = ctk.CTkEntry(frame_formulario)
        self.entry_ingredientes.pack(pady=5)

        ctk.CTkButton(frame_formulario, text="Agregar Menú", command=self.agregar_menu).pack(pady=10)
        ctk.CTkButton(frame_formulario, text="Eliminar Menú", command=self.eliminar_menu).pack(pady=10)

        # Frame de lista
        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_lista, columns=("Nombre", "Descripción", "Ingredientes"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Ingredientes", text="Ingredientes")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.actualizar_lista()

    def agregar_menu(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        ingredientes_texto = self.entry_ingredientes.get()

        if not nombre or not descripcion or not ingredientes_texto:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        try:
            ingredientes = {
                item.split(":")[0].strip(): int(item.split(":")[1].strip())
                for item in ingredientes_texto.split(",")
            }
        except ValueError:
            messagebox.showwarning("Error", "Los ingredientes deben tener el formato nombre:cantidad.")
            return

        nuevo_menu = MenuItem(nombre, descripcion, ingredientes)
        self.menu_system.agregar_menu(nuevo_menu)
        self.actualizar_lista()
        self.limpiar_campos()

    def eliminar_menu(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Selecciona un menú para eliminar.")
            return

        index = self.tree.index(seleccion[0])
        if self.menu_system.eliminar_menu(index):
            self.actualizar_lista()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el menú.")

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for menu in self.menu_system.obtener_menus():
            ingredientes_str = ", ".join([f"{k}:{v}" for k, v in menu.ingredientes.items()])
            self.tree.insert("", "end", values=(menu.nombre, menu.descripcion, ingredientes_str))

    def limpiar_campos(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_descripcion.delete(0, 'end')
        self.entry_ingredientes.delete(0, 'end')


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AplicacionMenu()
    app.mainloop()
