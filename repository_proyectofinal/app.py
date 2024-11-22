from crud.cliente_crud import GestionClientes, crear_cliente, obtener_todos_clientes, actualizar_cliente, eliminar_cliente
from database import init_db
import customtkinter as ctk

def main():
    # Inicializar la base de datos
    init_db()

    # Crear la ventana principal
    app = ctk.CTk()
    app.title("Sistema de Gestión de Clientes")
    app.geometry("600x600")  # Ajusta el tamaño de la ventana según sea necesario

    # Crear el frame principal
    frame = ctk.CTkFrame(app)
    frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Agregar pestañas
    tabs = ctk.CTkTabview(frame)
    tabs.grid(row=0, column=0, sticky="nsew")

    # Pestaña de Gestión de Clientes
    tabs.add("Clientes")
    clientes_tab = GestionClientes(
        tabs.tab("Clientes"), 
        crear_cliente, 
        obtener_todos_clientes, 
        actualizar_cliente, 
        eliminar_cliente
    )
    
    clientes_tab.grid(row=0, column=0, sticky="nsew")  # Asegurarse de que la pestaña se expanda

    app.mainloop()

if __name__ == "__main__":
    main()
