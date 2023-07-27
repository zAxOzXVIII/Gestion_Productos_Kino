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
    
    def admin_deleteW_control(self, tablaTreeview):
        try:
            tablaTreeview.item(tablaTreeview.selection())["text"]
            tablaTreeview.item(tablaTreeview.selection())["values"][0]
        except IndexError as e:
            self.messageShow(e, 2)
            return
        
        id_admin = tablaTreeview.item(tablaTreeview.selection())["text"]
        user = tablaTreeview.item(tablaTreeview.selection())["values"][0]
        password = tablaTreeview.item(tablaTreeview.selection())["values"][1]
        old_data = (user, id_admin)
        val = self.controlador.toplevel_admin_deleteW(old_data)
        if isinstance(val, int): 
            messagebox.showinfo("Mensaje del sistema", "Se elimino la fila")
            return val
        else: messagebox.showwarning("Advertencia del sistema", val)
    
    def add_sup_from_admin_control(self, name, last_name, dni):
        if name == "" and last_name == "" and dni == "":
            messagebox.showwarning("Advertencia del sistema", "Rellene los campos")
            return
        else:
            self.controlador.admin_query_customThree(1, (),(name, last_name, dni))
    
    def update_sup_from_admin_control(self, data_old, name, lastna, dni, toplevel):
        val = self.controlador.admin_query_customThree(2, data_old, (name, lastna, dni))
        if isinstance(val,int):
            messagebox.showinfo("Mensaje del sistema", "Se actualizo la data correctamente")
            toplevel.destroy()
        else:
            messagebox.showwarning("Advertencia del sistema", "No se actualizo la data")
    
    def delete_zone_work_admin_control(self, toplevel):
        try:
            nm_area_old = toplevel.item(toplevel.selection())["values"][0]
            cdg_zona_old = toplevel.item(toplevel.selection())["values"][1]
            id_sup_old = toplevel.item(toplevel.selection())["values"][2]
            old_data = (nm_area_old, cdg_zona_old, str(id_sup_old))
        except Exception as e:
            messagebox.showwarning("Advertencia del sistema",f"{e} debe seleccionar una fila")
            return None
        
        val = self.controlador.delete_zone_tpl(old_data)
        if isinstance(val, int):
            messagebox.showinfo("Mensaje del sistema", "Se elimino la data correctamente")
            return
        else:
            messagebox.showwarning("Advertencia del sistema", "No se puede eliminar una zona que tiene trabajadores")
    
    def query_add_worker_control(self, params = ()):
        if params[0].get() == "" and params[1].get() == "" and params[2].get() == "":
            messagebox.showwarning("Advertencia del sistema", "Debe llenar los campos correspondientes")
        else:
            self.controlador.query_add_worker(params)
            messagebox.showinfo("Mensaje del sistema", "Se agrego la data correctamente")
    
    def update_workers_sup_control(self, params = (), old_params = ()):
        if params[0].get() == "" and params[1].get() == "" and params[2].get() == "" and params[4].get() != "Seleccionar...":
            messagebox.showwarning("Advertencia del sistema", "Debe llenar los campos correspondientes")
        else:
            val=self.controlador.query_update_worker(params, old_params)
            if isinstance(val,int):
                messagebox.showinfo("Mensaje del sistema", "Se actualizo la data correctamente")
            else:
                messagebox.showwarning("Advertencia del sistema", f"Error {val}")
    
    def query_add_bienes_control(self, prms = ()):
        if prms[0].get()=="" and prms[1].get()=="" and prms[5].get()=="Seleccionar...":
            messagebox.showwarning("Advertencia del sistema", "Debe llenar los campos correspondientes")
            return
        else:
            val = self.controlador.query_add_bienes(prms)
            if isinstance(val, int):
                messagebox.showinfo("Mensaje del sistema", "Se agrego el bien correctamente")
                return True
            else:
                messagebox.showwarning("Advertencia del sistema", f"Error {val}")
    
    def act_data_sup_query_control(self, cnt, nm_c, desc_item, val, obs, id_b, num_c):
        if cnt == "" and nm_c == "" and desc_item == "" and val == "":
            messagebox.showwarning("Advertencia del sistema", "Debe llenar los campos correspondientes")
            return
        else:
            if messagebox.askyesno("Pregunta del sistema", "Desea actualizar el bien-mueble"):
                val = self.controlador.act_data_sup_query(cnt, nm_c, desc_item, val, obs, id_b, num_c)
                if isinstance(val,int): messagebox.showinfo("Mensaje del sistema", "Se actualizo correctamente")
                else:
                    messagebox.showwarning("Advertencia del sistema", f"Error {val}")
                    return val
            else:
                messagebox.showinfo("Mensaje del sistema", "Se revirtio accion")
    
    def query_tomar_data_bienes_controlador(self, id_area = ()):
        val = self.controlador.query_tomar_data_bienes(id_area)
        if val == []: return None
        else: return val
