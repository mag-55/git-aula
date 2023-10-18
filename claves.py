#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import inicio as inc

"""
Este modulo cuntiene distintas func para chequear ek ingreso de
los usuarios asi como validar claves y confimar inserción, edición
y eliminación de rigistros todo requerido por las clases de formulario.py
"""

# CHEQUEO DE INGRESO DE USUARIOS AL SISTEMA


# chequea que el usuario sea el administrador para poder generar usuarios
def chequear_a(lista):

    if lista[0].get() == "admin" and lista[1].get() == "admingral":
        valor = "usuario"
        inc.abrir(valor)

    else:
        messagebox.showwarning(title="DENEGADO!", message="Ingrese clave de ADMINISTRADOR!!!")
        lista[0].delete(0, tk.END)
        lista[0].focus()


# chequea que el usuario uno de los ya creados por el administrador
def chequear_u(respuesta):

    if respuesta:
        inc.abrir()

    else:
        messagebox.showwarning(title="DENEGADO!", message="Su autenticación es Incorrecta")


# VERIFICAION DE REGISTRO DE CLAVES DE USUARIOS

# ----------- FUNC VERIFICA LA LONGITUD -----------

def verificar_Long(cont, l1, l2):
    """ Esta func recibe 3 parametros, una cadena y 1 o 2 enteros(opcinal),
    la longitud de la cadena es comparada con los 2 enteros
    para controlar el largo min y max """

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

# ----------- FUNC VERIF ALFANUMERICO -----------


def verifcar_Simb(cont):
    """ Verifica que la cadena sea alfanumerica """

    verif = cont.isalnum()
    return verif

# ----------- FUNC VALIDAR USUARIO -----------

def validarUsuario(lista):
    """ Aquí se utilizan las dos verificaciones anteriores para saber si
    la cadena tiene la longitud correcta y no contiene mas que letras y
    numeros, si todo esta correcto, se habilita el siguente casillero
    poniendo el foco en este """

    longitud = verificar_Long(lista[0].get(), 6, 12)
    sin_simbolos = verifcar_Simb(lista[0].get())

    if longitud is False:
        messagebox.showerror(title="ERROR!", message="El nombre de usuario debe tener un largo de entre 6 y 12 caracteres")
        lista[0].focus()

    elif sin_simbolos is False:
        messagebox.showerror(title="ERROR!", message="El nombre de usuario debe tener unicamente letras y numeros")
        lista[0].focus()

    else:
        messagebox.showinfo(title="FELICITACIONES!!!", message="El usuario fue corretamente conformado")
        lista[1].configure(state='normal')
        lista[1].focus()

# ----------- FUNC VALIDAR CLAVE -----------

def validarClave(lista):
    """ Se hace uso de las mismas verificaciones, longitud y alfanumerica,
    se verifica que el usuario sea distinto a la clave que esta tenga
    mayúsculas y minúsculas """

    longitud = verificar_Long(lista[1].get(), 8, 0)
    sin_simbolos = verifcar_Simb(lista[1].get())

    if longitud is False:
        messagebox.showerror(title="ERROR!", message="La clave debe tener un minimo de 8 caracteres")
        lista[1].focus()

    elif sin_simbolos is False:
        messagebox.showerror(title="ERROR!", message="La clave debe tener solo letras y/o números sin espaios u otros simbolos")
        lista[1].focus()

    elif lista[0].get() == lista[1].get():
        messagebox.showwarning(title="CUIDADO!", message="EL USUARIO Y LA CLAVE NO PUEDEN SER IGUALES")
        lista[1].focus()

    elif lista[1].get().islower() is False and lista[1].get().isupper() is False:
        messagebox.showinfo(title="FELICIDADES!!!", message="Clave correctamente conformada, confirmela!!!")
        lista[2].configure(state='normal')
        lista[2].focus()

    else:
        messagebox.showerror(title="ERROR!", message="La clave debe tener al menos una letra mayúscula")
        lista[1].focus()

# ----------- FUNC CHEQUEAR Cl == CCl -----------

def compararClaves(lista):
    """ Se comparan clave y confirmación, ambas debenser iguales """

    if not lista[2].get() == lista[1].get():
        messagebox.showwarning(title="CUIDADO!", message="LA CLAVE Y LA CONFIMACION DE ESTA DEBEN SER IGUALES")
        lista[2].focus()
        
    else:
        messagebox.showinfo(title="EN HORA BUENA!", message="CLAVE CONFIRMADA!!!")
        for i in range(len(lista)):  # ver!!!... no tiene sentido
            lista[i].configure(state='normal')
