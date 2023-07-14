import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
import os
import pandas as pd
from exportar_pdf import exportar_a_pdf

def mostrar_cartas_canceladas(df):
    cartas_canceladas = [
        [
            str(fila["operador"]),
            str(fila["unidad"]),
            str(fila["letraPR"]),
            str(fila["origenMunicipio"]),
            str(fila["destinoMunicipio"]),
            str(fila["cliente"]),
            str(fila["producto"]),
            str(fila["cartaPorte"]),
            "Yes",
        ]
        for _, fila in df.iterrows()
        if fila["origenMunicipio"] == fila["destinoMunicipio"]
    ]
    
    if cartas_canceladas:
        ventana_cartas_canceladas = tk.Toplevel()
        ventana_cartas_canceladas.title("Cartas Porte Canceladas")

        tabla_frame = tk.Frame(ventana_cartas_canceladas)
        tabla_frame.pack(fill=tk.BOTH, expand=True)

        tabla_scroll = tk.Scrollbar(tabla_frame, orient="vertical")
        tabla_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tabla = tk.Listbox(tabla_frame, yscrollcommand=tabla_scroll.set)
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
        tabla.insert(tk.END, "\t".join(columnas))
        tabla.insert(tk.END, "-" * 100)
        
        for fila_values in cartas_canceladas:
            tabla.insert(tk.END, "\t".join(fila_values))
        
        tabla.pack(fill=tk.BOTH, expand=True)

        def exportar_a_pdf_personalizado():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
            )
            if file_path:
                exportar_a_pdf(cartas_canceladas, file_path)

        boton_exportar = tk.Button(
            ventana_cartas_canceladas,
            text="Exportar a PDF",
            command=exportar_a_pdf_personalizado,
        )
        boton_exportar.pack(pady=10)
    else:
        messagebox.showinfo("Cartas Porte Canceladas", "No hay Cartas Porte Canceladas")
