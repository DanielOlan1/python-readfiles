import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pandasgui import show

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lectura de archivo de Excel")

        boton_abrir = tk.Button(self, text="Abrir archivo de Excel", command=self.abrir_archivo_excel)
        boton_abrir.pack()

    def abrir_archivo_excel(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx;*.xls")])
        
        if archivo:
            # Leer el archivo de Excel en un DataFrame
            df = pd.read_excel(archivo)
            
            # Crear una ventana de pandasgui con el DataFrame
            gui = show(df)

if __name__ == '__main__':
    aplicacion = Aplicacion()
    aplicacion.mainloop()
