import tkinter

def config_window(window, title = ""):
    return window.title(title)

def config_toplevel(toplevel, title = ""):
    return toplevel.title(title)

def create_button(window, toplevel):
    tkinter.Button(window, text="Destruir Toplevel", command= lambda : toplevel.destroy()).pack(anchor='center')

window = tkinter.Tk()

config_window(window, "Ventana Prueba")

toplevel = tkinter.Toplevel(window)

config_toplevel(toplevel, "Top level Nuevo")

create_button(window, toplevel)

window.mainloop()