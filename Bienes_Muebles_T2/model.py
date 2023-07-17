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
# tkinter END
from tkinter import END
# importando libreria vista
# from view import View

class Model():
    db_name = "bienes_muebles"
    # Funciones
    
    def limpiar_ventana(self, opc = 1):
        # limpiando los widgets
        if opc == 1:
            for widget in self.window.winfo_children():
                widget.destroy()
        elif opc == 2:
            for widget in self.toplevel_admin_window.winfo_children():
                widget.destroy()
        elif opc == 3:
            for widget in self.zona_toplevel.winfo_children():
                widget.destroy()
        elif opc == 4:
            for widget in self.worker_toplevel_sup.winfo_children():
                widget.destroy()
        else: print("No existe esta opcion")
    
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
    
    def validacion_limite_str(self, text, limite):
        if len(text) < int(limite):
            return True
        else:
            return False
    
    def validacion_limite_int(self, text, limit):
        if text.isdigit() and len(text) <= int(limit):
            return True
        elif text == "":
            return True
        else:
            return False
    
    def validar_valor_flotante(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    def validar_valor_entero(self, valor):
        try:
            int(valor)
            return True
        except ValueError:
            return False
    
    def obtener_directorio(self):
        directorio = os.getcwd()
        print("Directorio: ",directorio)
        return directorio
    
    def log_public_sesion(self, parameters = ()):
        query = "SELECT * FROM personal_laborando WHERE cedula = %s"
        fetch = self.run_query(query, parameters)
        print(fetch)
        if isinstance(fetch, list):
            return fetch
        else: return fetch
    
    def sector_trabajo_query(self, code):
        # asignando la query sql
        sql = "SELECT * FROM bienes_por_zona WHERE codigo_qr = ?"
        
        try:
            fetch = self.run_query(sql, (code, ))
            if len(fetch) <= 0:
                self.messageShow("Codigo no encontrado favor verifique", 2)
                return
            print(fetch, "l79")
            # imprimiendo valores
            for row in fetch:
                self.messageShow(f"""Datos de la Query: id_bienes = {row[0]}\n id_area = {row[1]} cantidad = {row[2]}\n
                                    numero de consulta = {row[3]} descripcion del item = {row[4]}\n
                                    valor = {row[5]} observacion {row[6]} y codigo qr = {row[7]}""")
            
        except IndexError as E:
            msg = f"Se ha detectado un error: {E}"
            print(fetch)
            return self.messageShow(msg, 3)
    
    def safe_bm_data(self, id, cnt, nc, di, vlr, obs):
        sql = """INSERT INTO bienes_por_zona(id_area, cantidad, num_cons, desc_item, valor, observacion)
                VALUES(?, ?, ?, ?, ? ,?)"""
        # validar flotante o entero de valor
        if self.validar_valor_flotante(vlr) or self.validar_valor_entero(vlr):
            parameters = (id, cnt, nc, di, vlr, obs)
            fila =  self.run_query(sql, parameters, 2)
        else:
            self.messageShow("Error numerico en la entrada valor Bs", 2)
            return
        
        # limpiando formulario
        if isinstance(fila, int):self.messageShow(f"Se subio correctamente los datos, {fila}")
        else:
            self.messageShow("Error al subir la data", 2)
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
            self.messageShow("No coincide su contraseña con los registros", 2)
        else:
            # asignando id supervisor
            id_sup = fetch[0][0]
            self.messageShow("Bienvenido, su sesion a sido verificada con exito")
            self.sesion_level.destroy()
            self.main_sup_panel(id_sup)
    
    def rellenar_tabla_sup(self, id_area = []):
        # limpiar data
        valores = self.tablero_sup.get_children()
        for elemento in valores:
            self.tablero_sup.delete(elemento)
        # llenando data
        if len(id_area) <= 0:
            self.tablero_sup.insert("", "end", text = "No hay bienes por mostrar", values = ("X", "X", "X", "X", "X"))
            return
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
        parameters = (cnt.get(), nm_c.get(), desc_item.get(), val.get(), obs.get(), id_b, )
        if self.validar_valor_flotante(val.get()) or self.validar_valor_entero(val.get()):
            # Pregunta de verificacion
            if self.messageAsk("Esta seguro que desea modificar los valores?\nNo hay control vuelta atras para esta acción"):
                fila = self.run_query(query, parameters, 2)
                if isinstance(fila, int):
                    self.messageShow(f"Todo salio correcto\n se actualizaron {fila} filas")
                    for i in range(4):
                        parameters[i].delete(0, "end")
                else: self.messageShow(f"Se ha detectado un error: {fila}", 2)
            else:
                self.messageShow("Correcto se revirtio la accion")
                return
        else: 
            self.messageShow("Verificar que el valor del precio sea numerico", 2)
            return
    
    def create_qr_code(self):
        # Seleccionando valores
        try:
            self.tablero_sup.item(self.tablero_sup.selection())["text"]
        except IndexError as E:
            self.messageShow("No se a seleccionado ningun registro", 2)
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
            img.save(self.obtener_directorio() + "\\Bienes_Muebles_T2\\config\\images_Qr\\" + name_img + ".png")
        except Exception as e:
            print(e)
            return
    
    def up_qrcode_table(self, parameters = ()):
        query="UPDATE bienes_por_zona SET codigo_qr = ? WHERE id_bienes = ? AND cantidad = ?"
        filas = self.run_query(query, parameters, opc = 2)
        if isinstance(filas, int): self.messageShow(f"Se actualizaron {filas}")
        else: print(filas)
    
    def log_adm_sesion(self, user, password):
        if user=="" and password=="":
            self.messageShow("Rellenar los campos")
            return
        query = "SELECT * FROM administrador WHERE usuario = ? AND clave = ?"
        parameters = (user, password, )
        fetch = self.run_query(query, parameters)
        if isinstance(fetch, str) == True or fetch==[]:
            self.messageShow(f"Contraseña incorrecta o usuario incorrecto", 2)
            return
        else:
            # asignando valores
            for u in fetch:
                if user == u[1]: name_u = u[1]
            self.messageShow("Bienvenido, se verifico con exito")
            self.toplevel_admin.destroy()
            self.limpiar_ventana()
            # generando ventana admin
            self.w_admin_main(name_u)
    
    def fill_admin_table_sup(self, busqueda = (), w_quest = "1"):
        # limpiamos tabla
        records = self.admin_table_sup.get_children()
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
                query = f"SELECT * FROM supervisor_area_kino WHERE {valor}"
                fetch = self.run_query(query)
                for row in fetch:
                    self.admin_table_sup.insert("", "end", text=row[0], values = (row[1], row[2], row[3]))
    
    def fill_workers_table(self, id_busqueda = []):
        # limpiamos tabla
        records = self.table_workers_sup.get_children()
        for element in records:
            self.table_workers_sup.delete(element)
        # rellenamos tabla
        for row in id_busqueda:
            query = "SELECT * FROM personal_laborando WHERE id_area = %s"
            fetch = self.run_query(query, (row, ))
            if isinstance(fetch, list) and len(fetch) > 0:
                for prs in fetch:
                    self.table_workers_sup.insert("", "end", text = prs[0], values = (prs[1], prs[2], prs[3], prs[4], prs[5]))
            else: self.table_workers_sup.insert("", "end", text = "No hay personal en esta area", values = ("X", "X", "X", "X", "X"))
    
    def get_ci_sups(self):
        query = "SELECT cedula FROM supervisor_area_kino"
        fetch = self.run_query(query)
        return fetch
    
    def selec_zone_admin_table(self):
        try:
            nm_area_old = self.zone_treeView.item(self.zone_treeView.selection())["values"][0]
            cdg_zona_old = self.zone_treeView.item(self.zone_treeView.selection())["values"][1]
            id_sup_old = self.zone_treeView.item(self.zone_treeView.selection())["values"][2]
            return (nm_area_old, cdg_zona_old, str(id_sup_old))
        except Exception as e:
            self.messageShow(f"{e} debe seleccionar una fila", 2)
            return 0
    
    def delete_workers_sup(self, id_areasT : list):
        # pedir la data
        old_values = self.selec_workers_table()
        query = "DELETE FROM personal_laborando WHERE nombre = %s AND cedula = %s"
        if self.messageAsk(f"Esta seguro que desea eliminar para siempre al empleado {old_values[0]}"):
            rowcount = self.run_query(query, (old_values[0], old_values[2], ), 2)
            if isinstance(rowcount, int):
                self.messageShow(f"Se elimino al empleado = {old_values}")
                self.fill_workers_table(id_areasT)
        else: 
            self.messageShow("Se revirtieron las acciones")
            return
    
    def query_add_worker(self, parameters = ()):
        params_get = (parameters[0].get(), parameters[1].get(), parameters[2].get(), parameters[3].get(), parameters[4].get())
        query = """INSERT INTO personal_laborando(nombre, apellido, cedula, fecha_nacimiento, id_area)
                    VALUES (%s, %s, %s, %s, %s)"""
        rowcount = self.run_query(query, params_get, 2)
        if isinstance(rowcount, int):
            self.messageShow(f"Se inserto {rowcount} empleado")
            # limpiando entrys
            for entry in parameters:
                entry.delete(0, "end")
        else: 
            self.messageShow(f"Ocurrio un error al insertar, por favor llene todas las casillas", 2)
            print(rowcount)
    
    def query_update_worker(self, parameters = (), old_params = ()):
        params_get = (parameters[0].get(), parameters[1].get(), parameters[2].get(), parameters[3].get(), parameters[4].get())
        query = """UPDATE personal_laborando
                    SET nombre = %s, apellido = %s, cedula = %s, fecha_nacimiento = %s, id_area = %s
                    WHERE nombre = %s AND cedula = %s"""
        tlt_params = params_get + (old_params[0], old_params[2], )
        rowcount = self.run_query(query, tlt_params)
        if rowcount > 0 and isinstance(rowcount, int):
            self.messageShow(f"Se actualizo {rowcount} empleado")
            # limpiando entrys
            for entry in parameters:
                entry.delete(0, "end")
        else: 
            self.messageShow(f"Ocurrio un error al actualizar, por favor llene todas las casillas", 2)
            print(rowcount)
    
    def selec_workers_table(self):
        try:
            nm_worker_old = self.table_workers_sup.item(self.table_workers_sup.selection())["values"][0]
            lnm_worker_old = self.table_workers_sup.item(self.table_workers_sup.selection())["values"][1]
            ci_worker_old = self.table_workers_sup.item(self.table_workers_sup.selection())["values"][2]
            date_worker_old = self.table_workers_sup.item(self.table_workers_sup.selection())["values"][3]
            id_a_worker_old = self.table_workers_sup.item(self.table_workers_sup.selection())["values"][4]
            old_values = (nm_worker_old, lnm_worker_old, ci_worker_old, date_worker_old, id_a_worker_old)
            return old_values
        except Exception as e:
            self.messageShow(f"{e} | debe seleccionar una fila de trabajadores", 2)
            return 0
    
    def selec_bienes_table(self):
        try:
            cnt_old = self.tablero_sup.item(self.tablero_sup.selection())["values"][0]
            nmC_old = self.tablero_sup.item(self.tablero_sup.selection())["values"][1]
            descI_old = self.tablero_sup.item(self.tablero_sup.selection())["values"][2]
            val_old = self.tablero_sup.item(self.tablero_sup.selection())["values"][3]
            obs_old = self.tablero_sup.item(self.tablero_sup.selection())["values"][4]
            return (cnt_old, nmC_old, descI_old, val_old, obs_old, )
        except Exception as e:
            self.messageShow(f"{e} | debe seleccionar una fila de trabajadores", 2)
            return 0
    
    def query_add_bienes(self, params = ()):
        params_get = (params[0].get(), params[1].get(), params[2].get(), params[3].get(), params[4].get(), params[5].get())
        if self.validar_valor_flotante(params_get[3]) or self.validar_valor_entero(params_get[3]):
            query = """INSERT INTO bienes_por_zona(cantidad, num_cons, desc_item, valor, observacion, id_area)
                        VALUES(%s, %s, %s, %s, %s, %s)"""
            rowcount = self.run_query(query, params_get, 2)
            print(rowcount)
            if isinstance(rowcount, int):
                self.messageShow(f"Se agrego {rowcount} filas")
                for entry in params:
                    entry.delete(0, "end")
            else:
                self.messageShow(f"error: {rowcount}", 2)
        else:
            self.messageShow("Verificar la entrada de valor Bs que sea numerico", 2)
            return
    
    def get_zonas_sup_bienes(self, params=()):
        query = "SELECT nombre_area, id_area FROM areas_trabajo_kino WHERE id_supervisor = %s"
        fetch = self.run_query(query, params)
        return fetch
    
    def delete_bn_query(self, id_data_r : list):
        # data
        old_values = self.selec_bienes_table()
        if old_values == 0: return
        query="DELETE FROM bienes_por_zona WHERE desc_item = %s AND num_cons = %s"
        if self.messageAsk(f"Esta seguro de eliminar el bien {old_values}"):
            rowcount = self.run_query(query, (old_values[2], old_values[1], ), 2)
            if isinstance(rowcount, int):
                self.messageShow(f"Se elimino el bien {old_values}")
                self.rellenar_tabla_sup(id_data_r)
        else: self.messageshow("Se revirtieron las acciones")
    
    def delete_zone_tpl(self):
        old_values = self.selec_zone_admin_table()
        if old_values == 0: return
        # datos
        query = "DELETE FROM areas_trabajo_kino WHERE nombre_area = %s AND codigo_zona = %s AND id_supervisor = %s"
        rowcount = self.run_query(query, old_values, 2)
        self.back_zone_toplevel()
        return rowcount
    
    def query_busqueda_sup_zone(self, ci_old : str):
        query = "SELECT cedula FROM supervisor_area_kino WHERE id_supervisor = %s"
        fetch = self.run_query(query, (ci_old, ))
        return fetch
    
    def get_id_sup_byCi(self, ci : str):
        query = "SELECT id_supervisor FROM supervisor_area_kino WHERE cedula = %s"
        fetch = self.run_query(query, (ci, ))
        if isinstance(fetch, list): return fetch[0][0]
        else: self.messageShow(f"Error {fetch}", 2)
    
    def query_update_zone(self, parameters = ()):
        id_sup = self.get_id_sup_byCi(parameters[2])
        values = (parameters[0], parameters[1], id_sup, parameters[3], parameters[4], )
        print(values)
        query = "UPDATE areas_trabajo_kino SET nombre_area= %s, codigo_zona = %s, id_supervisor= %s WHERE nombre_area= %s AND codigo_zona = %s"
        rowcount = self.run_query(query, values, 2)
        if isinstance(rowcount, int): 
            self.messageShow(f"Todo salio correctamente se actualizaron {rowcount} filas")
            self.back_zone_toplevel()
        else: self.messageShow(f"{rowcount} error...")
    
    def query_add_zone(self, parameters = ()):
        id_sup = self.get_id_sup_byCi(parameters[2])
        values = (parameters[0], parameters[1], str(id_sup), )
        print(values)
        query = "INSERT INTO areas_trabajo_kino(nombre_area, codigo_zona, id_supervisor) VALUES (%s, %s, %s)"
        rowcount = self.run_query(query, values, 2)
        if isinstance(rowcount, int): 
            self.messageShow(f"Todo salio correctamente se agregaron {rowcount} filas")
            self.back_zone_toplevel()
        else: self.messageShow(f"{rowcount} error...")
    
    def sesion_sup_query(self, parameters = ()):
        query = "SELECT * FROM supervisor_area_kino WHERE cedula = %s AND nombre = %s"
        fetch = self.run_query(query, parameters)
        if isinstance(fetch, list) and len(fetch) > 0: 
            self.main_sup_panel(str(fetch[0][0]), fetch[0][1])
            
        else:
            self.messageShow(f"No coincide la sesion, please try again")
            return
    
    def select_admin_table_sup(self):
        try:
            self.admin_table_sup.item(self.admin_table_sup.selection())["text"]
        except IndexError as e:
            self.messageShow(e, 2)
            return
        
        name = self.admin_table_sup.item(self.admin_table_sup.selection())["values"][0]
        last_name = self.admin_table_sup.item(self.admin_table_sup.selection())["values"][1]
        dni = self.admin_table_sup.item(self.admin_table_sup.selection())["values"][2]
        return (name, last_name, str(dni))
    
    def table_selection_question_sup(self):
        if isinstance(self.admin_table_sup.item(self.admin_table_sup.selection())["text"], int): return True
        else: return False
    
    def admin_query_customThree(self, opc : int, old_info = (), new_info = ()):
        # tupla grande 
        update_info = new_info + old_info
        # imprimiendo valores
        print("Valores old_info L533", old_info)
        print("Valores new_info L534", new_info)
        if opc == 1:
            query = "INSERT INTO supervisor_area_kino(nombre, apellido, cedula) VALUES(?, ?, ?)"
            fila = self.run_query(query, new_info, 2)
            if isinstance(fila, int) == True:
                print("la insercion salio bien L-268")
                self.three_message_interface(self.add_window, "La insercion salio bien")
            else: print(fila)
        elif opc == 2:
            query = f"UPDATE supervisor_area_kino SET nombre = ?, apellido = ?, cedula = ? WHERE nombre = ? AND apellido = ? AND cedula = ?"
            fila = self.run_query(query, update_info, 2)
            if isinstance(fila, int) == True: 
                print("el update salio bien L-273", fila)
                self.three_message_interface(self.update_window, "La actualizacion salio bien")
            else: print(fila)
        elif opc == 3:
            query = f"DELETE FROM supervisor_area_kino WHERE nombre = ? AND apellido = ? AND cedula = ?"
            fila = self.run_query(query, old_info, 2)
            if isinstance(fila, int) == True:
                print(fila, "El delete salio bien L-279")
            else: print(fila)
    
    def fill_zona_treeview(self):
        query = "SELECT * FROM areas_trabajo_kino"
        fetch = self.run_query(query)
        return fetch
    
    def topLevel_admin_interface_delete(self):
        # testeando seleccion
        if self.table_selection_question_sup(): pass
        else: 
            self.messageShow("Se debe seleccionar un registro de la tabla supervisor", 2)
            return
        # Llamando query para eliminar data
        select_data = self.select_admin_table_sup()
        if len(select_data) > 0: 
            if self.messageAsk(f"Esta seguro de eliminar el registro {select_data}"):
                self.admin_query_customThree(3, old_info = select_data)
        else:
            self.messageShow("Error, debe seleccionar una fila", 2)
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
        else: self.messageShow(fetch, 2)
    
    def add_admin_registers(self, parameters = ()):
        query = "INSERT INTO administrador(usuario, clave) VALUES(?, ?)"
        rowcount = self.run_query(query, parameters, 2)
        print("Numero de filas apectadas {rowcount}".format(rowcount))
    # query para borrar administrador ->modelo
    
    def toplevel_admin_deleteW(self):
        try:
            self.table_admin_data.item(self.table_admin_data.selection())["text"]
            self.table_admin_data.item(self.table_admin_data.selection())["values"][0]
        except IndexError as e:
            self.messageShow(e, 2)
            return
        
        id_admin = self.table_admin_data.item(self.table_admin_data.selection())["text"]
        user = self.table_admin_data.item(self.table_admin_data.selection())["values"][0]
        password = self.table_admin_data.item(self.table_admin_data.selection())["values"][1]
        old_data = (user, id_admin)
        
        query = "DELETE FROM administrador WHERE usuario = ? AND id_sesion_admin = ?"
        rowcount = self.run_query(query, old_data, 2)
        if isinstance(rowcount, int): self.messageShow(f"Se borraron: {rowcount} registros correctamente")

