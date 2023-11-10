#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
En este archivo se encuentran dos funciones, iniciar y abrir,
la primera contiene el root y ejecuta la func acceder de la 
clase Acceso(acceso.py), la segunda contiene las otras dos ventanas 
que componen el programa de regintro escolar, según el valor que 
se ingrese  a esta última abrira la ventana de RegistroUsuario(registroUsuario.py) o
RegistroGral(registroGral.py), 
"""

import tkinter as tk
import acceso as form
import registroUsuario as form_dos
import registroGral as form_tres


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
        RegU = form_dos.RegistroUsuario(ventana)
        RegU.registrarUs()
        
    else:
        RegG = form_tres.RegistroGral(ventana)
        RegG.registrarGral()


if __name__ == "__main__":
    iniciar()

