import tkinter as tk
from PIL import Image,ImageTk

import sys,os
import fitz
import webbrowser
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import claseControlG
import matplotlib.pyplot as plt
from datetime import datetime
control = claseControlG.ControlG()
fecha = datetime.now().strftime("%d/%m/%Y")

def verificar_password():

    login = tk.Tk()
    login.title("Acceso al Sistema")
    login.geometry("500x350")
    login.resizable(False, False)
    login.configure(bg="#121212")

    acceso = {"ok": False}

    Label(
        login,
        text="Tienda de abarrotes El Milagro",
        font=("Segoe UI", 20, "bold"),
        bg="#121212",
        fg="#D4AF37"
    ).pack(pady=25)

    Label(
        login,
        text="🔒 INICIAR SESIÓN",
        font=("Segoe UI", 14, "bold"),
        bg="#121212",
        fg="white"
    ).pack()

    Label(
        login,
        text="Contraseña",
        font=("Segoe UI", 11),
        bg="#121212",
        fg="#D4AF37"
    ).pack(pady=(20,5))

    txtPass = Entry(
        login,
        show="*",
        font=("Segoe UI", 12),
        width=25,
        justify="center"
    )
    txtPass.pack()

    def entrar():
        if txtPass.get() == "1234":
            acceso["ok"] = True
            login.destroy()
        else:
            messagebox.showerror(
                "Error",
                "Contraseña incorrecta"
            )

    Button(
        login,
        text="INGRESAR",
        bg="#D4AF37",
        fg="black",
        font=("Segoe UI", 11, "bold"),
        width=20,
        cursor="hand2",
        command=entrar
    ).pack(pady=25)

    Label(
        login,
        text="Sistema de Control Administrativo",
        font=("Segoe UI", 9),
        bg="#121212",
        fg="gray"
    ).pack(side="bottom", pady=15)

    login.mainloop()

    return acceso["ok"]






# Funciones para cambiar el contenido
def mostrar_inicio():
    """
    esta funcion muestra la portada del apartado de inicio
    :return:
    """
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
    """
    esta funcion permite ingresar datos
    :return:
    """
    limpiar_contenido()
    Label(frame_contenido, text="INGRESOS Y EGRESOS", font=("Arial", 16, "bold")).place(x=20, y=20)


    def actualizar_tabla():
        """
        esta funcion actualiza la informacion de la tabla
        :return:
        """
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
        """
        esta funcion inserta los datos de la tabla
        :return:
        """
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
        """
        esta fincion elimina datos de la tabla
        :return:
        """
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro")
            return
        indice = tabla.index(seleccion[0])
        control.eliminar(indice)
        actualizar_tabla()

    def graficar():
        """
        esta funcion grafica los datos de la tabla
        :return:
        """
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

    # ===== FORMULARIO =====

    frame_form = Frame(frame_contenido, bg="#FFFFFF", bd=1, relief="solid")
    frame_form.place(x=20, y=60, width=700, height=180)

    lblFecha = Label(frame_form, text="📅 Fecha",
                     bg="#FFFFFF", fg="#000000",
                     font=("Segoe UI", 10, "bold"))
    lblFecha.place(x=20, y=20)

    txtFecha = Entry(frame_form, font=("Segoe UI", 10))
    txtFecha.place(x=140, y=20, width=220)

    lblTipo = Label(frame_form, text="📂 Tipo",
                    bg="#FFFFFF", fg="#000000",
                    font=("Segoe UI", 10, "bold"))
    lblTipo.place(x=20, y=60)

    cmbTipo = ttk.Combobox(
        frame_form,
        values=["ingreso", "egreso"],
        state="readonly",
        font=("Segoe UI", 10)
    )
    cmbTipo.place(x=140, y=60, width=220)
    cmbTipo.current(0)

    lblDes = Label(frame_form, text="📝 Descripción",
                   bg="#FFFFFF", fg="#000000",
                   font=("Segoe UI", 10, "bold"))
    lblDes.place(x=20, y=100)

    txtDes = Entry(frame_form, font=("Segoe UI", 10))
    txtDes.place(x=140, y=100, width=220)

    lblCantidad = Label(frame_form, text="💰 Cantidad",
                        bg="#FFFFFF", fg="#000000",
                        font=("Segoe UI", 10, "bold"))
    lblCantidad.place(x=20, y=140)

    txtCantidad = Entry(frame_form, font=("Segoe UI", 10))
    txtCantidad.place(x=140, y=140, width=220)

    # ===== BOTONES =====

    botonInsertar = Button(
        frame_form,
        text="➕ Insertar",
        command=insertar,
        bg="#D4AF37",
        fg="black",
        font=("Segoe UI", 10, "bold"),
        relief="flat"
    )
    botonInsertar.place(x=500, y=20, width=150, height=35)

    botonEliminar = Button(
        frame_form,
        text="❌ Eliminar",
        command=eliminar,
        bg="#8B0000",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat"
    )
    botonEliminar.place(x=500, y=70, width=150, height=35)

    botongraficar = Button(
        frame_form,
        text="📊 Graficar",
        command=graficar,
        bg="#0F766E",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat"
    )
    botongraficar.place(x=500, y=120, width=150, height=35)

    # ===== TARJETA RESUMEN =====

    frame_resumen = Frame(
        frame_contenido,
        bg="#FFF8DC",
        bd=1,
        relief="solid"
    )
    frame_resumen.place(x=760, y=60, width=220, height=180)

    Label(
        frame_resumen,
        text="💰 RESUMEN",
        bg="#FFF8DC",
        fg="#333333",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=15)

    Label(
        frame_resumen,
        text="Ingresos / Egresos",
        bg="#FFF8DC",
        fg="#555555",
        font=("Segoe UI", 10)
    ).pack()

    # ===== TABLA =====

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28,
        background="white",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        background="#D4AF37",
        foreground="black",
        font=("Segoe UI", 10, "bold")
    )

    tabla = ttk.Treeview(
        frame_contenido,
        columns=("fecha", "tipo", "descripcion", "cantidad", "acumulado"),
        show="headings"
    )

    tabla.heading("fecha", text="Fecha")
    tabla.heading("tipo", text="Tipo")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("acumulado", text="Acumulado")

    tabla.column("fecha", width=120)
    tabla.column("tipo", width=100)
    tabla.column("descripcion", width=320)
    tabla.column("cantidad", width=120)
    tabla.column("acumulado", width=150)

    tabla.place(x=20, y=260, width=960, height=250)

    # ===== RESULTADOS =====

    lblIngresos = Label(
        frame_contenido,
        text="Total Ingresos: $0.00",
        bg="#FFFFFF",
        fg="green",
        font=("Segoe UI", 10, "bold")
    )
    lblIngresos.place(x=20, y=530)

    lblEgresos = Label(
        frame_contenido,
        text="Total Egresos: $0.00",
        bg="#FFFFFF",
        fg="red",
        font=("Segoe UI", 10, "bold")
    )
    lblEgresos.place(x=280, y=530)

    lblAcumulado = Label(
        frame_contenido,
        text="Total Acumulado: $0.00",
        bg="#FFFFFF",
        fg="#D4AF37",
        font=("Segoe UI", 10, "bold")
    )
    lblAcumulado.place(x=540, y=530)

    lblGanancia = Label(
        frame_contenido,
        text="Ganancia: $0.00",
        bg="#FFFFFF",
        fg="#0F766E",
        font=("Segoe UI", 10, "bold")
    )
    lblGanancia.place(x=20, y=570)

    lblResultado = Label(
        frame_contenido,
        text="",
        bg="#FFFFFF",
        fg="#000000",
        font=("Segoe UI", 10, "bold")
    )
    lblResultado.place(x=280, y=570)

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
    """
    esta funcion permite ingresar datos a la tabla de clientes
    :return:
    """
    limpiar_contenido()

    frame_contenido.config(bg="#F8FAFC")

    # Título
    Label(
        frame_contenido,
        text="👥 CLIENTES",
        font=("Segoe UI", 20, "bold"),
        fg="#0F172A",
        bg="#F8FAFC"
    ).place(x=20, y=20)

    def insertar():
        """
        esta funcion permite ingresar datos a la tabloa de clientes
        :return:
        """
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

        lblTotal.config(text=str(len(tabla.get_children())))

    def eliminar():
        """
        esta funcion permite elimininar datos en la tabla de clientes
        :return:
        """
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro")
            return

        tabla.delete(seleccion[0])

        lblTotal.config(text=str(len(tabla.get_children())))

    # Marco formulario
    frame_form = Frame(
        frame_contenido,
        bg="white",
        bd=1,
        relief="solid"
    )
    frame_form.place(x=20, y=70, width=720, height=180)

    # Cliente
    Label(
        frame_form,
        text="🆔 No. Cliente",
        bg="white",
        font=("Segoe UI", 10, "bold")
    ).place(x=20, y=20)

    txtCliente = Entry(frame_form, font=("Segoe UI", 10))
    txtCliente.place(x=150, y=20, width=220)

    # Nombre
    Label(
        frame_form,
        text="👤 Nombre",
        bg="white",
        font=("Segoe UI", 10, "bold")
    ).place(x=20, y=60)

    txtNombre = Entry(frame_form, font=("Segoe UI", 10))
    txtNombre.place(x=150, y=60, width=220)

    # Correo
    Label(
        frame_form,
        text="📧 Correo",
        bg="white",
        font=("Segoe UI", 10, "bold")
    ).place(x=20, y=100)

    txtCorreo = Entry(frame_form, font=("Segoe UI", 10))
    txtCorreo.place(x=150, y=100, width=220)

    # Teléfono
    Label(
        frame_form,
        text="📞 Teléfono",
        bg="white",
        font=("Segoe UI", 10, "bold")
    ).place(x=20, y=140)

    txtTelefono = Entry(frame_form, font=("Segoe UI", 10))
    txtTelefono.place(x=150, y=140, width=220)

    # Botón insertar
    Button(
        frame_form,
        text="➕ Insertar",
        bg="#F59E0B",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=insertar
    ).place(x=500, y=40, width=160, height=40)

    # Botón eliminar
    Button(
        frame_form,
        text="🗑 Eliminar",
        bg="#EF4444",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=eliminar
    ).place(x=500, y=100, width=160, height=40)

    # Tarjeta resumen
    frame_resumen = Frame(
        frame_contenido,
        bg="#FEF3C7",
        bd=1,
        relief="solid"
    )
    frame_resumen.place(x=760, y=70, width=220, height=180)

    Label(
        frame_resumen,
        text="👥 CLIENTES",
        bg="#FEF3C7",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=20)

    lblTotal = Label(
        frame_resumen,
        text="3",
        bg="#FEF3C7",
        font=("Segoe UI", 28, "bold")
    )
    lblTotal.pack()

    # Estilo tabla
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview.Heading",
        background="#F59E0B",
        foreground="white",
        font=("Segoe UI", 10, "bold")
    )

    style.configure(
        "Treeview",
        rowheight=30,
        font=("Segoe UI", 10)
    )

    # Tabla
    tabla = ttk.Treeview(
        frame_contenido,
        columns=("cliente", "nombre", "correo", "telefono"),
        show="headings"
    )

    tabla.heading("cliente", text="No. Cliente")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("correo", text="Correo")
    tabla.heading("telefono", text="Teléfono")

    tabla.column("cliente", width=120)
    tabla.column("nombre", width=220)
    tabla.column("correo", width=250)
    tabla.column("telefono", width=180)

    tabla.insert("", END, values=("001", "Juan Pérez", "juan@gmail.com", "5512345678"))
    tabla.insert("", END, values=("002", "Ana López", "ana@gmail.com", "5587654321"))
    tabla.insert("", END, values=("003", "Carlos Ruiz", "carlos@gmail.com", "5545678901"))

    tabla.place(x=20, y=280, width=960, height=320)


def mostrar_proveedores():
    """
    esta funcion muestra la tabla de provedores
    :return:
    """
    limpiar_contenido()

    frame_contenido.config(bg="#FFFFFF")

    # Encabezado
    Frame(
        frame_contenido,
        bg="#111111",
        height=50
    ).place(x=0, y=0, width=1200)

    Label(
        frame_contenido,
        text="🚚 PROVEEDORES",
        font=("Segoe UI", 18, "bold"),
        fg="#D4AF37",
        bg="#111111"
    ).place(x=20, y=10)

    def insertar():
        """
        esta funcion permite ingresar datos a la tabla de provedores
        :return:
        """
        proveedor = txtProveedor.get()
        mercancia = txtMercancia.get()
        correo = txtCorreo.get()
        telefono = txtTelefono.get()

        if proveedor == "" or mercancia == "" or correo == "" or telefono == "":
            messagebox.showwarning("Aviso", "Complete todos los campos")
            return

        tabla.insert("", END, values=(proveedor, mercancia, correo, telefono))

        txtProveedor.delete(0, END)
        txtMercancia.delete(0, END)
        txtCorreo.delete(0, END)
        txtTelefono.delete(0, END)

        lblTotal.config(text=str(len(tabla.get_children())))

    def eliminar():
        """
        esta funcion permite eliminar datos a la tabla de provedores
        :return:
        """
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un registro")
            return

        tabla.delete(seleccion[0])

        lblTotal.config(text=str(len(tabla.get_children())))

    # Formulario
    frame_form = Frame(
        frame_contenido,
        bg="#FFFFFF",
        bd=1,
        relief="solid"
    )
    frame_form.place(x=20, y=70, width=700, height=180)

    Label(frame_form, text="🏢 Proveedor",
          bg="#FFFFFF",
          font=("Segoe UI", 10, "bold")).place(x=20, y=20)

    txtProveedor = Entry(frame_form, font=("Segoe UI", 10))
    txtProveedor.place(x=150, y=20, width=220)

    Label(frame_form, text="📦 Mercancía",
          bg="#FFFFFF",
          font=("Segoe UI", 10, "bold")).place(x=20, y=60)

    txtMercancia = Entry(frame_form, font=("Segoe UI", 10))
    txtMercancia.place(x=150, y=60, width=220)

    Label(frame_form, text="📧 Correo",
          bg="#FFFFFF",
          font=("Segoe UI", 10, "bold")).place(x=20, y=100)

    txtCorreo = Entry(frame_form, font=("Segoe UI", 10))
    txtCorreo.place(x=150, y=100, width=220)

    Label(frame_form, text="📞 Teléfono",
          bg="#FFFFFF",
          font=("Segoe UI", 10, "bold")).place(x=20, y=140)

    txtTelefono = Entry(frame_form, font=("Segoe UI", 10))
    txtTelefono.place(x=150, y=140, width=220)

    Button(
        frame_form,
        text="➕ Insertar",
        command=insertar,
        bg="#D4AF37",
        fg="black",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2"
    ).place(x=500, y=40, width=150, height=40)

    Button(
        frame_form,
        text="❌ Eliminar",
        command=eliminar,
        bg="#8B0000",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2"
    ).place(x=500, y=100, width=150, height=40)

    # Tarjeta resumen
    frame_resumen = Frame(
        frame_contenido,
        bg="#FFF8DC",
        bd=1,
        relief="solid"
    )
    frame_resumen.place(x=760, y=70, width=220, height=180)

    Label(
        frame_resumen,
        text="🚚 PROVEEDORES",
        bg="#FFF8DC",
        fg="#333333",
        font=("Segoe UI", 12, "bold")
    ).pack(pady=20)

    lblTotal = Label(
        frame_resumen,
        text="5",
        bg="#FFF8DC",
        fg="#D4AF37",
        font=("Segoe UI", 28, "bold")
    )
    lblTotal.pack()

    # Estilo tabla
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=30,
        background="white",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        background="#D4AF37",
        foreground="black",
        font=("Segoe UI", 10, "bold")
    )

    tabla = ttk.Treeview(
        frame_contenido,
        columns=("proveedor", "mercancia", "correo", "telefono"),
        show="headings"
    )

    tabla.heading("proveedor", text="Proveedor")
    tabla.heading("mercancia", text="Mercancía")
    tabla.heading("correo", text="Correo")
    tabla.heading("telefono", text="Teléfono")

    tabla.column("proveedor", width=250)
    tabla.column("mercancia", width=250)
    tabla.column("correo", width=300)
    tabla.column("telefono", width=180)

    tabla.insert("", END, values=("Distribuidora La Central", "Refrescos y Jugos", "ventas@lacentral.com", "5512345678"))
    tabla.insert("", END, values=("Abarrotes El Sol", "Arroz, Frijol y Azúcar", "contacto@abarroteselsol.com", "5587654321"))
    tabla.insert("", END, values=("Lácteos San José", "Leche, Queso y Yogurt", "pedidos@lacteossanjose.com", "5545678912"))
    tabla.insert("", END, values=("Dulcería La Estrella", "Dulces y Chocolates", "ventas@dulceriaestrella.com", "5532147896"))
    tabla.insert("", END, values=("Botanas Mexicanas SA", "Papas y Botanas", "pedidos@botanasmex.com", "5556781234"))

    tabla.place(
        x=20,
        y=280,
        width=960,
        height=320
    )




# Codigo de controles
# Elimina los controles anteriores
def limpiar_contenido():
    """ Elimina los controles anteriores """
    for widget in frame_contenido.winfo_children():
        widget.destroy()


def mostrar_principal():
    if not verificar_password():
        return
    """
    muestra una ventana principal de 3s
    :return:
    """
    global frame_contenido
    # Ruta de imagen, pdf

    # Para mostrar pdf

    def mostrar_pdf():

        ruta = os.path.join(getattr(sys, "_MEIPASS", "."), "Manual_U.pdf")

        doc = fitz.open(ruta)
        limpiar_contenido()
        pagina = {"i": 0}
        lbl = Label(frame_contenido)
        lbl.pack()

        def render(doc):
            page = doc.load_page(pagina["i"])

            pix = page.get_pixmap()
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            img = img.resize((600, 800))
            foto = ImageTk.PhotoImage(img)
            lbl.config(image=foto)
            lbl.image = foto

        def siguiente():
            if pagina["i"] < len(doc) - 1:
                pagina["i"] += 1

                render(doc)

        def anterior():
            if pagina["i"] > 0:
                pagina["i"] -= 1

                render(doc)
        btn = Frame(frame_contenido).pack()
        Button(btn, text="⬅", command=anterior).pack(side="left")
        Button(btn, text="➡", command=siguiente).pack(side="left")
        render(doc)





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
    Button(frame_menu,text="📖 Ayuda",bg="#D4AF37",fg="#FFFFFF",font=("Segoe UI",10,"italic"),command=mostrar_pdf,width=20).pack(pady=10)
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
    """
    esta funcion cierra el programa
    :return:
    """
    splash.destroy()
    mostrar_principal()


splash = Tk()

# Centrar ventana

ancho = 700

alto = 400

x = (splash.winfo_screenwidth() - ancho) // 2

y = (splash.winfo_screenheight() - alto) // 2

splash.geometry(f"{ancho}x{alto}+{x}+{y}")

# Colores

COLOR_FONDO = "#121212"

COLOR_DORADO = "#D4AF37"

splash.configure(bg=COLOR_FONDO)

splash.overrideredirect(True)

# Marco decorativo

Frame(

    splash,

    bg=COLOR_DORADO,

    height=4

).pack(fill=X)

# Título principal

Label(

    splash,

    text="🏪 TIENDA DE ABARROTES EL MILAGRO 🏪",

    fg=COLOR_DORADO,

    bg=COLOR_FONDO,

    font=("Times New Roman", 24, "bold")

).place(x=20, y=50)

# Emojis centrales

Label(

    splash,

    text="🛒   📦   💰",

    fg=COLOR_DORADO,

    bg=COLOR_FONDO,

    font=("Segoe UI Emoji", 60)

).place(x=130, y=100)

# Nombre del sistema

Label(

    splash,

    text="📊 SISTEMA DE CONTROL",

    fg="white",

    bg=COLOR_FONDO,

    font=("Arial", 20, "bold")

).place(x=175, y=220)

Label(

    splash,

    text="INGRESOS Y EGRESOS",

    fg=COLOR_DORADO,

    bg=COLOR_FONDO,

    font=("Arial", 16, "bold")

).place(x=225, y=260)

# Pie de página

Label(

    splash,

    text="👨‍💻 Realizado por:\nJ. Angel\nFernanda\nA. Antonio\nJ. Julian ",

    fg="white",

    bg=COLOR_FONDO,

    font=("Arial", 11)

).place(x=285, y=285)

Label(

    splash,

    text="⭐ Prototipo Junio 2026 ⭐",

    fg=COLOR_DORADO,

    bg=COLOR_FONDO,

    font=("Arial", 10, "bold")

).place(x=250, y=370)

# Cerrar después de 3 segundos

splash.after(3000, cerrar)

splash.mainloop()