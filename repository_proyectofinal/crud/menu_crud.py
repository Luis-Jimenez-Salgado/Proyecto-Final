class Menu:
    def __init__(self, nombre, descripcion, ingredientes):
        """
        Clase para representar un menú.
        :param nombre: Nombre del menú.
        :param descripcion: Descripción del menú.
        :param ingredientes: Diccionario de ingredientes {nombre: cantidad}.
        """
        self.nombre = nombre.upper()
        self.descripcion = descripcion
        self.ingredientes = ingredientes  # Diccionario de {ingrediente: cantidad}

    def __str__(self):
        ingredientes_str = ", ".join([f"{ing}: {cant}" for ing, cant in self.ingredientes.items()])
        return f"Menú: {self.nombre} - {self.descripcion} (Ingredientes: {ingredientes_str})"


class CrudMenu:
    def __init__(self):
        """
        Clase para gestionar el CRUD de menús.
        """
        self.menus = []

    def crear_menu(self, nombre, descripcion, ingredientes):
        if not ingredientes or len(ingredientes) == 0:
            raise ValueError("El menú debe tener al menos un ingrediente.")

        nuevo_menu = Menu(nombre, descripcion, ingredientes)
        self.menus.append(nuevo_menu)
        return nuevo_menu

    def leer_menus(self):
        return self.menus

    def actualizar_menu(self, nombre_menu, nueva_descripcion=None, nuevos_ingredientes=None):
        for menu in self.menus:
            if menu.nombre == nombre_menu.upper():
                if nueva_descripcion:
                    menu.descripcion = nueva_descripcion
                if nuevos_ingredientes:
                    if not nuevos_ingredientes or len(nuevos_ingredientes) == 0:
                        raise ValueError("El menú debe tener al menos un ingrediente.")
                    menu.ingredientes = nuevos_ingredientes
                return menu
        raise ValueError(f"No se encontró un menú con el nombre {nombre_menu}.")

    def eliminar_menu(self, nombre_menu):
        for menu in self.menus:
            if menu.nombre == nombre_menu.upper():
                self.menus.remove(menu)
                return True
        raise ValueError(f"No se encontró un menú con el nombre {nombre_menu}.")


# Integración en la aplicación principal
class AplicacionBodega(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Menús")
        self.geometry("1200x700")

        self.Ingredientes = Bodega()
        self.ListaEspecifica = ListaEspecifica()
        self.CrudMenu = CrudMenu()

        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()

    def configurar_pestana3(self):
        """
        Configuración de la pestaña de CRUD de Menús.
        """
        frame_formulario = ctk.CTkFrame(self.tab3)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_lista_menus = ctk.CTkFrame(self.tab3)
        frame_lista_menus.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario para crear un menú
        label_nombre_menu = ctk.CTkLabel(frame_formulario, text="Nombre del Menú:")
        label_nombre_menu.pack(pady=5)
        self.entry_nombre_menu = ctk.CTkEntry(frame_formulario)
        self.entry_nombre_menu.pack(pady=5)

        label_descripcion_menu = ctk.CTkLabel(frame_formulario, text="Descripción del Menú:")
        label_descripcion_menu.pack(pady=5)
        self.entry_descripcion_menu = ctk.CTkEntry(frame_formulario)
        self.entry_descripcion_menu.pack(pady=5)

        label_ingredientes_menu = ctk.CTkLabel(frame_formulario, text="Ingredientes (nombre: cantidad):")
        label_ingredientes_menu.pack(pady=5)
        self.entry_ingredientes_menu = ctk.CTkEntry(frame_formulario)
        self.entry_ingredientes_menu.pack(pady=5)

        self.boton_crear_menu = ctk.CTkButton(frame_formulario, text="Crear Menú", command=self.crear_menu)
        self.boton_crear_menu.pack(pady=10)

        # Lista de menús
        self.tree_menus = ttk.Treeview(frame_lista_menus, columns=("Nombre", "Descripción", "Ingredientes"), show="headings")
        self.tree_menus.heading("Nombre", text="Nombre")
        self.tree_menus.heading("Descripción", text="Descripción")
        self.tree_menus.heading("Ingredientes", text="Ingredientes")
        self.tree_menus.pack(expand=True, fill="both", padx=10, pady=10)

        self.boton_eliminar_menu = ctk.CTkButton(frame_lista_menus, text="Eliminar Menú", command=self.eliminar_menu)
        self.boton_eliminar_menu.pack(pady=10)

    def crear_menu(self):
        nombre = self.entry_nombre_menu.get()
        descripcion = self.entry_descripcion_menu.get()
        ingredientes_str = self.entry_ingredientes_menu.get()

        try:
            ingredientes = {}
            for item in ingredientes_str.split(","):
                nombre_ing, cantidad = item.split(":")
                ingredientes[nombre_ing.strip().upper()] = int(cantidad.strip())

            nuevo_menu = self.CrudMenu.crear_menu(nombre, descripcion, ingredientes)
            self.actualizar_lista_menus()
            messagebox.showinfo("Menú Creado", f"Menú '{nuevo_menu.nombre}' creado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_menu(self):
        seleccion = self.tree_menus.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Por favor selecciona un menú para eliminar.")
            return

        item = self.tree_menus.item(seleccion)
        nombre_menu = item['values'][0]

        try:
            self.CrudMenu.eliminar_menu(nombre_menu)
            self.actualizar_lista_menus()
            messagebox.showinfo("Menú Eliminado", f"Menú '{nombre_menu}' eliminado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_lista_menus(self):
        for item in self.tree_menus.get_children():
            self.tree_menus.delete(item)

        for menu in self.CrudMenu.leer_menus():
            ingredientes_str = ", ".join([f"{ing}: {cant}" for ing, cant in menu.ingredientes.items()])
            self.tree_menus.insert("", "end", values=(menu.nombre, menu.descripcion, ingredientes_str))
