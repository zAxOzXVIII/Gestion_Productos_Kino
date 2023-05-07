# Codigo 
import qrcode as qrc
from tkinter import *
from tkinter import ttk
import csv

# App
class App_Qr:
    def __init__(self, window):
        # window
        self.window = window
        self.window.title("Qr Codes")
        # LabelFrame
        frame = LabelFrame(self.window, text="Queso_chedar", pady=100, padx=100)
        frame.grid(column=0, row=0, columnspan=3, pady=5, padx=5)
        # Code Input
        Label(frame, text="Codigo de producto").grid(column=0, row=0)
        self.code = Entry(frame)
        self.code.grid(column=1, row=0, pady=5)
        # Description Input
        Label(frame, text="Descripcion del producto").grid(column=0, row=1)
        self.desc = Entry(frame)
        self.desc.grid(column=1, row=1, pady=15)
        # Button
        self.button = ttk.Button(frame, text="Guardar", command=self.save_data())
        self.button.grid(column=0, row=2, columnspan=2, sticky=W + E)
    
    def save_data(self):
        notes = self.read_data()
        data = []
        # llenando data
        if self.input_vacio():
            data = [self.code.get(), self.desc.get()]
        else: print("Debe llenar las casillas")
        # save new data
        notes.append(data)
        
        with open("Python-Projects\\App_Create_QR\\storage\\almacen\\data.csv", mode="w", newline="") as archive:
            writer = csv.writer(archive, delimiter=",")
            writer.writerows(notes)
    
    def read_data(self):
        
        with open("Python-Projects\\App_Create_QR\\storage\\almacen\\data.csv", mode="r", newline="") as archive:
            reader = csv.reader(archive, delimiter=",")
            notes = list(reader)
            return notes
    
    def input_vacio(self):
        if ((self.desc.get() == "") & (self.code.get() == "")): return False
        else: return True


# Objeto
window = Tk()
app = App_Qr(window)
window.mainloop()