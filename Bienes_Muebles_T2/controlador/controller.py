from modelo.model import Model
from tkinter import messagebox
from tkinter import *

class Controlador:
    def __init__(self):
        self.controlador = Model()
        
    def admin_register_control(self,parameters = ()):
        if parameters[0] != "" and parameters[1] != "":
            val = self.controlador.add_admin_registers(parameters)
            if isinstance(val, int):
                messagebox.showinfo("Mensaje del sistema", "Se inserto correctamente")
        else: 
            messagebox.showwarning("Advertencia del sistema", "Rellene formularios al agregar admin")
            return
    
    def admin_deleteW_control(self):
        val = self.controlador.toplevel_admin_deleteW()
        if isinstance(val, int): 
            messagebox.showinfo("Mensaje del sistema", "Se elimino la fila")
            return val
        else: messagebox.showwarning("Advertencia del sistema", val)