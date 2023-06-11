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
# Libreria Qrcode
import qrcode as qrc
# Importando librerias de tiempo
from datetime import datetime, date, time, timedelta
import calendar


# Clase Primaria
class Window:
    db_name = "bienes_muebles"
    def __init__(self, window):
        self.window = window
        print(type(self.window))
        self.window.title("Bienes Muebles Kino Tachira")
        
        # Label Titulo Main
        label_panel = Label(self.window, text="Panel de Usuarios").grid(row=0, column=0, columnspan=2)
        Label(self.window, text="Sesion Administrador").grid(row=1, column=0)
        boton_admin = ttk.Button(self.window, text="Iniciar Sesion", command = self.toplevel_login_admin).grid(row=1, column=1)
        
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
        
    
    def limpiar_ventana(self, opc = 1):
        # limpiando los widgets
        if opc == 1:
            for widget in self.window.winfo_children():
                widget.destroy()
        elif opc == 2:
            for widget in self.toplevel_admin_window.winfo_children():
                widget.destroy()
    
    def run_query(self, query, parameters=(), opc = 1):
        if opc == 1:
            try:
                conn = mdb.connect(host="127.0.0.1", user="root", 
                                password="", 
                                database=self.db_name)
                cursor = conn.cursor()
                cursor.execute(query, parameters)
                conn.commit()
                fetch = cursor.fetchall()
                print(fetch, "l62")
                return fetch
            except mdb.Error as e:
                message = f"Alert Error: {e}"
                return message
            finally:
                conn.close()
                print("Se ha finalizado la conexion")
        elif opc == 2:
            try:
                conn = mdb.connect(host="127.0.0.1", user="root", 
                                password="", 
                                database=self.db_name)
                cursor = conn.cursor()
                cursor.execute(query, parameters)
                conn.commit()
                rowcount = cursor.rowcount()
                print(rowcount, "l62")
                return rowcount
            except mdb.Error as e:
                message = f"Alert Error: {e}"
                return message
            finally:
                conn.close()
                print("Se ha finalizado la conexion")
    
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
        boton_admin = ttk.Button(self.window, text="Iniciar Sesion", command = self.toplevel_login_admin).grid(row=1, column=1)
        
        Label(self.window, text="Sesion supervisor").grid(row=2, column=0)
        boton_sup = ttk.Button(self.window, text="Iniciar Sesion", command=self.toplevel_login_sup).grid(row=2, column=1)
        
        Label(self.window, text="Publico").grid(row=3, column=0)
        boton_public = ttk.Button(self.window, text="Ingresar", command=self.public_main).grid(row=3, column=1)
        # pie de ventana
        self.pie_pagina()
    
    def sector_trabajo_query(self):
        # asignando la query sql
        sql = "SELECT nombre_area, id_area FROM areas_trabajo_kino WHERE codigo_zona = ?"
        
        try:
            fetch = self.run_query(sql, (self.code.get(), ))
            print(fetch, "l138")
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
        fetch =  self.run_query(sql, parameters)
        
        # limpiando formulario
        if fetch > 0:
            messagebox.showinfo(title="Mensaje del sistema",
                            message="Se subio correctamente los datos")
        else:
            messagebox.showwarning("Advertencia del sistema", "Error al subir la data")
            return
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
        ttk.Button(self.window, text="Actualizar Datos", command = self.up_data_sup).grid(row=2, column=0)
        ttk.Button(self.window, text="Generar Codigo Qr", command = self.create_qr_code).grid(row=2, column=1)
        
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
        
    def up_data_sup(self):
        # Verificamos que seleccione un registro
        try:
            self.tablero_sup.item(self.tablero_sup.selection())["text"]
        except IndexError as e:
            messagebox.showwarning("Advertencia del sistema", "Favor seleccionar un registro para actualizar")
            return
        # Generando variables de tablero
        id_product = self.tablero_sup.item(self.tablero_sup.selection())["text"]
        num_cons = self.tablero_sup.item(self.tablero_sup.selection())["values"][3]
        # Generamos nueva ventana para actualizar data
        self.ventana_act_sup = Toplevel()
        self.ventana_act_sup.title("Actualizar data de registros")
        # Asignando formulario
        Label(self.ventana_act_sup, text="Formulario para actualizar data\ndel registro seleccionado").grid(row=0, column=0, columnspan=2)
        Label(self.ventana_act_sup, text=f"Identificador de la fila seleccionada {id_product}")
        
        Label(self.ventana_act_sup, text="Cantidad").grid(row=1, column=0)
        cnt = Entry(self.ventana_act_sup)
        cnt.grid(row=1, column=1)
        
        Label(self.ventana_act_sup, text="Numero de consultas").grid(row=2, column=0)
        nm_c = Entry(self.ventana_act_sup)
        nm_c.grid(row=2, column=1)
        
        Label(self.ventana_act_sup, text="Descripcion del item").grid(row=3, column=0)
        desc_item = Entry(self.ventana_act_sup)
        desc_item.grid(row=3, column=1)
        
        Label(self.ventana_act_sup, text="Valor").grid(row=4, column=0)
        val = Entry(self.ventana_act_sup)
        val.grid(row=4, column=1)
        
        Label(self.ventana_act_sup, text="Observacion").grid(row=5, column=0)
        obs = Entry(self.ventana_act_sup)
        obs.grid(row=5, column=1)
        # Falta agregar botones, y hacer las consultas update
        # Botones
        ttk.Button(self.ventana_act_sup, text="Actualizar", command= lambda : self.act_data_sup_query(cnt.get(),
                                                                                                        nm_c.get(),
                                                                                                        desc_item.get(),
                                                                                                        val.get(),
                                                                                                        obs.get(),
                                                                                                        id_product,
                                                                                                        num_cons)).grid(row=6, column=0, columnspan=2, pady=15)
        
    def act_data_sup_query(self, cnt, nm_c, desc_item, val, obs, id_b, num_c):
        # update
        query = """UPDATE bienes_por_zona SET cantidad = ?, num_cons = ?, desc_item = ?, valor = ?, observacion = ?
                WHERE id_bienes = ? AND numero_cons = ?"""
        parameters = (cnt, nm_c, desc_item, val, obs, id_b, num_c, )
        # Pregunta de verificacion
        quest = messagebox.askyesno(title = "Consulta del sistema", message="Esta seguro que desea modificar los valores?\nNo hay control 'Z' para esta acción")
        if quest:
            fetch = self.run_query(query, parameters)
            print(fetch)
            if len(fetch) <= 0:
                messagebox.showinfo("Mensaje del sistema", "Todo salio correcto")
            else: messagebox.showwarning("Mensaje del sistema", "Se ha detectado un error")
        else:
            messagebox.showinfo("Mensaje del sistema", "Correcto se revirtio la accion")
            return
        
    def create_qr_code(self):
        # Seleccionando valores
        try:
            self.tablero_sup.item(self.tablero_sup.selection())["text"]
        except IndexError as E:
            messagebox.showinfo("Mensaje del sistema", "No se a seleccionado ningun registro")
            return
        # asignando valores a variables de la tabla
        id_b = self.tablero_sup.item(self.tablero_sup.selection())["text"]
        num_c = self.tablero_sup.item(self.tablero_sup.selection())["values"][1]
        cnt = self.tablero_sup.item(self.tablero_sup.selection())["values"][0]
        val = self.tablero_sup.item(self.tablero_sup.selection())["values"][3]
        
        fecha = datetime.now()
        fecha_m = f"{fecha.year}_{fecha.month}_{fecha.day}"
        
        name_code = f"ID_B{id_b}NM_C{num_c}C{cnt}V{val}"
        name_img = f"IMG_Code_ID{id_b}_{fecha_m}"
        qr = qrc.QRCode(
            version=5,
            error_correction=qrc.constants.ERROR_CORRECT_L,
            box_size=15,
            border=6,
        )
        qr.add_data(name_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(self.obtener_directorio() + "\\Python-Projects\\Bienes_Muebles_T2\\config\\images_Qr\\" + name_img + ".png")
        
    # Inicializacion de Administrador
    def toplevel_login_admin(self):
        self.toplevel_admin = Toplevel()
        self.toplevel_admin.title("Sesion de Administrador")
        #  planteando sesion de administrador
        Label(self.toplevel_admin, text="Inicia como administrador").grid(row=0, column=0, columnspan=2, pady=10)
        Label(self.toplevel_admin, text="Ingresa\nUsuario").grid(row=1, column=0)
        user_adm = Entry(self.toplevel_admin)
        user_adm.grid(row=1, column=1, padx=5)
        # password
        Label(self.toplevel_admin, text="Ingrese\nContraseña").grid(row=2, column=0)
        password_adm = Entry(self.toplevel_admin)
        password_adm.grid(row=2, column=1, padx=5)
        # button
        ttk.Button(self.toplevel_admin, text="Ingresar", command = lambda : self.log_adm_sesion(user_adm.get(), password_adm.get())).grid(row=3, column=0, columnspan=2, pady=10)
        # pie de pagina
        self.pie_pagina()
    
    def log_adm_sesion(self, user, password):
        query = "SELECT * FROM administrador WHERE usuario = ? AND clave = ?"
        parameters = (user, password, )
        fetch = self.run_query(query, parameters)
        print(fetch)
        if len(fetch) <= 0:
            print("Contraseña incorrecta")
            return
        else:
            # asignando valores
            for u in fetch:
                if user == u[1]: name_u = u[1]
            messagebox.showinfo("Mensaje del sistema", "Bienvenido, se verifico con exito")
            self.toplevel_admin.destroy()
            self.limpiar_ventana()
            # generando ventana admin
            self.w_admin_main(name_u)
    
    def w_admin_main(self, user):
        # Asignando a main
        # self.window.geometry("200x200")
        # Mensajes label
        Label(self.window, text=f"Bienvenido {user}").grid(row=0, column=0, columnspan=3, pady=15)
        # Mostrando los supervisores en turno
        Label(self.window, text="Tabla informativa").grid(row=1, column=0, padx=5)
        self.admin_table_sup = ttk.Treeview(self.window, height=10)
        # Asignando lugar
        self.admin_table_sup.grid(row=1, column=1, columnspan=2, padx=5)
        # especificando columnas
        self.admin_table_sup["columns"] = ("c1", "c2", "c3")
        # Asignando nombres a las columnas
        self.admin_table_sup.heading(column= "c1", text="Nombre")
        self.admin_table_sup.heading(column= "c2", text="Apellido")
        self.admin_table_sup.heading(column= "c3", text="Cedula")
        # Ajustar columnas al contenido
        for columna in self.admin_table_sup["columns"]:
            self.admin_table_sup.column(columna, width=100, minwidth=50, anchor=CENTER)
        # Llenando tabla
        self.fill_admin_table_sup()
        # Botones
        ttk.Button(self.window, text="Agregar supervisor", command = lambda : self.topLevel_admin_interface_add()).grid(row=2, column=0)
        ttk.Button(self.window, text="Modificar Supervisor", command = lambda : self.topLevel_admin_interface_update()).grid(row=2, column=1)
        ttk.Button(self.window, text="Eliminar Supervisor", command = lambda : self.topLevel_admin_interface_delete()).grid(row=2, column=2)
        # Consultar usuarios admin
        Label(self.window, text="Consultar sobre los usuarios admin disponibles").grid(row=3, column=1, columnspan=2, pady=15)
        ttk.Button(self.window, text="Usuarios Admin", command = self.topLevel_admin_i).grid(row=3, column=0, pady= 15)
        # pie de pagina
        self.pie_pagina()
    
    def fill_admin_table_sup(self, busqueda = (), w_quest = "1"):
        # limpiamos tabla
        records = self.admin_table_sup.get_children()
        print (records)
        for element in records:
            self.admin_table_sup.delete(element)
        
        busqueda_personalizada = f"{w_quest}"
        print(busqueda, "\n", busqueda_personalizada)
        if len(busqueda) <= 0:
            query = f"SELECT * FROM supervisor_area_kino WHERE {busqueda_personalizada}"
            fetch = self.run_query(query)
            for row in fetch:
                self.admin_table_sup.insert("", "end", text=row[0], values = (row[1], row[2], row[3]))
        else:
            for data in busqueda:
                valor = busqueda_personalizada + data
                print(valor)
                query = f"SELECT * FROM supervisor_area_kino WHERE {valor}"
                fetch = self.run_query(query)
                for row in fetch:
                    self.admin_table_sup.insert("", "end", text=row[0], values = (row[1], row[2], row[3]))
                
    # Consulta si se ha seleccionado una fila de la tabla de supervisores
    def select_admin_table_sup(self):
        try:
            self.admin_table_sup.item(self.admin_table_sup.selection())["text"]
        except IndexError as e:
            messagebox.showwarning("Advertencia del sistema", e)
            return
        
        name = self.admin_table_sup.item(self.admin_table_sup.selection())["values"][0]
        last_name = self.admin_table_sup.item(self.admin_table_sup.selection())["values"][1]
        dni = self.admin_table_sup.item(self.admin_table_sup.selection())["values"][2]
        return (name, last_name, dni)
    
    def topLevel_admin_interface_update(self):
        update_window = Toplevel()
        update_window.title("Agregar datos ventana")
        # Datos anteriores
        old_data = self.select_admin_table_sup()
        if len(old_data) <= 0:
            messagebox.showwarning("Advertencia del sistema", "Se debe seleccionar un registro")
            return
        
        # agregando labels
        Label(update_window, text=f"Antigua información : {old_data[0]}").grid(row=0, column=0)
        Label(update_window, text="Nombre del supervisor\nQue se actualizará").grid(row=1, column=0)
        name = Entry(update_window)
        name.grid(row=1, column=1)
        
        Label(update_window, text=f"Antigua información : {old_data[1]}").grid(row=2, column=0)
        Label(update_window, text="Apellido del supervisor\nQue se actualizará").grid(row=3, column=0)
        last_name = Entry(update_window)
        last_name.grid(row=3, column=1)
        
        Label(update_window, text=f"Antigua información : {old_data[2]}").grid(row=4, column=0)
        Label(update_window, text="Cedula del supervisor\nQue se actualizará").grid(row=5, column=0)
        dni = Entry(update_window)
        dni.grid(row=5, column=1)
        
        # query
        ttk.Button(update_window, text="Actualizar", command = lambda: self.admin_query_customThree(2, old_data,
                                                                                                        (name.get(), last_name.get(), dni.get()))).grid(row= 6, column=0, columnspan=2)
        # pie de pagina
        self.pie_pagina()
    
    def admin_query_customThree(self, opc : int, old_info = (), new_info = ()):
        # imprimiendo valores
        print("Valores old_info L533", old_info)
        print("Valores new_info L534", new_info)
        if opc == 1:
            query = "INSERT INTO supervisor_area_kino(nombre, apellido, cedula) VALUES(?, ?, ?)"
            fetch = self.run_query(query, new_info)
            if len(fetch) <= 0:
                print("la insercion salio bien")
            else: print(fetch)
        elif opc == 2:
            query = f"UPDATE supervisor_area_kino SET nombre = ?, apellido = ?, cedula = ? WHERE nombre = {old_info[0]} AND cedula = {old_info[2]}"
            fetch = self.run_query(query, new_info)
            if len(fetch) <= 0: print("el update salio bien", fetch)
        elif opc == 3:
            query = f"DELETE FROM supervisor_area_kino WHERE nombre = ? AND apellido = ? AND cedula = ?"
            fetch = self.run_query(query, old_info)
            print(fetch, "Mensaje L555")
        
    
    def topLevel_admin_interface_add(self):
        # ventana add
        add_window = Toplevel()
        print(type(add_window))
        add_window.title("Ventana de agregar")
        # Labels
        Label(add_window, text="Nombre del supervisor nuevo").grid(row=0, column=0)
        name = Entry(add_window)
        name.grid(row=0, column=1)
        
        Label(add_window, text="Apellido del supervisor nuevo").grid(row=1, column=0)
        last_name = Entry(add_window)
        last_name.grid(row=1, column=1)
        
        Label(add_window, text="Cedula del supervisor nuevo").grid(row=2, column=0)
        dni = Entry(add_window)
        dni.grid(row=2, column=1)
        # data
        # boton
        btn = ttk.Button(add_window, text="Agregar valores", command = lambda : self.admin_query_customThree(1, (),
                                                                                                                (name.get(), last_name.get(), dni.get())))
        btn.grid(row=3, column = 0, columnspan=2)
    
    def topLevel_admin_interface_delete(self):
        # Llamando query para eliminar data
        select_data = self.select_admin_table_sup()
        if len(select_data) > 0: 
            if messagebox.askyesno("Pregunta del sistema", f"Esta seguro de eliminar el registro {select_data}"):
                self.admin_query_customThree(3, old_info = select_data)
        else:
            messagebox.showwarning("Advertencia del sistema", "Error, debe seleccionar una fila")
            return
        # Actualizando tabla
        self.fill_admin_table_sup()
        
    
    def topLevel_admin_i(self):
        self.toplevel_admin_window = Toplevel()
        self.toplevel_admin_window.title("Panel de admins")
        # limpiar ventana
        self.limpiar_ventana(opc = 2)
        # Labels
        Label(self.toplevel_admin_window, text= "Administradores disponibles").grid(row= 0, column=0, columnspan=2)
        # Tabla
        self.table_admin_data = ttk.Treeview(self.toplevel_admin_window, height=10)
        # asignando a grilla
        self.table_admin_data.grid(row=1, column=0, columnspan=2)
        # columnas
        self.table_admin_data["columns"] = ("col0", "col1")
        # asignando
        self.table_admin_data.heading(column = "col0", text = "Usuario")
        self.table_admin_data.heading(column = "col1", text = "Contraseña")
        # asignando espacio
        
        # asignando valores a las filas de la tabla admins
        self.fill_admin_table()
        # Botones
        ttk.Button(self.toplevel_admin_window, text="Agregar", command = self.toplevel_admin_addW).grid(row=2, column=0)
        ttk.Button(self.toplevel_admin_window, text="Eliminar", command = self.toplevel_admin_deleteW).grid(row=2, column=1)
        
    
    def fill_admin_table(self):
        # limpiamos tabla
        records = self.table_admin_data.get_children()
        print (records)
        for element in records:
            self.table_admin_data.delete(element)
        
        query = "SELECT * FROM administrador"
        fetch = self.run_query(query)
        print(fetch, type(fetch))
        if isinstance(fetch, list):
            for row in fetch:
                self.table_admin_data.insert("", "end", text=row[0], values = (row[1], row[2]))
        else: messagebox.showwarning("Advertencia del sistema", fetch)
    
    def toplevel_admin_addW(self):
        # Limpiar ventana
        self.limpiar_ventana(opc = 2)
        # Formulario
        Label(self.toplevel_admin_window, text="Ingresar Usuario").grid(row=0, column=0)
        user = ttk.Entry(self.toplevel_admin_window)
        user.grid(row=0, column=1)
        Label(self.toplevel_admin_window, text="Ingresar Contraseña").grid(row=1, column=0)
        password = ttk.Entry(self.toplevel_admin_window)
        password.grid(row=1, column=1)
        # Volver
        ttk.Button(self.toplevel_admin_window, text="Volver", command = self.topLevel_admin_i).grid(row=2, column=0)
        # Agregar
        ttk.Button(self.toplevel_admin_window, text="Subir", command = lambda : self.add_admin_registers(user.get(),
                                                                                                            password.get())).grid(row=2, column=1)
    
    def add_admin_registers(self, parameters = ()):
        query = "INSERT INTO administrador(usuario, contraseña) VALUES(?, ?)"
        rowcount = self.run_query(query, parameters, 2)
        print("Numero de filas apectadas {rowcount}".format(rowcount))
    
    def toplevel_admin_deleteW(self):
        try:
            self.table_admin_data.item(self.table_admin_data.selection())["text"]
        except IndexError as e:
            messagebox.showwarning("Advertencia del sistema", e)
            return
        
        user = self.table_admin_data.item(self.table_admin_data.selection())["values"][0]
        password = self.table_admin_data.item(self.table_admin_data.selection())["values"][1]
        old_data = (user, password)
        
        query = "DELETE FROM administrador WHERE usuario = ? AND contraseña = ?"
        rowcount = self.run_query(query, old_data, 2)
        if isinstance(rowcount, int): messagebox.showinfo("Mensaje del sistema", f"Se borraron: {rowcount} registros correctamente")

# Proceso principal
if __name__ == "__main__":
    # Inicializacion de la interfaz Tk
    window = Tk()
    # Asignacion de la clase Window al objeto -> instanciacion de objeto
    app = Window(window)
    # Ciclo de ventana
    window.mainloop()