# Librerias
# importando libreria Pillow - convert image
from PIL import ImageTk, Image
# importando libreria grafica Tkainter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# fin de librerias
# Declarando clase vista
class View:
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
    
    def toplevel_login_sup(self):
        self.sesion_level = Toplevel()
        self.sesion_level.title("Inicio de sesion del supervisor de area")
        Label(self.sesion_level, text="Sesion de Supervisores").grid(row=0, column=0, columnspan=2)
        Label(self.sesion_level, text="Para verificar si tiene permisos\ncomo supervisor digite su numero de cedula").grid(row=1, column=0)
        ci_sesion = Entry(self.sesion_level)
        ci_sesion.grid(row=1, column=1)
        ttk.Button(self.sesion_level, text="Cargar data", command= lambda: self.sesion_sup_ci(ci_sesion.get())).grid(row=2, column=0, columnspan=2)
    
    def main_sup_panel(self, id_sup):
        # Limpiamos pantalla
        self.limpiar_ventana()
        # Recopilando data del id sesion
        query = "SELECT * FROM supervisor_area_kino WHERE id_supervisor = ?"
        parameters = (id_sup, )
        fetch = self.run_query(query, parameters)
        print(fetch)
        name = fetch[0][1]
        
        Label(self.window, text=f"Supervisor encargado {name}").grid(row=0, column=0, columnspan=3, pady=10, padx=25)
        self.tablero_sup = ttk.Treeview(self.window, height=10)
        # asignando en main window
        self.tablero_sup.grid(row=1, column=0, columnspan=3)
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
        ttk.Button(self.window, text="Salir", command = self.label_main).grid(row=2, column=2)
        # pie de pagina
        self.pie_pagina()
    
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
        Label(self.ventana_act_sup, text=f"Identificador de la fila seleccionada {id_product}").grid(row=0, column=2)
        
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
    
    def sesion_sup_ci(self, ci):
        query = "SELECT * FROM supervisor_area_kino WHERE cedula = ?"
        parameters = (ci, )
        fetch = self.run_query(query, parameters)
        if isinstance(fetch, str) == True:
            messagebox.showwarning(title="Error en la data",
                                    message="No se encontraron registros con esta cedula")
        else:
            print(f"fetch[0][0] {fetch[0][0]}")
            query2 = "SELECT * FROM supervisor_sesion WHERE id_supervisor = ?"
            parameters2 = (fetch[0][0], )
            fetch2 = self.run_query(query2, parameters2)
            # print(fetch2) -> testeo
            if isinstance(fetch2, str) == True: messagebox.showwarning("Mensaje de sesion", "No tiene permisos para iniciar sesion")
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
        