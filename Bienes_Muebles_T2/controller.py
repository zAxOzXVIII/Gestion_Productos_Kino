from model import Model
from view import View
# f
from tkinter import Tk

class Controller(Model, View):
    def __init__(self, window):
        self.window = window
        View.__init__(self, self.window)

# Proceso principal
if __name__ == "__main__":
    # Inicializacion de la interfaz Tk
    window = Tk()
    # Asignacion de la clase Window al objeto -> instanciacion de objeto
    app = Controller(window)
    # Ciclo de ventana
    window.mainloop()