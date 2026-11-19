import tkinter as tk
from PIL import Image,ImageTk
import os
import webbrowser
from tkinter import *
from tkinter import ttk, messagebox
import claseControlG
import matplotlib.pyplot as plt
from datetime import datetime
control = claseControlG.ControlG()
fecha = datetime.now().strftime("%d/%m/%Y")
# Funciones para cambiar el contenido
def mostrar_inicio():
    limpiar_contenido()

    Label(frame_contenido,
          text="SISTEMA DE CONTROL",
          font=("Segoe UI", 24, "italic"),
          fg="#2C3E50",
          bg="#F8F8F8").place(x=200, y=20)

    Label(frame_contenido,
          text="ABARROTES EL MILAGRO",
          font=("Segoe UI", 34, "bold"),
          fg="#D4A017",
          bg="#F8F8F8").place(x=100, y=90)

    Label(frame_contenido,
          text="🛒 🏪 🥫 🍞 🥛",
          font=("Segoe UI Emoji", 50),
          bg="#F8F8F8").place(x=100, y=180)

    Label(frame_contenido,
          text="Sistema de Egresos e Ingresos",
          font=("Segoe UI", 18),
          fg="#555555",
          bg="#F8F8F8").place(x=200, y=280)

    Label(frame_contenido,
          text="Clientes • Proveedores • Ingresos • Egresos",
          font=("Segoe UI", 12),
          fg="#777777",
          bg="#F8F8F8").place(x=210, y=330)

    frame_contenido.config(bg="#F8F8F8")
    Frame(frame_contenido,
          bg="#D4A017",
          height=4,
          width=500).place(x=120, y=160)
    Frame(frame_contenido, bg="white", width=150, height=80).place(x=80, y=400)
    Label(frame_contenido, text="👥 Clientes", bg="white").place(x=110, y=430)

    Frame(frame_contenido, bg="white", width=150, height=80).place(x=280, y=400)
    Label(frame_contenido, text="🚚 Provedores", bg="white").place(x=300, y=430)

    Frame(frame_contenido, bg="white", width=150, height=80).place(x=480, y=400)
    Label(frame_contenido, text="💰 Ingresos y Egresos", bg="white").place(x=500, y=430)

    Frame(
        frame_contenido,
        bg="#D4A017",
        width=500,
        height=2
    ).place(x=120, y=500)

    Label(
        frame_contenido,
        text="★ Tu negocio, en buenas manos ★",
        font=("Segoe UI", 16, "italic"),
        fg="#D4A017",
        bg="#F8F8F8"
    ).place(x=220, y=520)


# Codigo de controles
def mostrar_movimientos():
    limpiar_contenido()
    Label(frame_contenido, text="INGRESOS Y EGRESOS", font=("Arial", 16, "bold")).place(x=20, y=20)

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)
        acumulado = 0
        for registro in control.registros:
            if registro[1] == "ingreso":
                acumulado += registro[3]
            else:
                acumulado -= registro[3]
            tabla.insert("", END, values=(registro[0], registro[1], registro[2], registro[3], acumulado))
        lblIngresos.config(text=f"Total Ingresos: ${control.total_ingresos:.2f}")
        lblEgresos.config(text=f"Total Egresos: ${control.total_egresos:.2f}")
        lblAcumulado.config(text=f"Total Acumulado: ${control.total_acumulado:.2f}")
        lblGanancia.config(text=f"Ganancia: ${control.calcular_ganancia():.2f}")
        lblResultado.config(text=control.determinar_resultado())

    def insertar():
        try:
            fecha = txtFecha.get()
            tipo = cmbTipo.get().lower()
            descripcion = txtDes.get()
            cantidad = float(txtCantidad.get())
            if fecha == "" or descripcion == "":
                messagebox.showwarning("Aviso", "Complete todos los campos")
                return
            control.insertar(fecha, tipo, descripcion, cantidad)
            actualizar_tabla()
            txtFecha.delete(0, END)
            txtDes.delete(0, END)
            txtCantidad.delete(0, END)
            txtFecha.focus()
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida")

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro")
            return
        indice = tabla.index(seleccion[0])
        control.eliminar(indice)
        actualizar_tabla()

    def graficar():
        """ """
        # Crear listas para almacenar los datos a graficar
        ingresos = []
        egresos = []
        fechasI = []
        fechasE = []
        # Llenar listas con los datos a gràficar
        for registro in control.registros:
            if registro[1] == "ingreso":
                ingresos.append(registro[3])
                fechasI.append(registro[0])
            else:
                egresos.append(registro[3])
                fechasE.append(registro[0])
            # Crear figura y ejes
        fig, ax = plt.subplots()
        # Agregamos la serie ingresos de color purpura
        ax.plot(fechasI, ingresos, color='tab:purple', label='INGRESOS')
        # Agregamos la serie egreso de color verde
        ax.plot(fechasE, egresos, color='tab:green', label='EGRESOS')
        ax.legend(loc='upper right')
        # Confugurar etiquetas del eje de X , y titulo del gràfico
        ax.set_xlabel("FECHA", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:red'})
        ax.set_ylabel("CANTIDAD EN $ ")
        ax.set_title('CONTROL DE INGRESOS Y EGRESOS ', loc="left",
                     fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        # Titulo de la ventana del gràfico
        fig.canvas.manager.set_window_title('GRAFICO DE INGRESOS Y EGRESOS')
        # Mostrar gràfico
        plt.show()

        # Ventana

    # No crear otra ventana
    # Todo se mostrará en frame_contenido


    # Etiquetas y cajas de texto



    lblFecha = Label(frame_contenido, text="Fecha",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblFecha.place(x=20, y=60)
    txtFecha = Entry( frame_contenido,width=20,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    txtFecha.place(x=120, y=60)
    lblTipo = Label( frame_contenido,text="Tipo",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblTipo.place(x=20, y=90)
    cmbTipo = ttk.Combobox( frame_contenido,values=["ingreso",
                                           "egreso"], state="readonly", width=17,font=("Segoe UI", 10, "bold"))
    cmbTipo.place(x=120, y=90)
    cmbTipo.current(0)
    lblDes = Label(frame_contenido, text="Descripcion", bg="#F8F8F8", fg="#000000", font=("Segoe UI", 10, "bold"))
    lblDes.place(x=20, y=120)
    txtDes = Entry(frame_contenido, width=20)
    txtDes.place(x=120, y=120)
    lblCantidad = Label(frame_contenido, text="Cantidad",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblCantidad.place(x=20, y=160)
    txtCantidad = Entry( frame_contenido,width=20)
    txtCantidad.place(x=120, y=160)

    # Botones
    botonInsertar = Button( frame_contenido,text="➕ Insertar", width=15, command=insertar,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    botonInsertar.place(x=400, y=60)
    botonEliminar = Button(frame_contenido,text="❌ Eliminar", width=15, command=eliminar,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    botonEliminar.place(x=400, y=95)
    botongraficar = Button(frame_contenido,text="📊 Graficar", width=15, command=graficar,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    botongraficar.place(x=400, y=130)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=30,
        background="#F8F8F8",
        fieldbackground="#F8F8F8"
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#D4AF37",
        foreground="black"
    )
    tabla = ttk.Treeview(frame_contenido, columns=("fecha", "tipo", "descripcion", "cantidad",
                                          "acumulado"), show="headings", height=10)
    # Titulos de columnas de tabla
    tabla.heading("fecha", text="Fecha")
    tabla.heading("tipo", text="Tipo")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("acumulado", text="Total Acumulado")
    # Tamaño de columnas de tabla
    tabla.column("fecha", width=80)
    tabla.column("tipo", width=80)
    tabla.column("descripcion", width=200)
    tabla.column("cantidad", width=100)
    tabla.column("acumulado", width=120)
    tabla.place(x=20, y=200)
    # Etiquetas de resultados
    lblIngresos = Label( frame_contenido,text="Total Ingresos: $0.00",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold")
)
    lblIngresos.place(x=20, y=540)
    lblEgresos = Label( frame_contenido,text="Total Egresos: $0.00",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblEgresos.place(x=250, y=540)
    lblAcumulado = Label(frame_contenido, text="Total Acumulado: $0.00",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblAcumulado.place(x=500, y=540)
    lblGanancia = Label( frame_contenido,text="Ganancia: $0.00",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold") )
    lblGanancia.place(x=20, y=580)
    lblResultado = Label( frame_contenido,text="",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblResultado.place(x=250, y=580)

    # Datos de prueba
    control.insertar("20/05/2026", "ingreso", "venta vasos", 16)
    control.insertar("21/05/2026", "inreso", "venta de bolsas", 30)
    control.insertar("22/05/2026", "ingreso", "Venta del laton", 8)
    control.insertar("23/05/2026", "ingreso", "Venta de laton", 8)
    control.insertar("24/05/2026", "ingreso", "venta de mul mix", 16)
    control.insertar("25/05/2026", "ingreso", "Venta de huevo", 16)
    control.insertar("26/05/2026", "ingreso", "venta de servilletas", 14)
    control.insertar("27/05/2026", "ingreso", "Venta de vivk vaporub", 38)
    control.insertar("28/05/2026", "ingreso", "Venta de sabritas", 72)
    control.insertar("29/05/2026", "ingreso", "venta de pan", 300)
    control.insertar("20/06/2026", "ingreso", "venta de jabon", 24)
    control.insertar("21/06/2026", "inreso", "venta de queso", 58)
    control.insertar("22/06/2026", "ingreso", "Venta del cloralex", 30)
    control.insertar("23/06/2026", "ingreso", "Venta de leche", 20)
    control.insertar("24/06/2026", "ingreso", "venta de bolsas", 26)
    control.insertar("25/06/2026", "ingreso", "Venta de sabritas", 54)
    control.insertar("26/06/2026", "ingreso", "venta de cloralex", 24)
    control.insertar("27/06/2026", "ingreso", "Venta de jabon", 58)
    control.insertar("28/06/2026", "ingreso", "Venta de gansito", 24)
    control.insertar("29/06/2026", "ingreso", "venta de cofie", 16)
    control.insertar("20/07/2026", "ingreso", "venta de servilletas", 8)
    control.insertar("21/07/2026", "inreso", "venta de gumaba", 16)
    control.insertar("22/07/2026", "ingreso", "Venta del oro", 10)
    control.insertar("23/07/2026", "ingreso", "Venta de oro", 22)
    control.insertar("24/07/2026", "ingreso", "venta de ovito", 22)
    control.insertar("25/07/2026", "ingreso", "Venta de carpita", 10)
    control.insertar("26/07/2026", "ingreso", "venta de valle", 20)
    control.insertar("27/07/2026", "ingreso", "Venta de mantecadas", 28)
    control.insertar("28/07/2026", "ingreso", "Venta de vaso", 54)
    control.insertar("29/07/2026", "ingreso", "venta de del valle coco", 20)
    control.insertar("20/08/2026", "ingreso", "Venta de cuayu", 12)
    control.insertar("21/08/2026", "ingreso", "Venta de limonada", 20)
    control.insertar("22/08/2026", "ingreso", "venta de vuala", 4)
    control.insertar("23/08/2026", "egreso", "compra de fideo", 250)
    control.insertar("24/08/2026", "egreso", "compra de huevo", 18)
    control.insertar("25/08/2026", "egreso", "compra de cuino", 6)
    control.insertar("26/08/2026", "egreso", "compra de soya", 8)
    control.insertar("27/08/2026", "egreso", "compra de cajetilla", 8)
    control.insertar("28/08/2026", "egreso", "compra de brendy", 80)
    control.insertar("29/08/2026", "egreso", "compra de sabritas", 160)
    control.insertar("20/09/2026", "egreso", "compra de mul mix", 104)
    control.insertar("21/09/2026", "egreso", "compra de sabritas", 84)
    control.insertar("22/09/2026", "egreso", "compra de papas", 22)
    control.insertar("23/09/2026", "egreso", "compra de sabritas", 84)
    control.insertar("24/09/2026", "egreso", "compra de ovito", 80)
    control.insertar("25/09/2026", "egreso", "compra de mantecadas", 16)
    control.insertar("26/09/2026", "egreso", "compra de del valle coc", 48)
    control.insertar("27/09/2026", "egreso", "compra de delicias", 20)
    control.insertar("28/09/2026", "egreso", "compra de favos", 252)
    # Actualizar tabla por daos ingresados de prueba
    actualizar_tabla()
    # Bucle de ejecuciòn del programa







# Codigo de controles

def mostrar_clientes():
    limpiar_contenido()
    Label(frame_contenido, text="CLIENTES", font=("Arial", 16, "bold")).place(x=20, y=20)



    def insertar():
        cliente = txtCliente.get()
        nombre = txtNombre.get()
        correo = txtCorreo.get()
        telefono = txtTelefono.get()

        if cliente == "" or nombre == "" or correo == "" or telefono == "":
            messagebox.showwarning("Aviso", "Complete todos los campos")
            return

        tabla.insert("", END, values=(cliente, nombre, correo, telefono))

        txtCliente.delete(0, END)
        txtNombre.delete(0, END)
        txtCorreo.delete(0, END)
        txtTelefono.delete(0, END)
    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro")
            return
        indice = tabla.index(seleccion[0])
        control.eliminar(indice)



        # Ventana

    # No crear otra ventana
    # Todo se mostrará en frame_contenido


    # Etiquetas y cajas de texto

    lblCliente = Label(frame_contenido, text="No. Cliente",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblCliente.place(x=20, y=60)

    txtCliente = Entry(frame_contenido, width=20,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    txtCliente.place(x=120, y=60)

    lblNombre = Label(frame_contenido, text="Nombre",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblNombre.place(x=20, y=100)

    txtNombre = Entry(frame_contenido, width=20)
    txtNombre.place(x=120, y=100)

    lblCorreo = Label(frame_contenido, text="Correo",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblCorreo.place(x=20, y=140)

    txtCorreo = Entry(frame_contenido, width=20)
    txtCorreo.place(x=120, y=140)

    lblTelefono = Label(frame_contenido, text="Teléfono",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblTelefono.place(x=20, y=180)

    txtTelefono = Entry(frame_contenido, width=20)
    txtTelefono.place(x=120, y=180)

    # Botones
    botonInsertar = Button( frame_contenido,text="➕ Insertar", width=15, command=insertar,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    botonInsertar.place(x=400, y=60)
    botonEliminar = Button(frame_contenido,text="❌ Eliminar", width=15, command=eliminar,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    botonEliminar.place(x=400, y=95)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=30,
        background="#F8F8F8",
        fieldbackground="#F8F8F8"
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background="#D4AF37",
        foreground="black"
    )


    tabla = ttk.Treeview(
        frame_contenido,
        columns=("cliente", "nombre", "correo", "telefono"),
        show="headings",
        height=10
    )
    # Titulos de columnas de tabla
    tabla.heading("cliente", text="No. Cliente")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("correo", text="Correo")
    tabla.heading("telefono", text="Teléfono")

    tabla.column("cliente", width=100)
    tabla.column("nombre", width=180)
    tabla.column("correo", width=220)
    tabla.column("telefono", width=120)
    # Etiquetas de resultados

    tabla.insert("", END, values=("001", "Juan Pérez", "juan@gmail.com", "5512345678"))
    tabla.insert("", END, values=("002", "Ana López", "ana@gmail.com", "5587654321"))
    tabla.insert("", END, values=("003", "Carlos Ruiz", "carlos@gmail.com", "5545678901"))
    tabla.place(x=20,y=250)



def mostrar_proveedores():
    limpiar_contenido()
    Label(frame_contenido, text="PROVEEDORES", font=("Arial", 16, "bold")).place(x=20, y=20)
    def insertar():
        provedor = txtProvedor.get()
        mercancia = txtMercancia.get()
        correo = txtCorreo.get()
        telefono = txtTelefono.get()

        if provedor == "" or mercancia == "" or correo == "" or telefono == "":
            messagebox.showwarning("Aviso", "Complete todos los campos")
            return

        tabla.insert("", END, values=(provedor, mercancia, correo, telefono))

        txtProvedor.delete(0, END)
        txtMercancia.delete(0, END)
        txtCorreo.delete(0, END)
        txtTelefono.delete(0, END)
    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro")
            return
        indice = tabla.index(seleccion[0])
        control.eliminar(indice)



        # Ventana

    # No crear otra ventana
    # Todo se mostrará en frame_contenido


    # Etiquetas y cajas de texto

    lblProvedor = Label(frame_contenido, text="Provedor",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblProvedor.place(x=20, y=60)

    txtProvedor = Entry(frame_contenido, width=20,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    txtProvedor.place(x=120, y=60)

    lblMercancia = Label(frame_contenido, text="Mercancia",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblMercancia.place(x=20, y=100)

    txtNombre = Entry(frame_contenido, width=20)
    txtNombre.place(x=120, y=100)

    lblCorreo = Label(frame_contenido, text="Correo",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblCorreo.place(x=20, y=140)

    txtCorreo = Entry(frame_contenido, width=20)
    txtCorreo.place(x=120, y=140)

    lblTelefono = Label(frame_contenido, text="Teléfono",bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    lblTelefono.place(x=20, y=180)

    txtTelefono = Entry(frame_contenido, width=20)
    txtTelefono.place(x=120, y=180)

    # Botones
    botonInsertar = Button( frame_contenido,text="➕ Insertar", width=15, command=insertar,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    botonInsertar.place(x=400, y=60)
    botonEliminar = Button(frame_contenido,text="❌ Eliminar", width=15, command=eliminar,bg="#F8F8F8",fg="#000000",font=("Segoe UI", 10, "bold"))
    botonEliminar.place(x=400, y=95)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=30,
        background="#F8F8F8",
        fieldbackground="#F8F8F8"
    )

    style.configure("Treeview.Heading",font=("Segoe UI", 10, "bold"),background="#D4AF37",foreground="black")


    tabla = ttk.Treeview(frame_contenido,columns=("provedor", "mercancia", "correo", "telefono"),show="headings",height=10)
    # Titulos de columnas de tabla
    tabla.heading("provedor", text="Provedor")
    tabla.heading("mercancia", text="Mercancia")
    tabla.heading("correo", text="Correo")
    tabla.heading("telefono", text="Teléfono")

    tabla.column("provedor", width=100)
    tabla.column("mercancia", width=180)
    tabla.column("correo", width=220)
    tabla.column("telefono", width=120)
    # Etiquetas de resultados
    tabla.insert("", "end", values=(
        "Distribuidora La Central",
        "Refrescos y Jugos",
        "ventas@lacentral.com",
        "5512345678"
    ))

    tabla.insert("", "end", values=(
        "Abarrotes El Sol",
        "Arroz, Frijol y Azúcar",
        "contacto@abarroteselsol.com",
        "5587654321"
    ))

    tabla.insert("", "end", values=(
        "Lácteos San José",
        "Leche, Queso y Yogurt",
        "pedidos@lacteossanjose.com",
        "5545678912"
    ))

    tabla.insert("", "end", values=(
        "Dulcería La Estrella",
        "Dulces y Chocolates",
        "ventas@dulceriaestrella.com",
        "5532147896"
    ))

    tabla.insert("", "end", values=(
        "Botanas Mexicanas SA",
        "Papas y Botanas",
        "pedidos@botanasmex.com",
        "5556781234"
    ))


    tabla.place(x=20,y=250)




# Codigo de controles
# Elimina los controles anteriores
def limpiar_contenido():
    """ Elimina los controles anteriores """
    for widget in frame_contenido.winfo_children():
        widget.destroy()


def mostrar_principal():
    global frame_contenido
    def abrir_manual():
        archivo = "manual.docx.pdf"
        if os.path.exists(archivo):
            webbrowser.open_new(archivo)
        else:
            messagebox.showerror("Error","No se encontró el manual de usuario.")

    # Ventana principal
    ventana = Tk()
    ventana.title("Sistema de Control")
    # ventana.geometry("900x500") # asiganar tamaño
    ventana.state("zoomed")  # adpatar al tamaño de la pantalla
    # Frame izquierdo (menú)
    frame_menu = Frame(ventana, width=200, bg="#1C1C1C")
    frame_menu.pack(side=LEFT, fill=Y)
    # Frame derecho (contenido)
    frame_contenido = Frame(ventana, bg="#F8F8F8")
    frame_contenido.pack(side=RIGHT, expand=True, fill=BOTH)
    # Botones del menú
    Label(frame_menu,text="🛒 ABARROTES\nEL MILAGRO",bg="#0F1B2D",fg="#D4A017",font=("Segoe UI", 18, "bold")).pack(pady=20)
    Frame(frame_menu, bg="#D4AF37", width=180, height=2).pack(pady=(5, 2))
    Frame(frame_menu, bg="#D4AF37", width=120, height=2).pack(pady=(0, 10))
    Button(frame_menu, text="🏠 Inicio", width=20, bg="#D4AF37",fg="#FFFFFF",font=("Segoe UI",10,"italic"),command=mostrar_inicio).pack(pady=10)
    Button(frame_menu, text="📊 Ingresos y Egresos", width=20,bg="#D4AF37",fg="#FFFFFF",font=("Segoe UI",10,"italic"), command=mostrar_movimientos).pack(pady=10)
    Button(frame_menu, text="👥 Clientes", width=20, bg="#D4AF37",fg="#FFFFFF",font=("Segoe UI",10,"italic"),command=mostrar_clientes).pack(pady=10)
    Button(frame_menu, text="🚚 Proveedores", width=20,bg="#D4AF37",fg="#FFFFFF",font=("Segoe UI",10,"italic"), command=mostrar_proveedores).pack(pady=10)
    Button(frame_menu, text="❌ Salir", width=20,bg="#D4AF37",fg="#FFFFFF",font=("Segoe UI",10,"italic"), command=ventana.destroy).pack(pady=10)
    Button(frame_menu,text="📖 Ayuda",bg="#D4AF37",fg="#FFFFFF",font=("Segoe UI",10,"italic"),command=abrir_manual,width=20).pack(pady=5)
    Frame(frame_menu, bg="#D4AF37", width=180, height=2).pack(pady=(5, 2))
    Frame(frame_menu, bg="#D4AF37", width=120, height=2).pack(pady=(0, 10))
    Label(
        frame_menu,
        text=f"📅 {fecha}",
        bg="#1C1C1C",
        fg="white",
        font=("Segoe UI", 9)
    ).pack(side="bottom", pady=5)
    # Pantalla inicial
    mostrar_inicio()
    ventana.mainloop()



# SPLASH
def cerrar():
    splash.destroy()
    mostrar_principal()


splash = Tk()
# Centar ventana
# Ancho y alto de la ventana
ancho = 500
alto = 300
x = (splash.winfo_screenwidth() - ancho) // 2
y = (splash.winfo_screenheight() - alto) // 2
splash.geometry(f"{ancho}x{alto}+{x}+{y}")
# Color de fondo
splash.configure(bg="#1E3A5F")
# Quitar bordes y botones a la ventana
splash.overrideredirect(True)
# imagen de logo cecytem

logo = PhotoImage(file="logo.png")



Label(splash, image=logo, bg="#1E3A5F").place(x= 200, y=20)
Label(splash, text="SISTEMA DE CONTROL INGRESOS Y EGRESOS", fg="white", bg="#1E3A5F",
font=("Arial",15,"bold")).place(x= 20, y=150)
Label(splash, text="Realizado por: Jose Angel Nava Barrera", fg="yellow", bg="#1E3A5F",
font=("Arial",12)).place(x= 150, y=200)
Label(splash, text="Prototipo Junio 2026", fg="yellow", bg="#1E3A5F",
font=("Arial",10)).place(x= 190, y=250)
# Abrir ventana principal despues de 3 segundos
splash.after(3000, cerrar)


# Bucle de ejecuciòn
splash.mainloop()