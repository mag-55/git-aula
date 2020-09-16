#!/usr/bin/python3
#-*- coding: utf-8 -*-

import tkinter as tk
import formularios as form

def iniciar():
    raiz = tk.Tk()
    raiz.resizable(0, 0)
    raiz.title("Acceso")
    acc = form.Acceso(raiz)
    acc.acceder()
    raiz.mainloop()


def abrir(valor=""):
    ventana = tk.Toplevel()
    ventana.resizable(0, 0)

    if valor == "usuario":
        RegU = form.RegistroUsuario(ventana)
        RegU.registrarUs()
    else:
        RegG = form.RegistroGral(ventana)
        RegG.registrarGral()


if __name__ == "__main__":
    iniciar()

