import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors

def dividir_texto(texto, longitud_maxima):
    palabras = texto.split()
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        if len(linea_actual) + len(palabra) <= longitud_maxima:
            linea_actual += " " + palabra
        else:
            lineas.append(linea_actual.strip())
            linea_actual = palabra
    lineas.append(linea_actual.strip())
    return lineas


def mostrar_cartas_faltantes_sobrantes(df):
    filas_verde = []
    filas_rojo = []

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

                data_verde = [["Operador Sin Faltantes"]]
                data_rojo = [["Operador con Faltante"]]

                for item in tabla.get_children():
                    row_data = []
                    for value in tabla.item(item)['values']:
                        if value:
                            row_data.append(value)
                        else:
                            row_data.append("N/A")  # Valor predeterminado para celdas vacías

                    try:
                        faltante = float(row_data[-1])
                        if faltante <= 0:
                            data_verde.append(row_data)
                        else:
                            data_rojo.append(row_data)
                    except ValueError:
                        # Manejo de valores no numéricos
                        pass

                available_width = doc.width - doc.leftMargin - doc.rightMargin

                column_width = available_width / len(columnas)

                table_verde = Table(data_verde, colWidths=[column_width] * len(columnas))
                table_rojo = Table(data_rojo, colWidths=[column_width] * len(columnas))

                # Estilo para celdas positivas (verdes)
                estilo_verde = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.red, colors.transparent),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('WRAP', (0, 1), (-1, -1), True),  # Ajustar el contenido de las celdas
                    ('LEADING', (0, 0), (-1, -1), 12),  # Espacio adicional entre líneas de texto
                ])

                # Estilo para celdas negativas (rojas)
                estilo_rojo = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.red),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.red, colors.transparent),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('WRAP', (0, 1), (-1, -1), True),  # Ajustar el contenido de las celdas
                    ('LEADING', (0, 0), (-1, -1), 12),  # Espacio adicional entre líneas de texto
                ])

                table_verde.setStyle(estilo_verde)
                table_rojo.setStyle(estilo_rojo)

                elements = [table_verde, Spacer(0, 10), table_rojo]
                doc.build(elements)

                messagebox.showinfo("Exportación exitosa", f"Los datos se han exportado correctamente a {filename}")
        else:
            messagebox.showinfo("Exportación cancelada", "No se ha seleccionado ninguna ubicación.")
    df = df.sort_values(by="faltante", ascending=False)
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

        # Configurar el ancho de las columnas
        column_widths = [300, 300, 300, 300, 300, 300, 700, 300, 300]

        for i, columna in enumerate(columnas):
            tabla.column(columna, width=column_widths[i], anchor=tk.W, stretch=tk.NO)

        for columna in columnas:
            tabla.heading(columna, text=columna)

        for carta_porte_data in cartas_faltantes_sobrantes:
            fila_values = []
            for col in columnas:
                valor = carta_porte_data[col]
                if not pd.isna(valor):
                    valor = str(valor)  # Convertir a cadena
                    if len(valor) > 8:
                        lineas = dividir_texto(valor, 10)
                        fila_values.append("\n".join(lineas))
                    else:
                        fila_values.append(valor)
                else:
                    fila_values.append("")
            faltante = carta_porte_data["faltante"]
            if faltante <= 0:
                tabla.insert("", tk.END, values=fila_values, tags=("verde",))
            else:
                tabla.insert("", tk.END, values=fila_values, tags=("rojo",))
            tabla_scroll.config(command=tabla.yview)

        tabla_scroll.config(command=tabla.yview)    
        tabla.pack(fill=tk.BOTH, expand=True)
        tabla.configure(yscrollcommand=tabla_scroll.set)
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

