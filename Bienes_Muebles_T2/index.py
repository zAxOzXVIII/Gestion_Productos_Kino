# Proyecto de Trayecto 2
# importando libreria grafica Tkainter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# importando libreria Pillow - convert image
from PIL import ImageTk, Image
# Directorios OS
import os
# libreria de BD MariaDB
import mariadb as mdb


# Clase Primaria
class Window:
    db_name = "bienes_muebles"
    def __init__(self, window):
        self.window = window
        self.window.title("Bienes Muebles Kino Tachira")
        
        # Label Titulo Main
        label_panel = Label(self.window, text="Panel de Usuarios").grid(row=0, column=0, columnspan=2)
        Label(self.window, text="Sesion Administrador").grid(row=1, column=0)
        boton_admin = ttk.Button(self.window, text="Iniciar Sesion").grid(row=1, column=1)
        
        Label(self.window, text="Sesion supervisor").grid(row=2, column=0)
        boton_sup = ttk.Button(self.window, text="Iniciar Sesion", command = self.toplevel_login_sup).grid(row=2, column=1)
        
        Label(self.window, text="Publico").grid(row=3, column=0)
        boton_public = ttk.Button(self.window, text="Ingresar", command=self.public_main).grid(row=3, column=1)
        # Condicion admin
        
        # condicion superviso
        
        # Condicion publica
        
        # test
        
        # Pie de ventana
        self.pie_pagina()
        
    
    def limpiar_ventana(self):
        # limpiando los widgets
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def run_query(self, query, parameters=()):
        try:
            conn = mdb.connect(host="127.0.0.1", user="root", 
                                password="", 
                                database=self.db_name)
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
            fetch = cursor.fetchall()
            return fetch
        except mdb.Error as e:
            message = f"Alert Error: {e}"
            return message
    
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
        # print(self.window.grid_size()) -> imprime la tupla de size
        # label image
        
        lbl_img = Label(self.window, image=img_tk)
        lbl_img.grid(row=num_filas, column=1)
        lbl_img.imagen = img_tk
        
        # Label texto
        texto = "Requerimientos para Graduarse de TSU\nMarden Barrera V-30262472\nElio Sebas V-XXXXX\nDaniela Simanca V-XXXXX"
        copy = Label(self.window, text=texto).grid(row=num_filas, column=0)
        
    def public_main(self):
        # limpiar ventana principal
        self.limpiar_ventana()
        # generar nuevos labels
        title = Label(self.window, text="Digite el codigo del sector de trabajo\ncon el codigo correspondiente ").grid(row=0, column=0)
        self.code = Entry(self.window)
        self.code.grid(row=0, column=1)
        boton_load = ttk.Button(self.window, text="Buscar", command=self.sector_trabajo_query)
        boton_load.grid(row=1, column=0)
        
        # volver al inicio
        num_filas = self.window.grid_size()[1] 
        salir = ttk.Button(self.window, text="Ir al Inicio", command=self.label_main).grid(row=num_filas, column=0, columnspan=2, pady=15)
        
        # pie de ventana
        self.pie_pagina()
    
    def label_main(self):
        # limpiando ventana
        self.limpiar_ventana()
        
        label_panel = Label(self.window, text="Panel de Usuarios").grid(row=0, column=0, columnspan=2)
        Label(self.window, text="Sesion Administrador").grid(row=1, column=0)
        boton_admin = ttk.Button(self.window, text="Iniciar Sesion").grid(row=1, column=1)
        
        Label(self.window, text="Sesion supervisor").grid(row=2, column=0)
        boton_sup = ttk.Button(self.window, text="Iniciar Sesion").grid(row=2, column=1)
        
        Label(self.window, text="Publico").grid(row=3, column=0)
        boton_public = ttk.Button(self.window, text="Ingresar", command=self.public_main).grid(row=3, column=1)
        # pie de ventana
        self.pie_pagina()
    
    def sector_trabajo_query(self):
        # asignando la query sql
        sql = "SELECT nombre_area, id_area FROM areas_trabajo_kino WHERE codigo_zona = ?"
        
        try:
            fetch = self.run_query(sql, (self.code.get(), ))
            # imprimiendo valores
            for row in fetch:
                name = row[0]
                ide = row[1]
        except IndexError as E:
            msg = f"Se ha detectado un error: {E}"
            print(fetch)
            return messagebox.showerror(title="Mensaje del sistema",
                                message=msg)
        
        
        if len(fetch) > 0:
            msg = f"Sector {name}, ID {ide} del area"
            messagebox.showinfo(title="Mensaje del sistema",
                                message=msg)
            # limpiando ventana
            self.limpiar_ventana()
            # imprimiendo pantalla
            self.window_after_query_work(name, ide)
        else:
            messagebox.showerror(title="Mensaje del sistema",
                                    message="No coincide con un codigo de area")
        
    
    def window_after_query_work(self, zona, id):
        # Titulo
        Label(self.window, text=f"Registro de Bienes de {zona}").grid(row=0, column=0, columnspan=2)
        
        # añadiendo formulario
        Label(self.window, text="Digite cantidad de elementos").grid(row=1, column=1)
        self.cantidad = Entry(self.window)
        self.cantidad.grid(row=1, column=0)
        
        Label(self.window, text="Digite cantidad de numero de consulta").grid(row=2, column=1)
        self.num_cons = Entry(self.window)
        self.num_cons.grid(row=2, column=0)
        
        Label(self.window, text="Digite descripcion del item").grid(row=3, column=1)
        self.desc_item = Entry(self.window)
        self.desc_item.grid(row=3, column=0)
        
        Label(self.window, text="Digite valor en Bs").grid(row=4, column=1)
        self.valor = Entry(self.window)
        self.valor.grid(row=4, column=0)
        
        Label(self.window, text="Digite observacion").grid(row=5, column=1)
        self.observ = Entry(self.window)
        self.observ.grid(row=5, column=0)
        
        # Boton guardar data
        guardar = ttk.Button(self.window, text="Subir registro", command= lambda : self.safe_bm_data(id, self.cantidad.get(), self.num_cons.get(),
                                                                                                        self.desc_item.get(), self.valor.get(),
                                                                                                        self.observ.get())).grid(row=6, column=0, columnspan=2)
        # Salir
        num_filas = self.window.grid_size()[1]
        salir = ttk.Button(self.window, text="Ir al Inicio", command=self.label_main).grid(row=num_filas, column=0, columnspan=2, pady=15)
        # pie pagina
        self.pie_pagina()
    
    def safe_bm_data(self, id, cnt, nc, di, vlr, obs):
        sql = """INSERT INTO bienes_por_zona(id_area, cantidad, num_cons, desc_item, valor, observacion)
                VALUES(?, ?, ?, ?, ? ,?)"""
        parameters = (id, cnt, nc, di, vlr, obs)
        self.run_query(sql, parameters)
        # limpiando formulario
        messagebox.showinfo(title="Mensaje del sistema",
                            message="Se subio correctamente los datos")
        
        self.cantidad.delete(0, END)
        self.num_cons.delete(0, END)
        self.desc_item.delete(0, END)
        self.valor.delete(0, END)
        self.observ.delete(0, END)
    
    def toplevel_login_sup(self):
        self.sesion_level = Toplevel()
        self.sesion_level.title("Inicio de sesion del supervisor de area")
        Label(self.sesion_level, text="Sesion de Supervisores").grid(row=0, column=0, columnspan=2)
        Label(self.sesion_level, text="Para verificar si tiene permisos\ncomo supervisor digite su numero de cedula").grid(row=1, column=0)
        ci_sesion = Entry(self.sesion_level)
        ci_sesion.grid(row=1, column=1)
        ttk.Button(self.sesion_level, text="Cargar data", command= lambda: self.sesion_sup_ci(ci_sesion.get())).grid(row=2, column=0, columnspan=2)
    
    def sesion_sup_ci(self, ci):
        query = "SELECT * FROM supervisor_area_kino WHERE cedula = ?"
        parameters = (ci, )
        fetch = self.run_query(query, parameters)
        if(len(fetch)<=0):
            messagebox.showwarning(title="Error en la data",
                                    message="No se encontraron registros con esta cedula")
        else:
            print(f"fetch[0][0] {fetch[0][0]}")
            query2 = "SELECT * FROM supervisor_sesion WHERE id_supervisor = ?"
            parameters2 = (fetch[0][0], )
            fetch2 = self.run_query(query2, parameters2)
            # print(fetch2) -> testeo
            if len(fetch2) <= 0: messagebox.showwarning("Mensaje de sesion", "No tiene permisos para iniciar sesion")
            else:
                messagebox.showinfo(title="Mensaje de sesion",
                                        message=f"El usuario {fetch[0][1]} si tiene permisos, favor digite su contraseña")
                # limpiamos pantalla Top_level
                for widget in self.sesion_level.winfo_children():
                    widget.destroy()
                # Generamos una nueva interfaz para ingresar contraseña
                Label(self.sesion_level, text=f"Digite la contraseña, usuario: {fetch[0][1]}").grid(row=0, column=0, pady=25)
                password_sup = Entry(self.sesion_level)
                password_sup.grid(row=0, column=1, pady=25)
                ttk.Button(self.sesion_level, text="Ingresar", command= lambda : self.log_sesion_sup(password_sup.get())).grid(row=1, column=0, columnspan=2, pady=5)
                
    
    def log_sesion_sup(self, password):
        query = "SELECT id_supervisor, clave_sup FROM supervisor_sesion WHERE clave_sup = ?"
        parameters = (password, )
        fetch = self.run_query(query, parameters)
        print(fetch)
        
        if len(fetch) <= 0:
            messagebox.showwarning("Alerta de contraseña", "No coincide su contraseña con los registros")
        else:
            # asignando id supervisor
            id_sup = fetch[0][0]
            messagebox.showinfo("Mensaje del sistema", "Bienvenido, su sesion a sido verificada con exito")
            self.sesion_level.destroy()
            self.main_sup_panel(id_sup)
    
    def main_sup_panel(self, id_sup):
        # Limpiamos pantalla
        self.limpiar_ventana()
        # Recopilando data del id sesion
        query = "SELECT * FROM supervisor_area_kino WHERE id_supervisor = ?"
        parameters = (id_sup, )
        fetch = self.run_query(query, parameters)
        print(fetch)
        name = fetch[0][1]
        
        Label(self.window, text=f"Supervisor encargado {name}").grid(row=0, column=0, columnspan=5, pady=10, padx=25)
        self.tablero_sup = ttk.Treeview(self.window, height=10)
        # asignando en main window
        self.tablero_sup.grid(row=1, column=0, columnspan=5)
        # entablando heading
        self.tablero_sup["columns"] = ("col0", "col1", "col2", "col3", "col4")
        # asignando valores a las columnas
        self.tablero_sup.heading(column = "col0", text="Cantidad")
        self.tablero_sup.heading(column = "col1", text="Numero de consultas")
        self.tablero_sup.heading(column = "col2", text="Descripcion del item")
        self.tablero_sup.heading(column = "col3", text="Valor")
        self.tablero_sup.heading(column = "col4", text="Observacion")
        # Ajustar columnas al contenido
        for columna in self.tablero_sup["columns"]:
            self.tablero_sup.column(columna, width=100, minwidth=50, anchor=CENTER)
        # Rellenar de datos las filas
        query2 = "SELECT * FROM areas_trabajo_kino WHERE id_supervisor = ?"
        parameters2 = (id_sup, )
        fetch2 = self.run_query(query2, parameters2)
        # asignando valores
        id_area = []
        nombre_area = []
        codigo_zona = []
        for row in fetch2:
            id_area.append(row[0])
            nombre_area.append(row[1])
            codigo_zona.append(row[2])
        # funcion
        self.rellenar_tabla_sup(id_area)
        # Botones
        ttk.Button(self.window, text="Actualizar Datos").grid(row=2, column=0)
        ttk.Button(self.window, text="Generar Codigo Qr").grid(row=2, column=1)
        
    def rellenar_tabla_sup(self, id_area = []):
        # limpiar data
        valores = self.tablero_sup.get_children()
        for elemento in valores:
            self.tablero_sup.delete(elemento)
        # llenando data
        for area in id_area:
            query = "SELECT * FROM bienes_por_zona WHERE id_area = ?"
            parameters = (area, )
            fetch = self.run_query(query, parameters)
            for row in fetch:
                self.tablero_sup.insert("", "end", text=row[0], values=(row[2], row[3], row[4], row[5], row[6]))

# Inicializacion de la interfaz Tk
window = Tk()
# Asignacion de la clase Window al objeto -> instanciacion de objeto
app = Window(window)
# Ciclo de ventana
window.mainloop()