import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
from carta_porte_canceladas import mostrar_cartas_canceladas
from carta_porte_faltantes_sobrantes import mostrar_cartas_faltantes_sobrantes
from exportar_pdf import exportar_a_pdf

class Aplicacion(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Lectura de archivo de Excel")
        self.tabla_frame = None
        self.tabla = None
        self.formulario_frame = None
        self.formulario_texto_operador = None
        self.formulario_texto_unidad = None
        self.formulario_texto_letraPR = None
        self.formulario_texto_origenMunicipio = None
        self.formulario_texto_destinoMunicipio = None
        self.formulario_texto_cliente = None
        self.formulario_texto_fechaCarga = None
        self.formulario_texto_fechaDescarga = None
        self.formulario_texto_producto = None
        self.formulario_texto_cartaPorte = None
        self.formulario_texto_litrosCargados = None
        self.formulario_texto_litrosDescargados = None
        self.formulario_texto_faltante = None
        self.formulario_texto_tiempoViaje = None
        self.busqueda_texto = None
        self.df = None
        self.texto_cartas_canceladas = None

        # Crear la barra de tareas
        self.barra_tareas = tk.Frame(self)
        self.barra_tareas.pack(side=tk.TOP, fill=tk.X)
        

        # Botón "Abrir archivo de Excel"
        boton_abrir = tk.Button(self.barra_tareas, text="Abrir archivo de Excel", command=self.abrir_archivo_excel)
        boton_abrir.pack(side=tk.LEFT, padx=5, pady=5)

        # Botón "Mostrar Cartas Faltantes/Sobrantes"
        boton_mostrar = tk.Button(
            self.barra_tareas, text="Mostrar Cartas Faltantes/Sobrantes", command=lambda: mostrar_cartas_faltantes_sobrantes(self.df)
        )
        boton_mostrar.pack(side=tk.LEFT, padx=5, pady=5)

        # Cuadro de búsqueda
        self.busqueda_texto = tk.Entry(self.barra_tareas)
        self.busqueda_texto.pack(side=tk.LEFT, padx=5, pady=5)
        self.busqueda_texto.bind("<KeyRelease>", self.filtrar_tabla)

        # Botón "Buscar"
        boton_buscar = tk.Button(self.barra_tareas, text="Buscar", command=self.filtrar_tabla)
        boton_buscar.pack(side=tk.LEFT, padx=5, pady=5)

        # Botón "Ver Cartas Porte Canceladas"
        boton_ver_cartas = tk.Button(
            self.barra_tareas, text="Ver Cartas Porte Canceladas", command=lambda: mostrar_cartas_canceladas(self.df)
        )
        boton_ver_cartas.pack(side=tk.LEFT, padx=5, pady=5)

        # Texto "Cartas Porte Canceladas"
        self.texto_cartas_canceladas = tk.Label(self.barra_tareas, text="Cartas Porte Canceladas", fg="black")
        self.texto_cartas_canceladas.pack(side=tk.LEFT, padx=5, pady=5)

        self.geometry("800x600")

    def mostrar_datos(self, event):
        fila_seleccionada = self.tabla.focus()
        datos_fila = self.tabla.item(fila_seleccionada)["values"]

        self.formulario_texto_operador.delete(1.0, tk.END)
        self.formulario_texto_operador.insert(tk.END, str(datos_fila[0]))

        self.formulario_texto_unidad.delete(1.0, tk.END)
        self.formulario_texto_unidad.insert(tk.END, str(datos_fila[1]))

        self.formulario_texto_letraPR.delete(1.0, tk.END)
        self.formulario_texto_letraPR.insert(tk.END, str(datos_fila[2]))

        self.formulario_texto_origenMunicipio.delete(1.0, tk.END)
        self.formulario_texto_origenMunicipio.insert(tk.END, str(datos_fila[3]))

        self.formulario_texto_destinoMunicipio.delete(1.0, tk.END)
        self.formulario_texto_destinoMunicipio.insert(tk.END, str(datos_fila[4]))

        self.formulario_texto_cliente.delete(1.0, tk.END)
        self.formulario_texto_cliente.insert(tk.END, str(datos_fila[5]))

        self.formulario_texto_fechaCarga.delete(1.0, tk.END)
        self.formulario_texto_fechaCarga.insert(tk.END, str(datos_fila[6]))

        self.formulario_texto_fechaDescarga.delete(1.0, tk.END)
        self.formulario_texto_fechaDescarga.insert(tk.END, str(datos_fila[7]))

        self.formulario_texto_producto.delete(1.0, tk.END)
        self.formulario_texto_producto.insert(tk.END, str(datos_fila[8]))

        self.formulario_texto_cartaPorte.delete(1.0, tk.END)
        self.formulario_texto_cartaPorte.insert(tk.END, str(datos_fila[9]))

        self.formulario_texto_litrosCargados.delete(1.0, tk.END)
        self.formulario_texto_litrosCargados.insert(tk.END, str(datos_fila[10]))

        self.formulario_texto_litrosDescargados.delete(1.0, tk.END)
        self.formulario_texto_litrosDescargados.insert(tk.END, str(datos_fila[11]))

        self.formulario_texto_faltante.delete(1.0, tk.END)
        faltante = float(datos_fila[12])
        if faltante < 0:
            faltante = abs(faltante)
            self.formulario_texto_faltante.config(bg="green")
        elif faltante > 0:
            faltante = -faltante
            self.formulario_texto_faltante.config(bg="red")
        else:
            self.formulario_texto_faltante.config(bg="green")
        self.formulario_texto_faltante.insert(tk.END, str(faltante))

        fecha_carga = datos_fila[6]
        fecha_descarga = datos_fila[7]
        if fecha_descarga == 0:
            self.formulario_texto_tiempoViaje.config(text="El viaje no ha terminado", fg="red")
        else:
            tiempo_viaje = self.calcular_tiempo_viaje(fecha_carga, fecha_descarga)
            self.formulario_texto_tiempoViaje.config(text=str(tiempo_viaje), fg="black")

    def abrir_archivo_excel(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx;*.xls")])

        if archivo:
            if self.tabla_frame:
                self.tabla_frame.destroy()

            if archivo.endswith(".xlsx"):
                engine = "openpyxl"
            elif archivo.endswith(".xls"):
                engine = "xlrd"
            else:
                raise ValueError("Formato de archivo de Excel no compatible")

            df = pd.read_excel(archivo, engine=engine)

            columnas_requeridas = [
                "operador",
                "unidad",
                "letraPR",
                "origenMunicipio",
                "destinoMunicipio",
                "cliente",
                "fechaCarga",
                "fechaDescarga",
                "producto",
                "cartaPorte",
                "litrosCargados",
                "litrosDescargados",
                "faltante",
            ]

            # Verificar si todas las columnas requeridas están presentes
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]

            if columnas_faltantes:
                mensaje = f"Las siguientes columnas no se encontraron en el archivo: {', '.join(columnas_faltantes)}"
                messagebox.showwarning("Columnas faltantes", mensaje)
                return

            # Reordenar las columnas según el listado requerido
            df = df[columnas_requeridas]

            self.tabla_frame = tk.Frame(self)
            self.tabla_frame.pack(fill=tk.BOTH, expand=True)

            tabla_scroll = ttk.Scrollbar(self.tabla_frame, orient="horizontal")
            tabla_scroll.pack(side=tk.BOTTOM, fill=tk.X)

            self.tabla = ttk.Treeview(self.tabla_frame, xscrollcommand=tabla_scroll.set)
            tabla_scroll.config(command=self.tabla.xview)

            self.tabla["columns"] = columnas_requeridas

            for columna in columnas_requeridas:
                self.tabla.heading(columna, text=columna)

            for i in range(len(df.index)):
                fila = [str(df.iloc[i, j]) if not pd.isna(df.iloc[i, j]) else "0" for j in range(len(df.columns))]
                self.tabla.insert("", tk.END, values=fila)

            for columna in columnas_requeridas:
                self.tabla.column(columna, width=100, anchor=tk.CENTER)

            self.tabla.pack(fill=tk.BOTH, expand=True)

            self.tabla.configure(height=4, show="headings")

            self.tabla.bind("<ButtonRelease-1>", self.mostrar_datos)

            if self.formulario_frame:
                self.formulario_frame.destroy()

            self.crear_formulario()

            # Almacenar el DataFrame cargado en un atributo de la clase
            self.df = df
            cartas_canceladas = self.calcular_cartas_canceladas()
            self.texto_cartas_canceladas.config(
                text=f"Cartas Porte canceladas: {cartas_canceladas}", fg="black"
            )

    def crear_formulario(self):
        self.formulario_frame = tk.Frame(self)
        self.formulario_frame.pack(fill=tk.BOTH, expand=True)

        # Acomodar los cuadros de texto en filas de tres
        formulario_label_operador = tk.Label(self.formulario_frame, text="Operador:")
        formulario_label_operador.grid(row=0, column=0, padx=10, pady=5)

        self.formulario_texto_operador = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_operador.grid(row=0, column=1, padx=10, pady=5)

        formulario_label_unidad = tk.Label(self.formulario_frame, text="Unidad:")
        formulario_label_unidad.grid(row=0, column=2, padx=10, pady=5)

        self.formulario_texto_unidad = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_unidad.grid(row=0, column=3, padx=10, pady=5)

        formulario_label_letraPR = tk.Label(self.formulario_frame, text="Letra PR:")
        formulario_label_letraPR.grid(row=0, column=4, padx=10, pady=5)

        self.formulario_texto_letraPR = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_letraPR.grid(row=0, column=5, padx=10, pady=5)

        formulario_label_origenMunicipio = tk.Label(self.formulario_frame, text="Origen Municipio:")
        formulario_label_origenMunicipio.grid(row=1, column=0, padx=10, pady=5)

        self.formulario_texto_origenMunicipio = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_origenMunicipio.grid(row=1, column=1, padx=10, pady=5)

        formulario_label_destinoMunicipio = tk.Label(self.formulario_frame, text="Destino Municipio:")
        formulario_label_destinoMunicipio.grid(row=1, column=2, padx=10, pady=5)

        self.formulario_texto_destinoMunicipio = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_destinoMunicipio.grid(row=1, column=3, padx=10, pady=5)

        formulario_label_cliente = tk.Label(self.formulario_frame, text="Cliente:")
        formulario_label_cliente.grid(row=1, column=4, padx=10, pady=5)

        self.formulario_texto_cliente = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_cliente.grid(row=1, column=5, padx=10, pady=5)

        formulario_label_fechaCarga = tk.Label(self.formulario_frame, text="Fecha Carga:")
        formulario_label_fechaCarga.grid(row=2, column=0, padx=10, pady=5)

        self.formulario_texto_fechaCarga = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_fechaCarga.grid(row=2, column=1, padx=10, pady=5)

        formulario_label_fechaDescarga = tk.Label(self.formulario_frame, text="Fecha Descarga:")
        formulario_label_fechaDescarga.grid(row=2, column=2, padx=10, pady=5)

        self.formulario_texto_fechaDescarga = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_fechaDescarga.grid(row=2, column=3, padx=10, pady=5)

        formulario_label_producto = tk.Label(self.formulario_frame, text="Producto:")
        formulario_label_producto.grid(row=2, column=4, padx=10, pady=5)

        self.formulario_texto_producto = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_producto.grid(row=2, column=5, padx=10, pady=5)

        formulario_label_cartaPorte = tk.Label(self.formulario_frame, text="Carta Porte:")
        formulario_label_cartaPorte.grid(row=3, column=0, padx=10, pady=5)

        self.formulario_texto_cartaPorte = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_cartaPorte.grid(row=3, column=1, padx=10, pady=5)

        formulario_label_litrosCargados = tk.Label(self.formulario_frame, text="Litros Cargados:")
        formulario_label_litrosCargados.grid(row=3, column=2, padx=10, pady=5)

        self.formulario_texto_litrosCargados = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_litrosCargados.grid(row=3, column=3, padx=10, pady=5)

        formulario_label_litrosDescargados = tk.Label(self.formulario_frame, text="Litros Descargados:")
        formulario_label_litrosDescargados.grid(row=3, column=4, padx=10, pady=5)

        self.formulario_texto_litrosDescargados = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_litrosDescargados.grid(row=3, column=5, padx=10, pady=5)

        formulario_label_faltante = tk.Label(self.formulario_frame, text="Faltante:")
        formulario_label_faltante.grid(row=4, column=0, padx=10, pady=5)

        self.formulario_texto_faltante = tk.Text(self.formulario_frame, height=1, width=30)
        self.formulario_texto_faltante.grid(row=4, column=1, padx=10, pady=5)

        formulario_label_tiempoViaje = tk.Label(self.formulario_frame, text="Tiempo de Viaje:")
        formulario_label_tiempoViaje.grid(row=4, column=2, padx=10, pady=5)

        self.formulario_texto_tiempoViaje = tk.Label(self.formulario_frame, text="", fg="black")
        self.formulario_texto_tiempoViaje.grid(row=4, column=3, padx=10, pady=5)

    def filtrar_tabla(self, event=None):
        valor_busqueda = self.busqueda_texto.get()
        self.tabla.selection_remove(self.tabla.selection())
        if valor_busqueda:
            for item in self.tabla.get_children():
                fila = self.tabla.item(item)["values"]
                if valor_busqueda.lower() in [str(valor).lower() for valor in fila]:
                    self.tabla.selection_add(item)

    def calcular_tiempo_viaje(self, fecha_carga, fecha_descarga):
     formato_fecha = "%Y-%m-%dT%H:%M:%S"  # Formato de fecha en tus datos

     fecha_carga = datetime.strptime(str(fecha_carga), formato_fecha)
     fecha_descarga = datetime.strptime(str(fecha_descarga), formato_fecha)

     tiempo_viaje = fecha_descarga - fecha_carga
     dias = tiempo_viaje.days
     horas = tiempo_viaje.seconds // 3600
     minutos = (tiempo_viaje.seconds // 60) % 60

     return f"{dias} días, {horas} horas, {minutos} minutos"


    def calcular_cartas_canceladas(self):
        cartas_canceladas = len(
            [
                fila
                for _, fila in self.df.iterrows()
                if fila["origenMunicipio"] == fila["destinoMunicipio"]
            ]
        )
        return cartas_canceladas

    def mostrar_cartas_faltantes_sobrantes(df):
        cartas_faltantes_sobrantes = [
            {
                "operador": fila["operador"],
                "unidad": fila["unidad"],
                "letraPR": fila["letraPR"],
                "origenMunicipio": fila["origenMunicipio"],
                "destinoMunicipio": fila["destinoMunicipio"],
                "cliente": fila["cliente"],
                "producto": fila["producto"],
                "cartaPorte": fila["cartaPorte"],
                "cancelada": "Yes" if fila["cancelada"] else "No",
                "faltante": fila["faltante"]
            }
            for _, fila in df.iterrows()
            if fila["fechaDescarga"] != 0
        ]

        if cartas_faltantes_sobrantes:
            ventana_cartas_faltantes_sobrantes = tk.Toplevel()
            ventana_cartas_faltantes_sobrantes.title("Cartas Porte Faltantes y Sobrantes")

            tabla_frame = tk.Frame(ventana_cartas_faltantes_sobrantes)
            tabla_frame.pack(fill=tk.BOTH, expand=True)

            tabla_scroll = ttk.Scrollbar(tabla_frame, orient="vertical")
            tabla_scroll.pack(side=tk.RIGHT, fill=tk.Y)

            tabla = ttk.Treeview(tabla_frame, yscrollcommand=tabla_scroll.set)
            tabla_scroll.config(command=tabla.yview)

            columnas = [
                "operador",
                "unidad",
                "letraPR",
                "origenMunicipio",
                "destinoMunicipio",
                "cliente",
                "producto",
                "cartaPorte",
                "cancelada",
                "faltante"
            ]
            tabla["columns"] = columnas

            for columna in columnas:
                tabla.heading(columna, text=columna)

            for carta_porte_data in cartas_faltantes_sobrantes:
                fila_values = [
                    str(carta_porte_data[col]) if not pd.isna(carta_porte_data[col]) else ""
                    for col in columnas[:-2]  # Exclude "cancelada" and "faltante" columns
                ]
                fila_values.append(carta_porte_data["cancelada"])
                fila_values.append(carta_porte_data["faltante"])

                if carta_porte_data["faltante"] < 0:
                    tabla.insert("", tk.END, values=fila_values, tags=("sobrante",))
                elif carta_porte_data["faltante"] > 0:
                    tabla.insert("", tk.END, values=fila_values, tags=("faltante",))
                else:
                    tabla.insert("", tk.END, values=fila_values)

            tabla.tag_configure("sobrante", foreground="green")
            tabla.tag_configure("faltante", foreground="red")

            tabla.pack(fill=tk.BOTH, expand=True)

        else:
            messagebox.showinfo("Cartas Porte Faltantes y Sobrantes", "No hay Cartas Porte Faltantes y Sobrantes para mostrar.")
    pass