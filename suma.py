import tkinter as tk
from tkinter import filedialog

def abrir_archivo_excel():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx;*.xls")])
    
    if archivo:
        df = pd.read_excel(archivo)
        
        ventana = tk.Tk()
        ventana.title("Contenido del archivo Excel")
        
        texto = tk.Text(ventana)
        texto.pack(fill=tk.BOTH, expand=True)  # Hace que el widget de texto se ajuste al tamaño de la ventana
        
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                celda = str(df.iloc[i, j])
                texto.insert(tk.END, celda + "\t")
            texto.insert(tk.END, "\n")
        
        ventana.mainloop()

ventana_principal = tk.Tk()
ventana_principal.title("Lectura de archivo de Excel")

boton_abrir = tk.Button(ventana_principal, text="Abrir archivo de Excel", command=abrir_archivo_excel)
boton_abrir.pack()

ventana_principal.mainloop()
