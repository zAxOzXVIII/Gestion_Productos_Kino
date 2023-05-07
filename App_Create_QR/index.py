# Codigo 
import qrcode
from tkinter import *
from tkinter import ttk
import csv

# App
class App_Qr:
    def __init__(self, window):
        # window Principal
        self.window = window
        self.window.title("Qr Codes")
        # LabelFrame
        frame = LabelFrame(self.window, text="Ingresar Data", pady=60, padx=60)
        frame.grid(column=0, row=0, columnspan=3)
        # Code Input
        Label(frame, text="Codigo de producto").grid(column=0, row=0)
        self.code = Entry(frame)
        self.code.grid(column=1, row=0, pady=5)
        # Description Input
        Label(frame, text="Descripcion del producto").grid(column=0, row=1)
        self.desc = Entry(frame)
        self.desc.grid(column=1, row=1, pady=15)
        # Button
        self.button = ttk.Button(frame, text="Guardar", command= lambda : self.save_data())
        self.button.grid(column=0, row=2, columnspan=2, sticky=W + E, pady=25)
        # Tabla
        
        self.tree = ttk.Treeview(self.window, height=10, columns=2)
        self.tree.grid(column=0, row=3, columnspan=2)
        self.tree.heading("#0", text="Code", anchor=CENTER)
        self.tree.heading("#1", text="Description", anchor=CENTER)
        
        # Button _Table
        self.button_table = ttk.Button(self.window, text="Generar Codigo Qr", command= lambda : self.convert_Qr())
        self.button_table.grid(column=0, row=4, columnspan=2, sticky = W+E, pady=5)
        
        # filling tables
        self.get_products()
    
    def save_data(self):
        notes = self.read_data()
        data = []
        # llenando data
        if self.input_vacio():
            data = [self.code.get(), self.desc.get()]
            notes.append(data)
        else: print("Debe llenar las casillas")
        # save new data
        
        with open("Python-Projects\\App_Create_QR\\storage\\almacen\\data.csv", mode="w", newline="") as archive:
            writer = csv.writer(archive, delimiter=",")
            writer.writerows(notes)
        # load page
        self.get_products()
    
    def read_data(self):
        
        with open("Python-Projects\\App_Create_QR\\storage\\almacen\\data.csv", mode="r", newline="") as archive:
            reader = csv.reader(archive, delimiter=",")
            notes = list(reader)
            return notes
    
    def input_vacio(self):
        if ((self.desc.get() != "") & (self.code.get() != "")): return True
        else: return False
    
    def get_products(self):
        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # get data
        notes = self.read_data()
        print(notes)
        for column in range(1, len(notes)):
            self.tree.insert("", 0, text=notes[column][0], values=notes[column][1])
    
    def select_item(self):
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            print("Error no se ha seleccionado ningun dato")
            return
        code = self.tree.item(self.tree.selection())["text"]
        name_image = str(self.tree.item(self.tree.selection())["values"])
        print(code)
        print(self.tree.item(self.tree.selection()))
        return code, name_image
    
    def convert_Qr(self):
        code, name_image= self.select_item()
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=6,
        )
        qr.add_data(code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("Python-Projects\\App_Create_QR\\storage\\images\\img_"+ name_image +".png")


# Objeto
window = Tk()
app = App_Qr(window)
window.mainloop()