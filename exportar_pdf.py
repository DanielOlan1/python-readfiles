import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors

def exportar_a_pdf(datos):
    archivo_pdf = "output.pdf"
    doc = SimpleDocTemplate(archivo_pdf, pagesize=letter)

    # Crear una lista para almacenar las filas de la tabla
    tabla_datos = []

    # Agregar encabezados de columna a la tabla
    encabezados = ["Columna 1", "Columna 2", "Columna 3"]
    tabla_datos.append(encabezados)

    # Agregar filas de datos a la tabla
    for fila in datos:
        # Convertir los valores numéricos a cadenas de texto
        fila = [str(cell) for cell in fila]
        fila = [Paragraph(cell, tabla_estilo) for cell in fila]
        tabla_datos.append(fila)

    # Crear la tabla y establecer el estilo
    tabla = Table(tabla_datos)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Generar el documento PDF con la tabla
    doc.build([tabla])
    print(f"Se ha exportado el archivo PDF: {archivo_pdf}")