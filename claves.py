# !/usr/bin/python3.8
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import inicio as inc



# CHEQUEO DE INGRESO de usuarios al sistema


def chequear(lista):
    if lista[0].get() == "adm" and lista[1].get() == "gral":
        inc.abrir()
    else:
        messagebox.showwarning(
            title="DENEGADO!", message="Su autenticación es Incorrecta")
        lista[0].delete(0, tk.END)
        lista[0].focus()

# VERIFICAION DE REGISTRO DE CLAVES de usuarios

#----------- FUNC VERIF LONGITUD -----------


def verificar_Long(cont, l1, l2):
    longitud = len(cont)
    if l2 != 0:
        if longitud >= l1 and longitud <= l2:
            return True
        else:
            return False

    if longitud >= l1:
        return True
    else:
        return False

#----------- FUNC VERIF ALFANUMERICO -----------


def verifcar_Simb(cont):
    verif = cont.isalnum()
    return verif

#----------- FUNC VALIDAR USUARIO -----------


def validarUsuario(lista):
    longitud = verificar_Long(lista[0].get(), 6, 12)
    sinSimbolos = verifcar_Simb(lista[0].get())

    if longitud == False:
        messagebox.showerror(title="ERROR!", message="El nombre de usuario debe tener un largo de entre 6 y 12 caracteres")
        lista[0].focus()
    elif sinSimbolos == False:
        messagebox.showerror(title="ERROR!", message="El nombre de usuario debe tener unicamente letras y numeros")
        lista[0].focus()
    else:
        messagebox.showinfo(title="FELICITACIONES!!!", message="El usuario fue corretamente conformado")
        lista[1].configure(state='normal')
        lista[1].focus()
#----------- FUNC VALIDAR CLAVE -----------


def validarClave(lista):
    longitud = verificar_Long(lista[1].get(), 8, 0)
    sinSimbolos = verifcar_Simb(lista[1].get())

    if longitud == False:
        messagebox.showerror(title="ERROR!", message="La clave debe tener un minimo de 8 caracteres")
        lista[1].focus()
    elif sinSimbolos == False:
        messagebox.showerror(title="ERROR!", message="La clave debe tener solo letras y/o números sin espaios u otros simbolos")
        lista[1].focus()
    elif lista[0].get() == lista[1].get():
        messagebox.showwarning(title="CUIDADO!", message="EL USUARIO Y LA CLAVE NO PUEDEN SER IGUALES")
        lista[1].focus()
    elif lista[1].get().islower() == False and lista[1].get().isupper() == False:
        messagebox.showinfo(title="FELICIDADES!!!", message="Clave correctamente conformada, confirmela!!!")  
        lista[2].configure(state='normal')
        lista[2].focus()   
    else:
        messagebox.showerror(title="ERROR!", message="La clave debe tener al menos una letra mayúscula")
        lista[1].focus()

#----------- FUNC CHEQUEAR Cl == CCl -----------


def compararClaves(lista):
    if not lista[2].get() == lista[1].get():
        messagebox.showwarning(title="CUIDADO!", message="LA CLAVE Y LA CONFIMACION DE ESTA DEBEN SER IGUALES")
        lista[2].focus()
    else:
        messagebox.showinfo(title="EN HORA BUENA!", message="CLAVE CONFIRMADA!!!")
        for i in range(len(lista)):
            lista[i].configure(state='normal')
