# exportar_pdf.py

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def exportar_a_pdf(datos, file_path):
    # Crear el documento PDF con tamaño de página en formato horizontal
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))

    # Crear la tabla con los datos
    tabla_datos = datos

    # Obtener el estilo de párrafo para los encabezados de columna
    styles = getSampleStyleSheet()
    estilo_encabezado = styles['Heading2']

    # Agregar los nombres de las columnas a la tabla como párrafos con estilo de encabezado
    nombres_columnas = ['Operador', 'Unidad', 'Letra PR', 'Origen Municipio', 'Destino Municipio', 'Cliente', 'Producto', 'Carta Porte']
    encabezados = [Paragraph(nombre, estilo_encabezado) for nombre in nombres_columnas]
    tabla_datos.insert(0, encabezados)

    # Definir el estilo de la tabla
    tabla_estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Crear la tabla y aplicar el estilo
    tabla = Table(tabla_datos)
    tabla.setStyle(tabla_estilo)

    # Generar el documento PDF con la tabla
    elementos = [tabla]
    doc.build(elementos)

    print(f"Se ha exportado el archivo PDF: {file_path}")
