import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
from carta_porte_canceladas import mostrar_cartas_canceladas
from carta_porte_faltantes_sobrantes import mostrar_cartas_faltantes_sobrantes
from exportar_pdf import exportar_a_pdf
from aplicacion import Aplicacion

if __name__ == "__main__":
    aplicacion = Aplicacion()
    aplicacion.mainloop()