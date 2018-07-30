#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from registro import Registros


""" FORMULARIO DE INGRESO permite accder a la app en si """


def chequear():
	registros = Registros()

	if cajaUno.get() == "adm" and cajaDos.get() == "1":
		registros.registrarUs()
		raiz.withdraw()

	elif cajaUno.get() == "gerardo" and cajaDos.get() == "321":
		registros.registrarGral()
		raiz.withdraw()

	else:
		messagebox.showwarning(title= "Denegado", message= "Su autenticación es Incorrecta")

	# Borrar cajas de texto
	cajaUno.delete(0, END)
	cajaDos.delete(0, END)


#----------- VENTANA ACCESO -----------
raiz = Tk()
raiz.resizable(0, 0)
raiz.title("Ingreso de Usuarios")

#----------- MARCO UNO -----------
marcoUno = Frame(raiz, width= "400", height= "100")
marcoUno.grid(column= 0, row=0) 

#----------- ETIQUETAS UNO-----------
etiquetaUno = Label(marcoUno, text= "Usuario:")
etiquetaUno.grid(column= 0, row= 0, padx= 5)

etiquetaDos = Label(marcoUno, text= "Clave:")
etiquetaDos.grid(column= 0, row= 1, padx= 5)

#----------- CAJAS TEXTO UNO-----------
cajaUno = Entry(marcoUno)
cajaUno.grid(column= 1, row= 0, padx= 5, pady= (10, 5))

cajaDos = Entry(marcoUno, show= "*")
cajaDos.grid(column= 1, row= 1, padx= 5, pady= (5, 10))

#----------- BOTONES -----------
botonUno = Button(marcoUno, text= "Aceptar", width= "25", command= chequear)
botonUno.grid(row= 2, columnspan= 2)

botonDos = Button(marcoUno, text= "Salir", width= "25", command= quit)
botonDos.grid(row= 3, columnspan= 2, pady= 5)


raiz.mainloop()