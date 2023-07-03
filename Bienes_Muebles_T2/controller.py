# import model
from view import View
# tkinter library
from tkinter import Tk

class Controller(View):
    def __init__(self, window):
        View.__init__(self, window)

# Proceso principal
if __name__ == "__main__":
    # Inicializacion de la interfaz Tk
    window = Tk()
    # Asignacion de la clase Window al objeto -> instanciacion de objeto
    app = Controller(window)
    # Ciclo de ventana
    window.mainloop()
