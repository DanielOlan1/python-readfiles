import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

def mostrar_cartas_faltantes_sobrantes(df):
    filas_verde = []
    filas_rojo = []

    def toggle_seleccion():
        seleccion = casilla_var.get()
        casilla_var.set(not seleccion)

    for _, fila in df.iterrows():
        if fila["fechaDescarga"] != 0 and fila["faltante"] != fila["litrosCargados"]:
            carta_porte_data = {
                "operador": fila["operador"],
                "unidad": fila["unidad"],
                "letraPR": fila["letraPR"],
                "origenMunicipio": fila["origenMunicipio"],
                "destinoMunicipio": fila["destinoMunicipio"],
                "cliente": fila["cliente"],
                "producto": fila["producto"],
                "cartaPorte": fila["cartaPorte"],
                "faltante": fila["faltante"]
            }

            if carta_porte_data["faltante"] <= 0:
                filas_verde.append(carta_porte_data)
            else:
                filas_rojo.append(carta_porte_data)

    cartas_faltantes_sobrantes = filas_verde + filas_rojo

    if cartas_faltantes_sobrantes:
        ventana_cartas_faltantes_sobrantes = tk.Toplevel()
        ventana_cartas_faltantes_sobrantes.title("Cartas Porte Faltantes/Sobrantes")

        casilla_var = tk.BooleanVar()
        casilla_checkbutton = tk.Checkbutton(
            ventana_cartas_faltantes_sobrantes,
            text="A Sisa",
            variable=casilla_var,
            onvalue=True,
            offvalue=False,
            command=toggle_seleccion
        )
        casilla_checkbutton.pack()

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
            "faltante"
        ]
        tabla["columns"] = columnas

        for columna in columnas:
            tabla.heading(columna, text=columna)

        for carta_porte_data in cartas_faltantes_sobrantes:
            fila_values = [
                carta_porte_data[col] if not pd.isna(carta_porte_data[col]) else ""
                for col in columnas
            ]
            faltante = carta_porte_data["faltante"]
            if faltante <= 0:
                tabla.insert("", tk.END, values=fila_values, tags=("verde",))
            else:
                tabla.insert("", tk.END, values=fila_values, tags=("rojo",))

        tabla.tag_configure("verde", foreground="green")
        tabla.tag_configure("rojo", foreground="red")

        tabla.pack(fill=tk.BOTH, expand=True)

    else:
        messagebox.showinfo("Cartas Porte Faltantes/Sobrantes", "No hay Cartas Porte Faltantes/Sobrantes para mostrar.")
