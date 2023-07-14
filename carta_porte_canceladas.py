import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import pandas as pd
from exportar_pdf import exportar_a_pdf

def mostrar_cartas_canceladas(df):
    cartas_canceladas = [
        {
            "operador": fila["operador"],
            "unidad": fila["unidad"],
            "letraPR": fila["letraPR"],
            "origenMunicipio": fila["origenMunicipio"],
            "destinoMunicipio": fila["destinoMunicipio"],
            "cliente": fila["cliente"],
            "producto": fila["producto"],
            "cartaPorte": fila["cartaPorte"],
            "cancelada": "Yes",
        }
        for _, fila in df.iterrows()
        if fila["origenMunicipio"] == fila["destinoMunicipio"]
    ]
    if cartas_canceladas:
        ventana_cartas_canceladas = tk.Toplevel()
        ventana_cartas_canceladas.title("Cartas Porte Canceladas")

        tabla_frame = tk.Frame(ventana_cartas_canceladas)
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
        ]
        tabla["columns"] = columnas

        for columna in columnas:
            tabla.heading(columna, text=columna)

        for carta_porte_data in cartas_canceladas:
            fila_values = [
                str(carta_porte_data[col]) if not pd.isna(carta_porte_data[col]) else ""
                for col in columnas[:-1]
            ]  # Exclude the "cancelada" column
            fila_values.append("cancelada")
            tabla.insert("", tk.END, values=fila_values, tags=("cancelada",))

        tabla.tag_configure("cancelada", foreground="red")  # Configure red color for rows with the "cancelada" tag

        tabla.pack(fill=tk.BOTH, expand=True)

        boton_exportar = tk.Button(
            ventana_cartas_canceladas,
            text="Exportar a PDF",
            command=lambda: exportar_a_pdf(cartas_canceladas),
        )
        boton_exportar.pack(pady=10)
    else:
        messagebox.showinfo("Cartas Porte Canceladas", "No hay Cartas Porte Canceladas")
