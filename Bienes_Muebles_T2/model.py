# Directorios OS
import os
# libreria de BD MariaDB
import mariadb as mdb
# Libreria Qrcode
import qrcode as qrc
# Importando librerias de tiempo
from datetime import datetime, date, time, timedelta
import calendar
# importando el modulo de hash que genera diferentes tipos, usaremos md5
import hashlib as hhl
# tkinter message
from tkinter import messagebox, END
# importando libreria vista
# from view import View

class Model():
    # Funciones
    
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
                print(fetch, "l69")
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
                rowcount = cursor.rowcount #Arreglado
                print(rowcount, "l86")
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
    
    def safe_bm_data(self, id, cnt, nc, di, vlr, obs):
        sql = """INSERT INTO bienes_por_zona(id_area, cantidad, num_cons, desc_item, valor, observacion)
                VALUES(?, ?, ?, ?, ? ,?)"""
        parameters = (id, cnt, nc, di, vlr, obs)
        fila =  self.run_query(sql, parameters, 2)
        
        # limpiando formulario
        if isinstance(fila, int):
            messagebox.showinfo(title="Mensaje del sistema",
                            message=f"Se subio correctamente los datos, {fila}")
        else:
            messagebox.showwarning("Advertencia del sistema", "Error al subir la data")
            return
        self.cantidad.delete(0, END)
        self.num_cons.delete(0, END)
        self.desc_item.delete(0, END)
        self.valor.delete(0, END)
        self.observ.delete(0, END)
    
    def log_sesion_sup(self, password):
        query = "SELECT id_supervisor, clave_sup FROM supervisor_sesion WHERE clave_sup = ?"
        parameters = (password, )
        fetch = self.run_query(query, parameters)
        print(fetch)
        
        if isinstance(fetch, str) == True:
            messagebox.showwarning("Alerta de contraseña", "No coincide su contraseña con los registros")
        else:
            # asignando id supervisor
            id_sup = fetch[0][0]
            messagebox.showinfo("Mensaje del sistema", "Bienvenido, su sesion a sido verificada con exito")
            self.sesion_level.destroy()
            self.main_sup_panel(id_sup)
    
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
    
    def act_data_sup_query(self, cnt, nm_c, desc_item, val, obs, id_b, num_c):
        # update
        query = """UPDATE bienes_por_zona SET cantidad = ?, num_cons = ?, desc_item = ?, valor = ?, observacion = ?
                WHERE id_bienes = ?"""
        parameters = (cnt, nm_c, desc_item, val, obs, id_b, )
        # Pregunta de verificacion
        quest = messagebox.askyesno(title = "Consulta del sistema", message="Esta seguro que desea modificar los valores?\nNo hay control 'Z' para esta acción")
        if quest:
            fila = self.run_query(query, parameters, 2)
            print(fila)
            if isinstance(fila, int):
                messagebox.showinfo("Mensaje del sistema", f"Todo salio correcto\n se actualizaron {fila} filas")
            else: messagebox.showwarning("Mensaje del sistema", f"Se ha detectado un error: {fila}")
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
        
        try:
            fecha = datetime.now()
            fecha_m = f"{fecha.year}_{fecha.month}_{fecha.day}"
            
            name_code = f"ID_B{id_b}NM_C{num_c}C{cnt}V{val}"
            # tupla que guardara informacion para la query del QR que se subira a la tabla
            data_query = (name_code, str(id_b), str(cnt))
            # query
            self.up_qrcode_table(data_query)
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
            img.save(self.obtener_directorio() + "\\Python-Projects\\Gestion_Productos_Kino-main\\Bienes_Muebles_T2\\config\\images_Qr\\" + name_img + ".png")
        except Exception as e:
            print(e)
            return
    
    def up_qrcode_table(self, parameters = ()):
        query="UPDATE bienes_por_zona SET codigo_qr = ? WHERE id_bienes = ? AND cantidad = ?"
        filas = self.run_query(query, parameters, opc = 2)
        if isinstance(filas, int): messagebox.showinfo("Mensaje del sistema", f"Se actualizaron {filas}")
        else: print(filas)
    
    def log_adm_sesion(self, user, password):
        query = "SELECT * FROM administrador WHERE usuario = ? AND clave = ?"
        parameters = (user, password, )
        fetch = self.run_query(query, parameters)
        print(fetch)
        if isinstance(fetch, str) == True:
            print("Contraseña incorrecta L474")
            messagebox.showwarning("Advertencia del sistema", f"Contraseña incorrecta")
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
    
    def admin_query_customThree(self, opc : int, old_info = (), new_info = ()):
        # imprimiendo valores
        print("Valores old_info L533", old_info)
        print("Valores new_info L534", new_info)
        # convertir valores a string
        if opc == 1:
            query = "INSERT INTO supervisor_area_kino(nombre, apellido, cedula) VALUES(?, ?, ?)"
            fila = self.run_query(query, new_info, 2)
            if isinstance(fila, int) == True:
                print("la insercion salio bien L-593")
            else: print(fila)
        elif opc == 2:
            query = f"UPDATE supervisor_area_kino SET nombre = ?, apellido = ?, cedula = ? WHERE nombre = {old_info[0]} AND cedula = {old_info[2]}"
            fila = self.run_query(query, new_info, 2)
            if isinstance(fila, int) == True: print("el update salio bien L-598", fila)
            else: print(fila)
        elif opc == 3:
            query = f"DELETE FROM supervisor_area_kino WHERE nombre = ? AND apellido = ? AND cedula = ?"
            fila = self.run_query(query, old_info, 2)
            if isinstance(fila, int) == True:
                print(fila, "El delete salio bien L-604")
            else: print(fila)
    
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
                # Debemos proteger la contraseña por lo que la incriptaremos
                md5 = hhl.md5(row[2].encode())
                hash_md5 = md5.hexdigest()
                self.table_admin_data.insert("", "end", text=row[0], values = (row[1], hash_md5))
        else: messagebox.showwarning("Advertencia del sistema", fetch)
    
    def add_admin_registers(self, parameters = ()):
        query = "INSERT INTO administrador(usuario, clave) VALUES(?, ?)"
        rowcount = self.run_query(query, parameters, 2)
        print("Numero de filas apectadas {rowcount}".format(rowcount))
    # query para borrar administrador ->modelo
    def toplevel_admin_deleteW(self):
        try:
            self.table_admin_data.item(self.table_admin_data.selection())["text"]
        except IndexError as e:
            messagebox.showwarning("Advertencia del sistema", e)
            return
        
        id_admin = self.table_admin_data.item(self.table_admin_data.selection())["text"]
        user = self.table_admin_data.item(self.table_admin_data.selection())["values"][0]
        password = self.table_admin_data.item(self.table_admin_data.selection())["values"][1]
        old_data = (user, id_admin)
        
        query = "DELETE FROM administrador WHERE usuario = ? AND id_sesion_admin = ?"
        rowcount = self.run_query(query, old_data, 2)
        if isinstance(rowcount, int): messagebox.showinfo("Mensaje del sistema", f"Se borraron: {rowcount} registros correctamente")
    
    
    

