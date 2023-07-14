import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

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
