import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lectura de archivo de Excel")
        self.tabla_frame = None
        self.tabla = None
        self.formulario_frame = None
        self.formulario_texto_operador = None
        self.formulario_texto_unidad = None
        self.formulario_texto = None

        boton_abrir = tk.Button(self, text="Abrir archivo de Excel", command=self.abrir_archivo_excel)
        boton_abrir.pack(pady=10)
        self.geometry("400x300")

    def mostrar_datos(self, event):
        fila_seleccionada = self.tabla.focus()
        datos_fila = self.tabla.item(fila_seleccionada)['values']

        operador = datos_fila[0]  # Obtén el valor de la primera columna (operador)
        unidad = datos_fila[1]  # Obtén el valor de la segunda columna (unidad)
        texto_fila = '\n'.join(str(dato) for dato in datos_fila[2:])  # Resto de las columnas

        self.formulario_texto_operador.delete(1.0, tk.END)  # Limpia el cuadro de texto del operador
        self.formulario_texto_operador.insert(tk.END, operador)  # Inserta el valor del operador

        self.formulario_texto_unidad.delete(1.0, tk.END)  # Limpia el cuadro de texto de la unidad
        self.formulario_texto_unidad.insert(tk.END, unidad)  # Inserta el valor de la unidad

        self.formulario_texto.delete(1.0, tk.END)
        self.formulario_texto.insert(tk.END, texto_fila)

    def abrir_archivo_excel(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx;*.xls")])
        
        if archivo:
            # Cerrar la ventana actual si existe
            if self.tabla_frame:
                self.tabla_frame.destroy()

            # Especificar el motor de lectura de Excel según el formato del archivo
            if archivo.endswith('.xlsx'):
                engine = 'openpyxl'
            elif archivo.endswith('.xls'):
                engine = 'xlrd'
            else:
                raise ValueError("Formato de archivo de Excel no compatible")
            
            df = pd.read_excel(archivo, engine=engine)
            
            # Reemplaza las celdas vacías con ceros
            df.fillna(0, inplace=True)
            
            # Obtiene el nombre de todas las columnas presentes en el archivo
            columnas = df.columns.tolist()
            
            self.tabla_frame = tk.Frame(self)
            self.tabla_frame.pack(fill=tk.BOTH, expand=True)
            
            tabla_scroll = ttk.Scrollbar(self.tabla_frame, orient="horizontal")
            tabla_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            
            self.tabla = ttk.Treeview(self.tabla_frame, xscrollcommand=tabla_scroll.set)
            tabla_scroll.config(command=self.tabla.xview)
            
            self.tabla["columns"] = columnas
            
            # Establece los encabezados de las columnas
            for columna in columnas:
                self.tabla.heading(columna, text=columna)
            
            # Agrega los datos a la tabla
            for i in range(len(df.index)):
                fila = [str(df.iloc[i, j]) if not pd.isna(df.iloc[i, j]) else '0' for j in range(len(df.columns))]
                self.tabla.insert("", tk.END, values=fila)
            
            # Ajusta el ancho de las columnas automáticamente
            for columna in columnas:
                self.tabla.column(columna, width=100, anchor=tk.CENTER)
            
            self.tabla.pack(fill=tk.BOTH, expand=True)
            
            # Ajusta el tamaño de la tabla
            self.tabla.configure(height=4, show="headings")
            
            self.tabla.bind('<ButtonRelease-1>', self.mostrar_datos)
            
            # Cerrar el formulario actual si existe
            if self.formulario_frame:
                self.formulario_frame.destroy()

            # Crea el formulario para mostrar los datos de la fila seleccionada
            self.formulario_frame = tk.Frame(self)
            self.formulario_frame.pack(fill=tk.BOTH, expand=True)
            
            formulario_label_operador = tk.Label(self.formulario_frame, text="Operador:")
            formulario_label_operador.pack(side=tk.TOP)
            
            self.formulario_texto_operador = tk.Text(self.formulario_frame, height=1, width=100)
            self.formulario_texto_operador.pack(side=tk.TOP)
            
            formulario_label_unidad = tk.Label(self.formulario_frame, text="Unidad:")
            formulario_label_unidad.pack(side=tk.TOP)
            
            self.formulario_texto_unidad = tk.Text(self.formulario_frame, height=1, width=100)
            self.formulario_texto_unidad.pack(side=tk.TOP)
            
            formulario_label = tk.Label(self.formulario_frame, text="Datos de la fila seleccionada:")
            formulario_label.pack(side=tk.TOP)
            
            self.formulario_texto = tk.Text(self.formulario_frame, height=10, width=100)
            self.formulario_texto.pack(side=tk.BOTTOM)

if __name__ == '__main__':
    aplicacion = Aplicacion()
    aplicacion.mainloop()
