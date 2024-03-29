# Librerias
# importando libreria Pillow - convert image
import PIL as pil
from PIL import ImageTk
# Excel
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side 
# importando libreria grafica Tkainter
from tkinter import ttk, Label, Entry, Toplevel, CENTER
from tkinter import messagebox
from tkcalendar import DateEntry
# importando modelo
from modelo.model import Model
from controlador.controller import Controlador
# os
import os
# fin de librerias
# Declarando clase vista
class View(Model):
    
    def __init__(self, window):
        self.window = window
        # print(type(self.window))
        # self.window.geometry("640x480")
        self.window.title("Bienes Muebles Kino Tachira")
        self.window.resizable(width=False, height=False)
        self.controlador = Controlador()
        # Label Titulo Main
        label_panel = Label(self.window, text="Panel de Usuarios", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=(20,0))
        Label(self.window, text="Sesion Administrador").grid(row=1, column=0, pady=(25,6))
        boton_admin = ttk.Button(self.window, text="Iniciar Sesion", command = self.toplevel_login_admin).grid(row=1, column=1, pady=(25,6), padx=(0, 15))
        
        Label(self.window, text="Sesion supervisor").grid(row=2, column=0, pady=(6,6))
        boton_sup = ttk.Button(self.window, text="Iniciar Sesion", command = self.toplevel_login_sup).grid(row=2, column=1, pady=(6,6), padx=(0, 15))
        
        Label(self.window, text="Publico").grid(row=3, column=0, pady=(6,15))
        boton_public = ttk.Button(self.window, text="Ingresar", command=self.sesion_public_main).grid(row=3, column=1, pady=(6,15), padx=(0, 15))
        # Pie de ventana
        self.pie_pagina(0, 1)
        
    
    def pie_pagina(self, p1 : int, p2 : int):
        direct = self.obtener_directorio()
        imagen = pil.Image.open(f"{direct}\\config\\images_ui\\kino_logo.png")
        image_re = imagen.resize((64,64), pil.Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(image_re)
        # obtener numero de filas
        num_filas = self.window.grid_size()[1]
        num_columnas = self.window.grid_size()[0]
        # print(self.window.grid_size()) -> imprime la tupla de size
        # label image
        
        lbl_img = Label(self.window, image=img_tk)
        lbl_img.grid(row=num_filas, column=p2)
        lbl_img.imagen = img_tk
        
        # Label texto
        texto = "Requerimientos para Graduarse de TSU\nMarden Barrera V-30262472\nElio Gutiérrez V-31509689\nDaniela Simanca V-26987707"
        copy = Label(self.window, text=texto).grid(row=num_filas, column=p1)
    
    def messageShow(self, msg : str, opc = 1):
        if opc==1:
            return messagebox.showinfo(title = "Mensaje del sistema", message = msg)
        elif opc==2:
            return messagebox.showwarning(title = "Advertencia del sistema", message = msg)
        elif opc==3:
            return messagebox.showerror(title = "Error del sistema", message = msg)
    
    def messageAsk(self, msg = "", opc = 1):
        if opc == 1:
            return messagebox.askyesno("Pregunta del sistema", msg)
    
    def sesion_public_main(self):
        # top level
        self.toplevel_public_sesion = Toplevel(self.window)
        self.toplevel_public_sesion.title("Sesion de trabajadores")
        self.toplevel_public_sesion.resizable(width=None, height=None)
        self.toplevel_public_sesion.grab_set()
        Label(self.toplevel_public_sesion, text="Ingrese su numero de cedula").grid(row=0, column=0, padx=50, pady=(25, 10), columnspan=2)
        # validaciones
        validacion_limiteInt = self.toplevel_public_sesion.register(self.validacion_limite_int)
        cedula = ttk.Entry(self.toplevel_public_sesion, validate="key", validatecommand=(validacion_limiteInt, "%P", 9))
        cedula.grid(row=1, column=0, padx=50, pady=(0, 25), columnspan=2)
        ttk.Button(self.toplevel_public_sesion, text="Ingresar", command = lambda : self.public_main(cedula.get(), )).grid(row=2, column=0, padx=(50, 5))
        ttk.Button(self.toplevel_public_sesion, text="Regresar", command = lambda : self.toplevel_public_sesion.destroy()).grid(row=2, column=1, padx=(5, 50))
    
    
    
    def public_main(self, ci : str):
        datos = self.log_public_sesion(parameters = (ci, ))
        if isinstance(datos, list) and len(datos) > 0:
            self.messageShow(f"Bienvenido {datos[0][1]}")
        elif datos == []:
            self.messageShow(f"No se encontraron registros", 2)
            return
        else:  self.messageShow(datos, 2)
        # limpiar ventana principal
        self.limpiar_ventana()
        # generar nuevos labels
        # configurando validacion
        validacion_limiteStr = self.window.register(self.validacion_limite_str)
        title = Label(self.window, text="Digite el codigo del QR\nCon el cual se hará la busqueda").grid(row=0, column=0)
        code = Entry(self.window, width=24, validate="key", validatecommand=(validacion_limiteStr, "%P", 25))
        code.focus()
        code.grid(row=0, column=1)
        boton_load = ttk.Button(self.window, text="Buscar", command= lambda : self.sector_trabajo_query(code.get()))
        boton_load.grid(row=1, column=0)
        
        # volver al inicio
        num_filas = self.window.grid_size()[1]
        salir = ttk.Button(self.window, text="Ir al Inicio", command=self.label_main).grid(row=num_filas, column=0, columnspan=2, pady=15)
        
        # pie de ventana
        self.pie_pagina(0, 1)
    
    def label_main(self):
        # limpiando ventana
        self.limpiar_ventana()
        # ajustando tamaño
        # self.window.geometry("640x480")
        
        label_panel = Label(self.window, text="Panel de Usuarios").grid(row=0, column=0, columnspan=2)
        Label(self.window, text="Sesion Administrador").grid(row=1, column=0)
        boton_admin = ttk.Button(self.window, text="Iniciar Sesion", command = self.toplevel_login_admin).grid(row=1, column=1)
        
        Label(self.window, text="Sesion supervisor").grid(row=2, column=0)
        boton_sup = ttk.Button(self.window, text="Iniciar Sesion", command=self.toplevel_login_sup).grid(row=2, column=1)
        
        Label(self.window, text="Publico").grid(row=3, column=0)
        boton_public = ttk.Button(self.window, text="Ingresar", command=self.sesion_public_main).grid(row=3, column=1)
        # pie de ventana
        self.pie_pagina(0, 1)
    
    def toplevel_login_admin(self):
        self.toplevel_admin = Toplevel()
        self.toplevel_admin.title("Sesion de Administrador")
        self.toplevel_admin.resizable(width=False, height=False)
        # configurando validaciones
        validacion_limiteStr = self.toplevel_admin.register(self.validacion_limite_str)
        self.toplevel_admin.grab_set()
        #  planteando sesion de administrador
        Label(self.toplevel_admin, text="Inicia como administrador").grid(row=0, column=0, columnspan=2, padx=(50, 50), pady=(15, 10))
        Label(self.toplevel_admin, text="Ingresa\nUsuario").grid(row=1, column=0, padx=(50, 0), pady=(0, 10))
        user_adm = Entry(self.toplevel_admin, validate="key", validatecommand=(validacion_limiteStr, "%P", 32))
        user_adm.grid(row=1, column=1, padx=(0, 50), pady=(0, 10))
        user_adm.focus()
        # password
        Label(self.toplevel_admin, text="Ingrese\nContraseña").grid(row=2, column=0, padx=(50, 0), pady=(0, 10))
        password_adm = Entry(self.toplevel_admin, validate="key", validatecommand=(validacion_limiteStr, "%P", 16), show="*")
        password_adm.grid(row=2, column=1, padx=(0, 50), pady=(0, 10))
        # button
        ttk.Button(self.toplevel_admin, text="Ingresar", command = lambda : self.log_adm_sesion(user_adm.get(), password_adm.get())).grid(row=3, column=0, columnspan=2, pady=10, padx=50)
    
    def window_after_query_work(self, zona, id):
        # Titulo
        Label(self.window, text=f"Registro de Bienes de {zona}").grid(row=0, column=0, columnspan=2)
        # configurando validaciones
        validacion_limiteStr = self.window.register(self.validacion_limite_str)
        validacion_limiteInt = self.window.register(self.validacion_limite_int)
        # añadiendo formulario
        Label(self.window, text="Digite cantidad de elementos").grid(row=1, column=1)
        self.cantidad = Entry(self.window, validate="key", validatecommand=(validacion_limiteInt, "%P", 4))
        self.cantidad.grid(row=1, column=0)
        
        Label(self.window, text="Digite cantidad de numero de consulta").grid(row=2, column=1)
        self.num_cons = Entry(self.window, validate="key", validatecommand=(validacion_limiteInt, "%P", 6))
        self.num_cons.grid(row=2, column=0)
        
        Label(self.window, text="Digite descripcion del item").grid(row=3, column=1)
        self.desc_item = Entry(self.window, validate="key", validatecommand=(validacion_limiteStr, "%P", 64))
        self.desc_item.grid(row=3, column=0)
        
        Label(self.window, text="Digite valor en Bs").grid(row=4, column=1)
        self.valor = Entry(self.window, validate="key", validatecommand=(validacion_limiteStr, "%P", 8))
        self.valor.grid(row=4, column=0)
        
        Label(self.window, text="Digite observacion").grid(row=5, column=1)
        self.observ = Entry(self.window, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        self.observ.grid(row=5, column=0)
        
        # Boton guardar data
        guardar = ttk.Button(self.window, text="Subir registro", command= lambda : self.safe_bm_data(id, self.cantidad.get(), self.num_cons.get(),
                                                                                                        self.desc_item.get(), self.valor.get(),
                                                                                                        self.observ.get())).grid(row=6, column=0, columnspan=2)
        # Salir
        num_filas = self.window.grid_size()[1]
        salir = ttk.Button(self.window, text="Ir al Inicio", command=self.label_main).grid(row=num_filas, column=0, columnspan=2, pady=15)
        # pie pagina
        self.pie_pagina(0, 1)
    
    def toplevel_login_sup(self):
        self.sesion_level = Toplevel(self.window)
        self.sesion_level.title("Inicio de sesion del supervisor de area")
        self.sesion_level.resizable(width=False, height=False)
        # focus
        self.sesion_level.grab_set()
        # configurando validaciones
        validacion_limiteStr = self.sesion_level.register(self.validacion_limite_str)
        validacion_limiteInt = self.sesion_level.register(self.validacion_limite_int)
        Label(self.sesion_level, text="Sesion de Supervisores").grid(row=0, column=0, columnspan=2, padx=50, pady=(5, 15))
        Label(self.sesion_level, text="Para verificar si tiene permisos\ncomo supervisor digite su numero de cedula").grid(row=1, column=0, padx=(50, 0), pady=(0, 10))
        ci_sesion = Entry(self.sesion_level, validate="key", validatecommand=(validacion_limiteInt, "%P", 9))
        ci_sesion.grid(row=1, column=1, padx=(0, 50), pady=(0, 10))
        # nombre
        Label(self.sesion_level, text="Digite el nombre del supervisor").grid(row=2, column=0, padx=(50,0), pady=(5, 15))
        nm_sesion = ttk.Entry(self.sesion_level, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        nm_sesion.grid(row=2, column=1, padx=(0,50), pady=(5, 15))
        ttk.Button(self.sesion_level, text="Ingresar", command= lambda: self.sesion_sup_query(parameters = (ci_sesion.get(), nm_sesion.get(), ))).grid(row=3, column=0, columnspan=2)
    
    def main_sup_panel(self, id_sup : str, name : str):
        # Limpiamos pantalla
        self.limpiar_ventana()
        # Recopilando data del id sesion
        # self.window.geometry("900x450")
        # 
        Label(self.window, text=f"Supervisor encargado {name}").grid(row=0, column=0, columnspan=3, pady=10, padx=25)
        self.tablero_sup = ttk.Treeview(self.window, height=10)
        # asignando en main window
        self.tablero_sup.grid(row=1, column=0, columnspan=3, rowspan=3)
        # entablando heading
        self.tablero_sup["columns"] = ("col0", "col1", "col2", "col3", "col4")
        # asignando valores a las columnas
        self.tablero_sup.heading(column = "#0", text="ID")
        self.tablero_sup.heading(column = "col0", text="Cantidad")
        self.tablero_sup.heading(column = "col1", text="Numero de consultas")
        self.tablero_sup.heading(column = "col2", text="Descripcion del item")
        self.tablero_sup.heading(column = "col3", text="Valor")
        self.tablero_sup.heading(column = "col4", text="Observacion")
        # Ajustar columnas al contenido
        for columna in self.tablero_sup["columns"]:
            self.tablero_sup.column(columna, width=100, minwidth=50, anchor=CENTER)
        # Rellenar de datos las filas
        query = "SELECT * FROM areas_trabajo_kino WHERE id_supervisor = ?"
        parameters = (id_sup, )
        fetch = self.run_query(query, parameters)
        # asignando valores
        id_area = []
        nombre_area = []
        codigo_zona = []
        for row in fetch:
            id_area.append(row[0])
            nombre_area.append(row[1])
            codigo_zona.append(row[2])
        # funcion
        self.rellenar_tabla_sup(id_area)
        # Botones
        ttk.Button(self.window, text="Actualizar Datos", command = lambda : self.up_data_sup(id_area)).grid(row=4, column=0)
        ttk.Button(self.window, text="Generar Codigo Qr", command = self.create_qr_code).grid(row=4, column=1)
        ttk.Button(self.window, text="Salir", command = self.label_main).grid(row=4, column=2)
        # bienes
        ttk.Button(self.window, text="Empleados configuracion", command = lambda : self.main_worker_tpl(name, id_area)).grid(row=1, column=3)
        ttk.Button(self.window, text="Agregar Bienes", command = lambda : self.add_bn_tpl(id_sup, id_area)).grid(row=2, column=3)
        ttk.Button(self.window, text="Eliminar Bienes", command = lambda : self.delete_bn_query(id_area)).grid(row=3, column=3)
        # Generar Excel button
        ttk.Button(self.window, text="Generar registro de bienes", command = lambda : self.generar_excel()).grid(row=4, column=0, columnspan=4)
        # pie de pagina
        self.pie_pagina(0, 3)
    
    def add_bn_tpl(self, sup_id, id_ar):
        # Generando top level
        self.bienes_add_topl = Toplevel()
        self.bienes_add_topl.title("Ventana para agregar bienes")
        self.bienes_add_topl.resizable(width=False, height=False)
        # configurando validaciones
        validacion_limiteStr = self.bienes_add_topl.register(self.validacion_limite_str)
        validacion_limiteInt = self.bienes_add_topl.register(self.validacion_limite_int)
        # focus
        self.bienes_add_topl.grab_set()
        # labels
        Label(self.bienes_add_topl, text="Digite cantidad").grid(row=0, column=0, columnspan=2)
        cnt_bn = ttk.Entry(self.bienes_add_topl, validate="key", validatecommand=(validacion_limiteInt, "%P", 4))
        cnt_bn.grid(row=1, column=0, padx=10)
        
        Label(self.bienes_add_topl, text="Digite numero de consulta").grid(row=2, column=0, columnspan=2)
        nmC_bn = ttk.Entry(self.bienes_add_topl, validate="key", validatecommand=(validacion_limiteInt, "%P", 6))
        nmC_bn.grid(row=3, column=0, padx=10)
        
        Label(self.bienes_add_topl, text="Digite descripcion del item").grid(row=4, column=0, columnspan=2)
        descI_bn = ttk.Entry(self.bienes_add_topl, validate="key", validatecommand=(validacion_limiteStr, "%P", 64))
        descI_bn.grid(row=5, column=0, padx=10)
        
        Label(self.bienes_add_topl, text="Digite valor del bienmueble").grid(row=6, column=0, columnspan=2)
        val_bn = ttk.Entry(self.bienes_add_topl, validate="key", validatecommand=(validacion_limiteInt, "%P", 8))
        val_bn.grid(row=7, column=0, padx=10)
        
        Label(self.bienes_add_topl, text="Digite observacion").grid(row=8, column=0, columnspan=2)
        obs_bn = ttk.Entry(self.bienes_add_topl, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        obs_bn.grid(row=9, column=0, padx=10)
        
        Label(self.bienes_add_topl, text="Digite zona del bien").grid(row=10, column=0, columnspan=2)
        lista_zonas = ["Seleccionar..."]
        bienesL = self.get_zonas_sup_bienes((sup_id, ))
        for val in bienesL:
            lista_zonas.append(val[1])
        zon_bn = ttk.Combobox(self.bienes_add_topl, value=lista_zonas, state="readonly")
        zon_bn.set(lista_zonas[0])
        zon_bn.grid(row=11, column=0, padx=10)
        # botones
        ttk.Button(self.bienes_add_topl, text="Agregar", command = lambda : self.add_biees_vie(id_ar,(cnt_bn, nmC_bn, descI_bn,
                                                                                                            val_bn,
                                                                                                            obs_bn,
                                                                                                            zon_bn
                                                                                                            ))).grid(row=12, column=0)
        ttk.Button(self.bienes_add_topl, text="Volver", command = lambda : self.bienes_add_topl.destroy()).grid(row=12, column=1)
    
    def add_biees_vie(self, id_area, par=()):
        val = self.controlador.query_add_bienes_control(par)
        if val == True: self.rellenar_tabla_sup(id_area)
    
    def main_worker_tpl(self, name_sup : str, id_areas = []):
        # predefiniendo nuevo toplevel
        self.worker_toplevel_sup = Toplevel(self.window)
        self.worker_toplevel_sup.title("Ventana de trabajadores")
        self.worker_toplevel_sup.resizable(width=False, height=False)
        # focus
        self.worker_toplevel_sup.grab_set()
        # self.worker_toplevel_sup.geometry("900x400")
        # tablero que muestra trabajadores actuales
        Label(self.worker_toplevel_sup, text = f"Tablero de empleados actuales a cargo de {name_sup}").grid(row=0, column=0, columnspan=2)
        self.table_workers_sup = ttk.Treeview(self.worker_toplevel_sup, height=10)
        self.table_workers_sup.grid(row=1, column=0, rowspan=3)
        self.table_workers_sup["columns"] = ("col0", "col1", "col2", "col3", "col4")
        # cabeceras
        self.table_workers_sup.heading(column = "col0", text="Nombre")
        self.table_workers_sup.heading(column = "col1", text="Apellido")
        self.table_workers_sup.heading(column = "col2", text="Cedula")
        self.table_workers_sup.heading(column = "col3", text="Fecha nacimiento")
        self.table_workers_sup.heading(column = "col4", text="id_area")
        # Ajustar columnas al contenido
        for columna in self.table_workers_sup["columns"]:
            self.table_workers_sup.column(columna, width=100, minwidth=50, anchor=CENTER)
        # rellenar tabla
        self.fill_workers_table(id_areas)
        # botones
        ttk.Button(self.worker_toplevel_sup, text = "Agregar empleado", command = lambda : self.add_workers_sup(name_sup, id_areas)).grid(row=1, column=1)
        ttk.Button(self.worker_toplevel_sup, text = "Actualizar empleado", command = lambda : self.update_workers_sup(name_sup, id_areas)).grid(row=2, column=1)
        ttk.Button(self.worker_toplevel_sup, text = "Eliminar empleado", command = lambda : self.delete_workers_sup(id_areas)).grid(row=3, column=1)
        # salir
        ttk.Button(self.worker_toplevel_sup, text = "Salir", command = self.close_workers_tpl).grid(row=4, column=0, columnspan=2)
    
    def back_workers_tpl(self, name_supT : str, id_areasT = []):
        # eliminar pantalla
        self.close_workers_tpl()
        # reescribiendo main worker
        self.main_worker_tpl(name_supT, id_areasT)
    
    def add_workers_sup(self, name_supT : str, id_areasT = []):
        if name_supT == "":
            messagebox.showwarning("Advertencia del sistema", "No hay data del supervisor")
            return
        # limpiar ventana toplevel workers
        self.limpiar_ventana(4)
        # configurando validaciones
        validacion_limiteStr = self.worker_toplevel_sup.register(self.validacion_limite_str)
        validacion_limiteInt = self.worker_toplevel_sup.register(self.validacion_limite_int)
        # D
        Label(self.worker_toplevel_sup, text = "Nombre").grid(row=0, column=0)
        nm_w = ttk.Entry(self.worker_toplevel_sup, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        nm_w.grid(row=0, column=1)
        
        Label(self.worker_toplevel_sup, text = "Apellido").grid(row=1, column=0)
        lnm_w = ttk.Entry(self.worker_toplevel_sup, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        lnm_w.grid(row=1, column=1)
        
        Label(self.worker_toplevel_sup, text = "Cedula").grid(row=2, column=0)
        ci_w = ttk.Entry(self.worker_toplevel_sup, validate="key", validatecommand=(validacion_limiteInt, "%P", 9))
        ci_w.grid(row=2, column=1)
        
        Label(self.worker_toplevel_sup, text = "Fecha\nde nacimiento").grid(row=3, column=0)
        date_w = DateEntry(self.worker_toplevel_sup, date_pattern="YYYY-MM-DD")
        date_w.grid(row=3, column=1)
        
        Label(self.worker_toplevel_sup, text = "id_area donde trabajara").grid(row=4, column=0)
        lista = ["Seleccionar..."]
        # agregar listado
        for row in id_areasT:
            lista.append(row)
        # combo box
        combo_id = ttk.Combobox(self.worker_toplevel_sup, values=lista)
        combo_id.set(lista[0])
        combo_id.grid(row=4, column=1)
        # agregar
        ttk.Button(self.worker_toplevel_sup, text="Agregar", command = lambda : self.controlador.query_add_worker_control((nm_w,
                                                                                                                    lnm_w,
                                                                                                                    ci_w,
                                                                                                                    date_w,
                                                                                                                    combo_id))).grid(row=5, column = 0, padx=2, pady=15)
        # regresar
        ttk.Button(self.worker_toplevel_sup, text="Regresar", command = lambda : self.back_workers_tpl(name_supT, id_areasT)).grid(row=5, column=1, padx=2, pady=15)
    
    def update_workers_sup(self, name_supT : str, id_areasT = []):
        # old data
        old_data = self.selec_workers_table()
        if old_data == 0:
            self.back_workers_tpl(name_supT, id_areasT)
            return
        # limpiar ventana toplevel workers
        self.limpiar_ventana(4)
        # configurando validaciones
        validacion_limiteStr = self.worker_toplevel_sup.register(self.validacion_limite_str)
        validacion_limiteInt = self.worker_toplevel_sup.register(self.validacion_limite_int)
        # D
        Label(self.worker_toplevel_sup, text = "Nombre").grid(row=0, column=0)
        nm_w = ttk.Entry(self.worker_toplevel_sup, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        nm_w.grid(row=0, column=1)
        Label(self.worker_toplevel_sup, text = f"Nombre actual = {old_data[0]}", relief="sunken")
        
        Label(self.worker_toplevel_sup, text = "Apellido").grid(row=1, column=0)
        lnm_w = ttk.Entry(self.worker_toplevel_sup, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        lnm_w.grid(row=1, column=1)
        
        Label(self.worker_toplevel_sup, text = "Cedula").grid(row=2, column=0)
        ci_w = ttk.Entry(self.worker_toplevel_sup, validate="key", validatecommand=(validacion_limiteInt, "%P", 9))
        ci_w.grid(row=2, column=1)
        
        Label(self.worker_toplevel_sup, text = "Fecha\nde nacimiento").grid(row=3, column=0)
        date_w = DateEntry(self.worker_toplevel_sup, date_pattern="YYYY-MM-DD")
        date_w.grid(row=3, column=1)
        
        Label(self.worker_toplevel_sup, text = "id_area donde trabajara").grid(row=4, column=0)
        lista = ["Seleccionar..."]
        # agregar listado
        for row in id_areasT:
            lista.append(row)
        # combo box
        combo_id = ttk.Combobox(self.worker_toplevel_sup, values=lista)
        combo_id.set(lista[0])
        combo_id.grid(row=4, column=1)
        # data
        id_worker = (old_data[5], )
        # agregar
        ttk.Button(self.worker_toplevel_sup, text="Actualizar", command = lambda : self.controlador.update_workers_sup_control((nm_w,
                                                                                                                    lnm_w,
                                                                                                                    ci_w,
                                                                                                                    date_w,
                                                                                                                    combo_id), id_worker)).grid(row=5, column = 0, padx=2, pady=15)
        # regresar
        ttk.Button(self.worker_toplevel_sup, text="Regresar", command = lambda : self.back_workers_tpl(name_supT, id_areasT)).grid(row=5, column=1, padx=2, pady=15)
    
    def close_workers_tpl(self):
        self.worker_toplevel_sup.grab_release()
        self.worker_toplevel_sup.destroy()
    
    def up_data_sup(self, iderA):
        # Verificamos que seleccione un registro
        try:
            # Generando variables de tablero
            id_product = self.tablero_sup.item(self.tablero_sup.selection())["text"]
            num_cons = self.tablero_sup.item(self.tablero_sup.selection())["values"][3]
        except Exception as e:
            self.messageShow("Favor seleccionar un registro para actualizar", 2)
            return
        # Generamos nueva ventana para actualizar data
        self.ventana_act_sup = Toplevel(self.window)
        self.ventana_act_sup.title("Actualizar data de registros")
        self.ventana_act_sup.resizable(width=False, height=False)
        self.ventana_act_sup.grab_set()
        # configurando validaciones
        validacion_limiteStr = self.ventana_act_sup.register(self.validacion_limite_str)
        validacion_limiteInt = self.ventana_act_sup.register(self.validacion_limite_int)
        # Asignando formulario
        Label(self.ventana_act_sup, text="Formulario para actualizar data\ndel registro seleccionado").grid(row=0, column=0, columnspan=2)
        Label(self.ventana_act_sup, text=f"Identificador de la fila seleccionada {id_product}").grid(row=0, column=2, pady=5)
        
        Label(self.ventana_act_sup, text="Cantidad").grid(row=1, column=0, pady=5)
        cnt = Entry(self.ventana_act_sup, validate="key", validatecommand=(validacion_limiteInt, "%P", 4))
        cnt.focus()
        cnt.grid(row=1, column=1, pady=5)
        
        Label(self.ventana_act_sup, text="Numero de consultas").grid(row=2, column=0, pady=5)
        nm_c = Entry(self.ventana_act_sup, validate="key", validatecommand=(validacion_limiteInt, "%P", 6))
        nm_c.grid(row=2, column=1, pady=5)
        
        Label(self.ventana_act_sup, text="Descripcion del item").grid(row=3, column=0, pady=5)
        desc_item = Entry(self.ventana_act_sup, validate="key", validatecommand=(validacion_limiteStr, "%P", 64))
        desc_item.grid(row=3, column=1, pady=5)
        
        Label(self.ventana_act_sup, text="Valor").grid(row=4, column=0, pady=5)
        val = Entry(self.ventana_act_sup, validate="key", validatecommand=(validacion_limiteInt, "%P", 8))
        val.grid(row=4, column=1, pady=5)
        
        Label(self.ventana_act_sup, text="Observacion").grid(row=5, column=0, pady=5)
        obs = Entry(self.ventana_act_sup, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        obs.grid(row=5, column=1, pady=5)
        # Falta agregar botones, y hacer las consultas update
        # Botones
        ttk.Button(self.ventana_act_sup, text="Actualizar", command= lambda : self.actualizar_bien_vista(iderA, cnt,
                                                                                                        nm_c,
                                                                                                        desc_item,
                                                                                                        val,
                                                                                                        obs,
                                                                                                        id_product,
                                                                                                        num_cons)).grid(row=6, column=0, columnspan=2, pady=15)
    
    def actualizar_bien_vista(self, id_area, cnt, nm_c, desc_item, val, obs, id_b, num_c):
        val = self.controlador.act_data_sup_query_control(cnt, nm_c, desc_item, val, obs, id_b, num_c)
        if val == None:
            self.rellenar_tabla_sup(id_area)
        else:
            messagebox.showerror("Error", f"{val}")
    
    def w_admin_main(self, user):
        # Asignando a main
        # self.window.geometry("800x600")
        # Mensajes label
        Label(self.window, text=f"Bienvenido {user}", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(25, 10))
        # Mostrando los supervisores en turno
        self.admin_table_sup = ttk.Treeview(self.window, height=10)
        # Asignando lugar
        self.admin_table_sup.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        # especificando columnas
        self.admin_table_sup["columns"] = ("c1", "c2", "c3")
        # Asignando nombres a las columnas
        self.admin_table_sup.heading("#0", text="ID supervisor")
        self.admin_table_sup.heading(column= "c1", text="Nombre")
        self.admin_table_sup.heading(column= "c2", text="Apellido")
        self.admin_table_sup.heading(column= "c3", text="Cedula")
        # Ajustar columnas al contenido
        for columna in self.admin_table_sup["columns"]:
            self.admin_table_sup.column(columna, width=100, minwidth=50, anchor=CENTER)
        # Llenando tabla
        self.fill_admin_table_sup()
        # Botones
        ttk.Button(self.window, text="Agregar supervisor", command = lambda : self.topLevel_admin_interface_add()).grid(row=2, column=0, pady=(5, 15))
        ttk.Button(self.window, text="Modificar Supervisor", command = lambda : self.topLevel_admin_interface_update()).grid(row=2, column=1, pady=(5, 15))
        ttk.Button(self.window, text="Eliminar Supervisor", command = lambda : self.topLevel_admin_interface_delete()).grid(row=2, column=2, pady=(5, 15))
        # Consultar usuarios admin
        Label(self.window, text="Consultar sobre los usuarios admin \ndisponibles", font=("Arial", 16, "bold")).grid(row=3, column=0, columnspan=4, pady=(0, 10))
        ttk.Button(self.window, text="Usuarios Admin", command = self.topLevel_admin_i).grid(row=4, column=0, columnspan=4, pady=(0, 10))
        # Administrar zonas del kino
        Label(self.window, text="Administrar las zonas de \ntrabajo", font=("Arial", 16, "bold")).grid(row=5, column=0, columnspan=2, pady=(5, 10))
        ttk.Button(self.window, text="Zonas de trabajo", command = self.zone_admin).grid(row=5, column=2, columnspan=2, pady=(5, 10))
        # Salir
        ttk.Button(self.window, text="Salir", command = self.label_main).grid(row=6, column=0, columnspan=4, pady=(5, 25))
        # pie de pagina
        self.pie_pagina(1, 2)
    
    def topLevel_admin_interface_delete(self):
        # testeando seleccion
        # Llamando query para eliminar data
        select_data = self.select_admin_table_sup()
        if isinstance(select_data, tuple):
            supervisor_id = select_data[3]
            # print(supervisor_id)
        else: 
            self.messageShow("Error, debe seleccionar una fila", 2)
            return
        empleados = self.get_trabajadores_supervisor(supervisor_id)
        # print(empleados)
        if empleados != []:
            self.messageShow("Se le advierte que no se puede eliminar\n ya que el supervisor tiene empleados a su\n cargo", 2)
            self.empleados_sup_mensaje(empleados)
            return
        else: 
            if self.messageAsk(f"Esta seguro de eliminar el registro {select_data}"):
                self.admin_query_customThree(3, old_info = select_data)
                # Actualizando tabla
                self.fill_admin_table_sup()
            else:
                self.messageShow("Se revirtio la eliminacion")
                return
    
    def empleados_sup_mensaje(self, data = []):
        toplevel_message = Toplevel()
        toplevel_message.title("Lista de empleados al cargo del sup ")
        toplevel_message.resizable(width=False, height=False)
        toplevel_message.grab_set()
        
        tabla_empleados = ttk.Treeview(toplevel_message, height=10)
        tabla_empleados["columns"] = ("c0", "c1", "c2", "c3", "c4",)
        tabla_empleados.heading("#0", text="ID")
        tabla_empleados.heading("c0", text="Nombre")
        tabla_empleados.heading("c1", text="Apellido")
        tabla_empleados.heading("c2", text="Cedula")
        tabla_empleados.heading("c3", text="Fecha de nacimiento")
        tabla_empleados.heading("c4", text="ID area")
        tabla_empleados.grid(row=0, column=0, columnspan=2, padx=50, pady=25)
        
        for row in data:
            tabla_empleados.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))
        
        ttk.Button(toplevel_message, text="Salir", command = lambda : toplevel_message.destroy()).grid(row=1, column=0, columnspan=2, padx=50, pady=15)
    
    def close_zone_admin(self):
        self.zona_toplevel.grab_release()
        self.zona_toplevel.destroy()
    
    def zone_admin(self):
        # Generando toplevel
        self.zona_toplevel = Toplevel(self.window)
        # self.zona_toplevel.geometry("800x600")
        self.zona_toplevel.title("Zonas de trabajo")
        # focus a la toplevel
        self.zona_toplevel.grab_set()
        # main de zonas kino
        Label(self.zona_toplevel, text="Tabla de las zonas de trabajo registradas").grid(row=0, column=0, columnspan=2, pady=25)
        self.zone_treeView = ttk.Treeview(self.zona_toplevel, height=10)
        self.zone_treeView.grid(row=1, column=0, rowspan=3)
        # Asignando columnas
        self.zone_treeView["columns"] = ("col0", "col1", "col2")
        # asignando data a las columnas
        self.zone_treeView.heading(column = "col0", text = "Nombre de area")
        self.zone_treeView.heading(column = "col1", text = "Codigo de zona")
        self.zone_treeView.heading(column = "col2", text = "id del supervisor")
        # Ajustar columnas al contenido
        for columna in self.zone_treeView["columns"]:
            self.zone_treeView.column(columna, width=100, minwidth=50, anchor=CENTER)
        # llenar tablas
        zone_list = self.fill_zona_treeview()
        if len(zone_list) > 0:
            for row in zone_list:
                self.zone_treeView.insert("", "end", text=row[0], values = (row[1], row[2], row[3]))
        else: self.zone_treeView.insert("", "end", text="No hay data")
        # botones para actualizar, agregar y eliminar datos
        ttk.Button(self.zona_toplevel, text="Agregar zonas", command = self.add_zone_tpl).grid(row=1, column=1)
        ttk.Button(self.zona_toplevel, text="Actualizar zonas", command = self.update_zone_tpl).grid(row=2, column=1)
        ttk.Button(self.zona_toplevel, text="Eliminar zonas", command = self.eliminar_zona).grid(row=3, column=1)
        # Regresar
        ttk.Button(self.zona_toplevel, text="Salir", command = lambda : self.close_zone_admin()).grid(row=4, column=0, columnspan=2)
    
    def eliminar_zona(self):
        if self.controlador.delete_zone_work_admin_control(self.zone_treeView) == None: return
        self.back_zone_toplevel()
    
    def update_zone_tpl(self):
        # Seleccion
        old_values = self.selec_zone_admin_table()
        if old_values == None: return
        # print(old_values)
        # limpiar toplevel
        self.limpiar_ventana(3)
        # configurando validaciones
        validacion_limiteStr = self.zona_toplevel.register(self.validacion_limite_str)
        validacion_limiteInt = self.zona_toplevel.register(self.validacion_limite_int)
        # widgedts
        Label(self.zona_toplevel, text="Nombre de area").grid(row=0, column=0)
        Label(self.zona_toplevel, text=f"area actual = {old_values[0]}", relief="sunken").grid(row=1, column=1)
        nm_area = ttk.Entry(self.zona_toplevel, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        nm_area.grid(row=1, column=0, pady=8)
        
        Label(self.zona_toplevel, text="Codigo de area").grid(row=2, column=0)
        Label(self.zona_toplevel, text=f"codigo actual ={old_values[1]}", relief="sunken").grid(row=3, column=1)
        cdg_area = ttk.Entry(self.zona_toplevel, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        cdg_area.grid(row=3, column=0, pady=8)
        # busqueda id -> cedula supervisor
        ci_id = self.query_busqueda_sup_zone(old_values[2])
        Label(self.zona_toplevel, text="Seleccionar supervisor designado para el area").grid(row=4, column=0, pady=10)
        # generando listado de combo box
        lista_supervisores = ["Seleccionar..."]
        # pedir supervisores
        cedulas_sups = self.get_ci_sups()
        for cedula in cedulas_sups:
            if cedula != ci_id[0]: lista_supervisores.append(cedula)
        # seleccionar la primera
        combo = ttk.Combobox(self.zona_toplevel, values=lista_supervisores, state="readonly")
        combo.set(lista_supervisores[0])
        combo.grid(row=4, column=1, padx=5, pady=10)
        # Actualizar
        ttk.Button(self.zona_toplevel, text="Actualizar", command = lambda : self.query_update_zone(parameters = (nm_area.get(),
                                                                                                                    cdg_area.get(),
                                                                                                                    combo.get(),
                                                                                                                    old_values[0],
                                                                                                                    old_values[1]))).grid(row=5, column=1)
        # salir
        ttk.Button(self.zona_toplevel, text="Regresar", command = self.back_zone_toplevel).grid(row=5, column=0)
    
    def add_zone_tpl(self):
        # limpiar toplevel
        self.limpiar_ventana(3)
        # configurando validaciones
        validacion_limiteStr = self.zona_toplevel.register(self.validacion_limite_str)
        validacion_limiteInt = self.zona_toplevel.register(self.validacion_limite_int)
        # agregando widgets al toplevel
        Label(self.zona_toplevel, text="Agregar el nombre del area de trabajo").grid(row=0, column=0, pady=10)
        nm_a = ttk.Entry(self.zona_toplevel, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        nm_a.grid(row=0, column=1, pady=10)
        
        Label(self.zona_toplevel, text="Agregar el codigo del area de trabajo").grid(row=1, column=0, pady=10)
        cdg_a = ttk.Entry(self.zona_toplevel, validate="key", validatecommand=(validacion_limiteStr, "%P", 16))
        cdg_a.grid(row=1, column=1, pady=10)
        
        Label(self.zona_toplevel, text="Seleccionar supervisor designado para el area").grid(row=2, column=0, pady=10)
        # generando listado de combo box
        lista_supervisores = ["Seleccionar..."]
        # pedir supervisores
        cedulas_sups = self.get_ci_sups()
        for cedula in cedulas_sups:
            lista_supervisores.append(cedula)
        # seleccionar la primera
        combo = ttk.Combobox(self.zona_toplevel, values=lista_supervisores, state="readonly")
        combo.set(lista_supervisores[0])
        combo.grid(row=2, column=1, padx=5, pady=10)
        # insertar data
        ttk.Button(self.zona_toplevel, text="Agregar", command = lambda : self.query_add_zone(parameters = (nm_a.get(),
                                                                                                cdg_a.get(),
                                                                                                combo.get()))).grid(row=3, column=1)
        # salir
        ttk.Button(self.zona_toplevel, text="Regresar", command = self.back_zone_toplevel).grid(row=3, column=0)
    
    def back_zone_toplevel(self):
        # destruimos el top level
        self.zona_toplevel.destroy()
        # generamos otro toplevel
        self.zone_admin()
    
    def three_message_interface(self, toplevel, msg = ""):
        # Mostrando mensaje por pantalla
        self.messageShow(msg)
        # Rellenar nuevas filas en la tabla de supervisores
        self.fill_admin_table_sup()
        # Destruir toplevel
        toplevel.destroy()
    
    def topLevel_admin_interface_update(self):
        # Datos anteriores
        old_data = self.select_admin_table_sup()
        if old_data == None:
            self.messageShow("Se debe seleccionar un registro", 2)
            return
        # testeando seleccion
        self.update_window = Toplevel(self.window)
        self.update_window.title("Agregar datos ventana")
        self.update_window.resizable(width=False, height=False)
        # configurando validaciones
        validacion_limiteStr = self.update_window.register(self.validacion_limite_str)
        validacion_limiteInt = self.update_window.register(self.validacion_limite_int)
        # agregando labels
        Label(self.update_window, text=f"Antigua información : {old_data[0]}").grid(row=0, column=0, pady=5)
        Label(self.update_window, text="Nombre del supervisor\nQue se actualizará").grid(row=1, column=0, pady=5)
        name = Entry(self.update_window, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        name.grid(row=1, column=1, pady=5)
        
        Label(self.update_window, text=f"Antigua información : {old_data[1]}").grid(row=2, column=0, pady=5)
        Label(self.update_window, text="Apellido del supervisor\nQue se actualizará").grid(row=3, column=0, pady=5)
        last_name = Entry(self.update_window, validate="key", validatecommand=(validacion_limiteStr, "%P", 32))
        last_name.grid(row=3, column=1, pady=5)
        
        Label(self.update_window, text=f"Antigua información : {old_data[2]}").grid(row=4, column=0, pady=5)
        Label(self.update_window, text="Cedula del supervisor\nQue se actualizará").grid(row=5, column=0, pady=5)
        dni = Entry(self.update_window, validate="key", validatecommand=(validacion_limiteInt, "%P", 9))
        dni.grid(row=5, column=1, pady=5)
        uptd_data = (old_data[0],old_data[1],old_data[2])
        # query
        ttk.Button(self.update_window, text="Actualizar", command = lambda: self.actualizar_supervisor_vista(uptd_data,
                                                                                                        name.get(), last_name.get(), dni.get())).grid(row= 6, column=0, columnspan=2)
        
    
    def actualizar_supervisor_vista(self, old_data, name, lastn, dni):
        if dni == "" and name == "" and lastn == "":
            self.messageShow("Debe llenar los campos", 2)
            return
        else:
            self.controlador.update_sup_from_admin_control(old_data, name, lastn, dni, self.update_window)
            self.fill_admin_table_sup()
    
    def topLevel_admin_interface_add(self):
        # ventana add
        self.add_window = Toplevel(self.window)
        # print(type(self.add_window))
        self.add_window.title("Ventana de agregar")
        self.add_window.resizable(width=False, height=False)
        self.add_window.grab_set()
        # configurando validaciones
        validacion_limiteStr = self.add_window.register(self.validacion_limite_str)
        validacion_limiteInt = self.add_window.register(self.validacion_limite_int)
        # Labels
        Label(self.add_window, text="Nombre del supervisor nuevo").grid(row=0, column=0, pady=5)
        name = Entry(self.add_window, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        name.grid(row=0, column=1, pady=5)
        
        Label(self.add_window, text="Apellido del supervisor nuevo").grid(row=1, column=0, pady=5)
        last_name = Entry(self.add_window, validate="key", validatecommand=(validacion_limiteStr, "%P", 42))
        last_name.grid(row=1, column=1, pady=5)
        
        Label(self.add_window, text="Cedula del supervisor nuevo").grid(row=2, column=0, pady=5)
        dni = Entry(self.add_window, validate="key", validatecommand=(validacion_limiteInt, "%P", 9))
        dni.grid(row=2, column=1, pady=5)
        # data
        # boton
        btn = ttk.Button(self.add_window, text="Agregar valores", command = lambda : self.controlador.add_sup_from_admin_control(name.get(), last_name.get(), dni.get()))
        btn.grid(row=3, column = 0, columnspan=2)
    
    def topLevel_admin_i(self):
        self.toplevel_admin_window = Toplevel(self.window)
        self.toplevel_admin_window.title("Panel de admins")
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
        ttk.Button(self.toplevel_admin_window, text="Eliminar", command = self.eliminar_admin).grid(row=2, column=1)
    
    def eliminar_admin(self):
        val = self.controlador.admin_deleteW_control(self.table_admin_data)
        if isinstance(val, int):
            self.fill_admin_table()
        else: return
    
    def toplevel_admin_addW(self):
        # Limpiar ventana
        self.limpiar_ventana(opc = 2)
        # configurando validaciones
        validacion_limiteStr = self.toplevel_admin_window.register(self.validacion_limite_str)
        validacion_limiteInt = self.toplevel_admin_window.register(self.validacion_limite_int)
        # Formulario
        Label(self.toplevel_admin_window, text="Ingresar Usuario").grid(row=0, column=0, padx=320, pady=(50, 15))
        user = ttk.Entry(self.toplevel_admin_window, validate="key", validatecommand=(validacion_limiteStr, "%P", 32))
        user.grid(row=0, column=1)
        Label(self.toplevel_admin_window, text="Ingresar Contraseña").grid(row=1, column=0, padx=320, pady=(0, 15))
        password = ttk.Entry(self.toplevel_admin_window, validate="key", validatecommand=(validacion_limiteStr, "%P", 16))
        password.grid(row=1, column=1)
        # Volver
        ttk.Button(self.toplevel_admin_window, text="Volver", command =  self.volver_toplevel_admin_i).grid(row=2, column=0, padx=(160, 0), pady=(0, 25))
        # Agregar
        ttk.Button(self.toplevel_admin_window, text="Subir", command = lambda : self.controlador.admin_register_control((user.get(), password.get()))).grid(row=2, column=1, padx=(0, 160), pady=(0, 25))
    
    def volver_toplevel_admin_i(self):
        self.toplevel_admin_window.destroy()
        self.topLevel_admin_i()
    
    def generar_excel(self):
        # data de bienes
        bienes = self.controlador.query_tomar_data_bienes_controlador()
        if bienes == None: return
        # Leer el archivo contador
        with open('config\\Excels\\contador.txt', 'r') as file:
            current_count = int(file.read().strip())
        # sumar
        current_count+=1
        # woorkbook
        book = Workbook()
        sheet = book.active
        # Columnas de bienes por zona
        sheet['A1'] = "ID Bienes"
        sheet['A1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        sheet['B1'] = "ID Area"
        sheet['B1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        sheet['C1'] = "Cantidad"
        sheet['C1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        sheet['D1'] = "Numero de consultas"
        sheet['D1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        sheet['E1'] = "Descripcion del item"
        sheet['E1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        sheet['F1'] = "Valor"
        sheet['F1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        sheet['G1'] = "Observacion"
        sheet['G1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        sheet['H1'] = "Codigo QR"
        sheet['H1'].font = Font(name='Arial', size=12, bold=True, italic=False)
        
        for i in range(2,len(bienes)):
            sheet[f'A{i}'] = bienes[i-2][0]
            sheet[f'B{i}'] = bienes[i-2][1]
            sheet[f'C{i}'] = bienes[i-2][2]
            sheet[f'D{i}'] = bienes[i-2][3]
            sheet[f'E{i}'] = bienes[i-2][4]
            sheet[f'F{i}'] = bienes[i-2][5]
            sheet[f'G{i}'] = bienes[i-2][6]
            sheet[f'H{i}'] = bienes[i-2][7]
        
        # Iterar sobre las celdas de la fila 1 desde A1 hasta H1
        for column in range(1, 9):  # Columnas A hasta H (8 columnas)
            cell = sheet.cell(row=len(bienes+1), column=column)
            # Establecer el estilo del borde cuadriculado para cada celda
            border_style = 'thin'  # Puedes ajustar el grosor del borde si lo deseas
            border = Border(left=Side(style=border_style),
                            right=Side(style=border_style),
                            top=Side(style=border_style),
                            bottom=Side(style=border_style))
            cell.border = border
        
        name_path = f"Excel_Bienes{current_count:4}"
        book.save(f"config\\Excels\\{name_path}.xlsx")
        
        # Actualizar el valor del contador en el archivo contador.txt
        with open('config\\Excels\\contador.txt', 'w') as file:
            file.write(str(current_count))