import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk #este es la unica "libreria" que encontre para poder asignarle imagenes a los botones
import random 
import re
from fpdf import FPDF  # Importar la librería fpdf para generar el PDF

class Ingrediente:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre.upper()  # Convertir nombre a mayúsculas
        self.cantidad = int(cantidad)  # Convertir cantidad a entero

    def __str__(self):
        return f"{self.nombre} , Cantidad: {self.cantidad}"

class Bodega:
    def __init__(self):
        self.lista_ing = []

    def agregar_ING(self, ingrediente):
        for i in self.lista_ing:
            if i.nombre == ingrediente.nombre:
                i.cantidad += ingrediente.cantidad
                return True
        self.lista_ing.append(ingrediente)
        return True  

    def eliminar_ING(self, nombre_ing, cantidad):
        nombre_ing = nombre_ing.upper()
        for lis in self.lista_ing:
            if lis.nombre == nombre_ing:
                if lis.cantidad >= cantidad:
                    lis.cantidad -= cantidad
                    if lis.cantidad == 0:
                        self.lista_ing.remove(lis)
                    return True
                else:
                    return False
        return False

    def obtener_ING(self):
        return self.lista_ing

class ListaEspecifica:
    def __init__(self):
        self.lista_unica = []

    def agregar_elemento(self, ingrediente, cantidad, precio):
        for item in self.lista_unica:
            if item["ingrediente"] == ingrediente:
                item["cantidad"] += cantidad
                return True
        self.lista_unica.append({"ingrediente": ingrediente, "cantidad": cantidad, "precio": precio})
        return True

    def eliminar_elemento(self, index):
        if 0 <= index < len(self.lista_unica):
            del self.lista_unica[index]
            return True
        return False

    def obtener_lista(self):
        return self.lista_unica

class AplicacionBodega(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("bodega")
        self.geometry("1200x700")

        self.Ingredientes = Bodega()
        self.ListaEspecifica = ListaEspecifica()

        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()

    def crear_pestanas(self):
        self.tab1 = self.tabview.add("Ingreso de Ingredientes")
        self.tab2 = self.tabview.add("Lista de Menú")

        self.configurar_pestana1()
        self.configurar_pestana2()

    def configurar_pestana1(self):
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad:")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente", command=self.ingresar_ING)
        self.boton_ingresar.pack(pady=10)

        self.boton_actualizar = ctk.CTkButton(frame_formulario, text="Generar Menú", command=self.actualizar_botones)
        self.boton_actualizar.pack(pady=10)

        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", command=self.eliminar_ING)
        self.boton_eliminar.pack(pady=10)

        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Cantidad"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.actualizar_treeview_pestana1()

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    # Cargar y redimensionar las imágenes
        img_papas_fritas = Image.open("icono_papas_fritas_64x64.png").resize((64, 64))
        img_completo = Image.open("icono_hotdog_sin_texto_64x64.png").resize((64, 64))
        img_hamburguesa = Image.open("icono_hamburguesa_negra_64x64.png").resize((64, 64))
        img_pepsi = Image.open("icono_cola_64x64.png").resize((64, 64))

    # Convertir las imágenes a formato compatible con tkinter
        img_papas_fritas_tk = ImageTk.PhotoImage(img_papas_fritas)
        img_completo_tk = ImageTk.PhotoImage(img_completo)
        img_hamburguesa_tk = ImageTk.PhotoImage(img_hamburguesa)
        img_pepsi_tk = ImageTk.PhotoImage(img_pepsi)

    # Función para crear un botón con imagen y texto
        def boton_con_imagen_texto(frame, imagen, texto, comando):
            boton = ctk.CTkButton(frame, text=texto, image=imagen, compound="top", command=comando)
            boton.pack(side="left", padx=5, pady=5)

            return boton

    # Crear los botones con imagen y texto
        self.boton_papas_fritas = boton_con_imagen_texto(frame_superior, img_papas_fritas_tk, "Papas Fritas", lambda: self.agregar_producto('Papas Fritas'))
        self.boton_completo = boton_con_imagen_texto(frame_superior, img_completo_tk, "Completo", lambda: self.agregar_producto('Completo'))
        self.boton_hamburguesa = boton_con_imagen_texto(frame_superior, img_hamburguesa_tk, "Hamburguesa", lambda: self.agregar_producto('Hamburguesa'))
        self.boton_pepsi = boton_con_imagen_texto(frame_superior, img_pepsi_tk, "Pepsi", lambda: self.agregar_producto('Pepsi'))

    # Mantener referencias a las imágenes para evitar que sean recolectadas por el recolector de basura
        self.img_papas_fritas_tk = img_papas_fritas_tk
        self.img_completo_tk = img_completo_tk
        self.img_hamburguesa_tk = img_hamburguesa_tk
        self.img_pepsi_tk = img_pepsi_tk

        self.boton_eliminar_menu = ctk.CTkButton(frame_inferior, text="Eliminar Menú", command=self.eliminar_menu)
        self.boton_eliminar_menu.pack(pady=10)

        self.tree_lista = ttk.Treeview(frame_inferior, columns=("Producto", "Cantidad", "Precio"), show="headings")
        self.tree_lista.heading("Producto", text="Producto")
        self.tree_lista.heading("Cantidad", text="Cantidad")
        self.tree_lista.heading("Precio", text="Precio")
        self.tree_lista.pack(expand=True, fill="both", padx=10, pady=10)

        self.label_total = ctk.CTkLabel(frame_inferior, text="Total: $0")
        self.label_total.pack(side="right", padx=10, pady=10)

        self.boton_generar_boleta = ctk.CTkButton(frame_inferior, text="Generar Boleta", command=self.generar_boleta)  # Botón para generar el PDF
        self.boton_generar_boleta.pack(side="left", padx=5, pady=5)

        self.actualizar_treeview_pestana2()

    def validar_nombre(self, nombre):
    # Elimina los espacios al inicio y al final
        nombre = nombre.strip()
    
    # Verifica que el nombre no esté vacío y contenga al menos una letra
        if nombre and re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            messagebox.showwarning("Error de Validación", "El nombre debe al menos una letra.")
            return False

    def validar_cantidad(self, cantidad):
        if cantidad.isdigit() and int(cantidad) > 0:
            return True
        else:
            messagebox.showwarning("Error de Validación", "La cantidad debe ser un número entero positivo.")
            return False

    def ingresar_ING(self):
        nombre = self.entry_nombre.get().upper()
        cantidad = self.entry_cantidad.get()

        if not self.validar_nombre(nombre) or not self.validar_cantidad(cantidad):
            return

        ING = Ingrediente(nombre, cantidad)

        if self.Ingredientes.agregar_ING(ING):
            self.actualizar_treeview_pestana1()
            self.limpiar_campos()
            self.actualizar_botones()
        else:
            messagebox.showwarning("Error", "El Ingrediente ya existe en la bodega.")

    def eliminar_ING(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Por favor selecciona un Ingrediente para eliminar.")
            return

        item = self.tree.item(seleccion)
        nombre = item['values'][0]
        cantidad = item['values'][1]

        if self.Ingredientes.eliminar_ING(nombre, int(cantidad)):
            self.actualizar_treeview_pestana1()
            self.actualizar_botones()
        else:
            messagebox.showwarning("Error", "El Ingrediente no se pudo eliminar.")

    def agregar_producto(self, producto):
        ingredientes_requeridos = {
            'PAPAS FRITAS': {'PAPAS': 5},
            'COMPLETO': {'PAN DE COMPLETO': 1, 'VIANESA': 1, 'PALTA': 1, 'TOMATE': 1},
            'HAMBURGUESA': {'PAN DE HAMBURGUESA': 1, 'CHURRASCO DE CARNE': 1, 'LAMINA DE QUESO': 1},
            'PEPSI': {'BEBIDA': 1}
        }

        precios = {
            'PAPAS FRITAS': 500,
            'COMPLETO': 1800,
            'HAMBURGUESA': 3500,
            'PEPSI': 1100
        }

        requisitos = ingredientes_requeridos.get(producto.upper(), {})
        if not all(self.check_ingredientes({nombre: cantidad}) for nombre, cantidad in requisitos.items()):
            messagebox.showwarning("Error", f"No hay suficientes ingredientes para {producto}.")
            return

        precio = precios.get(producto.upper(), 0)
        self.ListaEspecifica.agregar_elemento(producto.upper(), 1, precio)

        for nombre, cantidad in requisitos.items():
            self.Ingredientes.eliminar_ING(nombre, cantidad)

        self.actualizar_treeview_pestana2()
        self.actualizar_total()
        self.actualizar_botones()

    def actualizar_treeview_pestana1(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for ing in self.Ingredientes.obtener_ING():
            self.tree.insert("", "end", values=(ing.nombre, ing.cantidad))

    def actualizar_treeview_pestana2(self):
        for item in self.tree_lista.get_children():
            self.tree_lista.delete(item)

        for item in self.ListaEspecifica.obtener_lista():
            self.tree_lista.insert("", "end", values=(item["ingrediente"], item["cantidad"], item["precio"]))

    def eliminar_menu(self):
        seleccion = self.tree_lista.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Por favor selecciona un producto para eliminar.")
            return

        item = self.tree_lista.item(seleccion)
        producto = item['values'][0]
        index = next((i for i, e in enumerate(self.ListaEspecifica.obtener_lista()) if e["ingrediente"] == producto), None)

        if index is not None:
            if self.ListaEspecifica.eliminar_elemento(index):
                self.actualizar_treeview_pestana2()
                self.actualizar_total()
            else:
                messagebox.showwarning("Error", "No se pudo eliminar el producto.")
        else:
            messagebox.showwarning("Error", "Producto no encontrado en la lista.")

    def actualizar_total(self):
        total = sum(item["precio"] * item["cantidad"] for item in self.ListaEspecifica.obtener_lista())
        self.label_total.configure(text=f"Total: ${total}")

    def actualizar_botones(self):
        self.boton_papas_fritas.configure(state="normal" if self.check_ingredientes({'PAPAS': 5}) else "disabled")
        self.boton_completo.configure(state="normal" if self.check_ingredientes({'PAN DE COMPLETO': 1, 'VIANESA': 1, 'PALTA': 1, 'TOMATE': 1}) else "disabled")
        self.boton_hamburguesa.configure(state="normal" if self.check_ingredientes({'PAN DE HAMBURGUESA': 1, 'CHURRASCO DE CARNE': 1, 'LAMINA DE QUESO': 1}) else "disabled")
        self.boton_pepsi.configure(state="normal" if self.check_ingredientes({'BEBIDA': 1}) else "disabled")

    def check_ingredientes(self, requisitos):
        for nombre, cantidad in requisitos.items():
            ingrediente = next((i for i in self.Ingredientes.obtener_ING() if i.nombre == nombre), None)
            if not ingrediente or ingrediente.cantidad < cantidad:
                return False
        return True

    def limpiar_campos(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_cantidad.delete(0, 'end')

    def generar_boleta(self):
        try:
        # Crear PDF
            pdf = FPDF()
            pdf.add_page()

         # RUT falso, título, y número de boleta
            rut_falso = "99.999.999-9"
            numero_boleta = f"N°{random.randint(1, 999):03}"
            direccion_falsa = "Dirección Falsa 123"
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Encabezado de la boleta
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Boleta Electrónica", ln=True, align="C")
            pdf.ln(5)

            pdf.set_font("Arial", size=12)
            pdf.cell(100, 10, txt=f"RUT: {rut_falso}", ln=True)
            pdf.cell(100, 10, txt=f"{numero_boleta}", ln=True)
            pdf.cell(100, 10, txt=f"Dirección: {direccion_falsa}", ln=True)
            pdf.cell(100, 10, txt=f"Fecha de Emisión: {fecha_hora_actual}", ln=True)
            pdf.ln(10)

        # Encabezado de la tabla
            pdf.set_font("Arial", "B", 12)
            pdf.cell(50, 10, "Item", border=1, align="C")
            pdf.cell(40, 10, "P. Unitario", border=1, align="C")
            pdf.cell(30, 10, "Cantidad", border=1, align="C")
            pdf.cell(40, 10, "Total", border=1, align="C")
            pdf.ln()

            total_general = 0
            pdf.set_font("Arial", size=12)

            # Agregar los productos a la tabla
            for item in self.ListaEspecifica.obtener_lista():
                producto = item["ingrediente"]
                cantidad = item["cantidad"]
                precio_unitario = item["precio"]
                total_item = cantidad * precio_unitario

                pdf.cell(50, 10, producto, border=1)
                pdf.cell(40, 10, f"${precio_unitario}", border=1, align="R")
                pdf.cell(30, 10, str(cantidad), border=1, align="C")
                pdf.cell(40, 10, f"${total_item}", border=1, align="R")
                pdf.ln()

                total_general += total_item

        # Calcular IVA (19%)
            iva = int(total_general * 0.19)
            total_con_iva = total_general + iva

        # Espacio y totales
            pdf.ln(10)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(120, 10, "Total General", border=1, align="R")
            pdf.cell(40, 10, f"${total_general}", border=1, align="R")
            pdf.ln()
            pdf.cell(120, 10, "IVA (19%)", border=1, align="R")
            pdf.cell(40, 10, f"${iva}", border=1, align="R")
            pdf.ln()
            pdf.cell(120, 10, "Total con IVA", border=1, align="R")
            pdf.cell(40, 10, f"${total_con_iva}", border=1, align="R")

        # Guardar PDF
            pdf_file = "boleta_defi.pdf"
            pdf.output(pdf_file)

            messagebox.showinfo("Boleta Generada", f"Boleta guardada como {pdf_file}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la boleta: {str(e)}")



if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AplicacionBodega()
    app.mainloop()
