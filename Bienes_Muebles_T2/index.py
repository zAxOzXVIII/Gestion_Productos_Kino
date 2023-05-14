# Proyecto de Trayecto 2
# importando libreria grafica Tkainter
from tkinter import *
from tkinter import ttk
# importando libreria Pillow - convert image
from PIL import ImageTk, Image
# Directorios OS
import os


# Clase Primaria
class Window:
    def __init__(self, window):
        self.window = window
        self.window.title("Bienes Muebles Kino Tachira")
        
        # Label Titulo
        label_panel = Label(self.window, text="Panel de Usuarios").grid(row=0, column=0, columnspan=2)
        Label(self.window, text="Sesion Administrador").grid(row=1, column=0)
        boton_admin = ttk.Button(self.window, text="Iniciar Sesion").grid(row=1, column=1)
        
        Label(self.window, text="Sesion supervisor").grid(row=2, column=0)
        boton_sup = ttk.Button(self.window, text="Iniciar Sesion").grid(row=2, column=1)
        
        Label(self.window, text="Publico").grid(row=3, column=0)
        boton_public = ttk.Button(self.window, text="Ingresar").grid(row=3, column=1)
        # test
        
        # Pie de ventana
        self.pie_pagina()
        
    
    def obtener_directorio(self):
        directorio = os.getcwd()
        print("Directorio: ",directorio)
        return directorio
    
    def pie_pagina(self):
        direct = self.obtener_directorio()
        imagen = Image.open(f"{direct}\\Python-Projects\\Bienes_Muebles_T2\\config\\images_ui\\kino_logo.png")
        image_re = imagen.resize((64,64), Image.LANCZOS)
        
        img_tk = ImageTk.PhotoImage(image_re)
        # obtener numero de filas
        num_filas = self.window.grid_size()[1]
        print(self.window.grid_size())
        # label image
        
        lbl_img = Label(self.window, image=img_tk)
        lbl_img.grid(row=num_filas, column=1)
        lbl_img.imagen = img_tk
        
        # Label texto
        texto = "Requerimientos para Graduarse de TSU\nMarden Barrera V-30262472\nElio Sebas V-XXXXX\nDaniela Simanca V-XXXXX"
        copy = Label(self.window, text=texto).grid(row=num_filas, column=0)
        


# Inicializacion de la interfaz Tk
window = Tk()
# Asignacion de la clase Window al objeto -> instanciacion de objeto
app = Window(window)
# Ciclo de ventana
window.mainloop()