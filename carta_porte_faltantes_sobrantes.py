import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def mostrar_cartas_faltantes_sobrantes(df):
    filas_verde = []
    filas_rojo = []

    def toggle_seleccion():
        seleccion = casilla_var.get()
        casilla_var.set(not seleccion)

    def borrar_filas():
        seleccionadas = tabla.selection()
        if seleccionadas:
            confirmacion = messagebox.askyesno(
                "Confirmar eliminación",
                "¿Estás seguro de que deseas eliminar las filas seleccionadas?"
            )
            if confirmacion:
                for item in seleccionadas:
                    tabla.delete(item)
        else:
            messagebox.showinfo("Sin selección", "No se ha seleccionado ninguna fila.")

    def exportar_pdf():
        folder_path = filedialog.askdirectory()
        if folder_path:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialdir=folder_path
            )
            if filename:
                doc = SimpleDocTemplate(filename, pagesize=landscape(letter))

                data = [["Operador", "Unidad", "Letra PR", "Origen", "Destino", "Cliente", "Producto", "Carta Porte", "Faltante"]]
                for item in tabla.get_children():
                    row_data = []
                    for value in tabla.item(item)['values']:
                        if value:
                            row_data.append(value)
                        else:
                            row_data.append("")
                    data.append(row_data)

                # Obtener el ancho disponible de la página
                available_width = doc.width - doc.leftMargin - doc.rightMargin

                # Obtener el número de columnas
                num_columns = len(data[0])

                # Calcular el ancho de cada columna en función del ancho disponible
                column_width = available_width / num_columns

                # Crear la instancia de la tabla con los anchos de columna definidos
                table = Table(data, colWidths=[column_width] * num_columns)
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente al centro
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Cambiar la fuente de la tabla
                    ('FONTSIZE', (0, 1), (-1, -1), 6),  # Cambiar el tamaño de fuente de la tabla
                    ('TOPPADDING', (0, 0), (-1, -1), 8),  # Añadir espacio superior de celda
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Añadir espacio inferior de celda
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Añadir espacio izquierdo de celda
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Añadir espacio derecho de celda
                ])
                table.setStyle(style)

                elements = [table]
                doc.build(elements)

                messagebox.showinfo("Exportación exitosa", f"Los datos se han exportado correctamente a {filename}")
        else:
            messagebox.showinfo("Exportación cancelada", "No se ha seleccionado ninguna ubicación.")

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

        boton_borrar = ttk.Button(
            ventana_cartas_faltantes_sobrantes,
            text="Borrar Filas Seleccionadas",
            command=borrar_filas
        )
        boton_borrar.pack(side=tk.BOTTOM, pady=10)

        boton_exportar = ttk.Button(
            ventana_cartas_faltantes_sobrantes,
            text="Exportar a PDF",
            command=exportar_pdf
        )
        boton_exportar.pack(side=tk.BOTTOM, pady=10)

    else:
        messagebox.showinfo("Cartas Porte Faltantes/Sobrantes", "No hay Cartas Porte Faltantes/Sobrantes para mostrar.")
