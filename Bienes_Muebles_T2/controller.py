# import model
from view import View
# tkinter library
from tkinter import Tk

# Proceso principal
if __name__ == "__main__":
    # Inicializacion de la interfaz Tk
    window = Tk()
    # Asignacion de la clase Window al objeto -> instanciacion de objeto
    app = View(window)
    # Ciclo de ventana
    window.mainloop()
