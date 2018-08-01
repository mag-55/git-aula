
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import *

"""Este módulo está orientado a crear componentes sencillos de un formulario"""

#var = IntVar()

def ordenar(obj="", fila=0, col=0, x=0, y=0, coord="", cols=1, rows=1):
	widget=obj.grid(row=fila, column=col,  padx=x, pady=y, sticky=coord, columnspan=cols, rowspan=rows)


def duplicar(contenedor, lista, e=False, c=False, b=False):
	for i in range(len(lista)):
		if e == True:
			ordenar(crear_E(contenedor, lista[i]), i, 0, 5)
		if c == True:
			ordenar(crear_C(contenedor, "50"), i, 1, 5, 5)


def crear_E(contenedor, titulo= ""):
	etiqueta = Label(contenedor, text= titulo)
	return etiqueta


def crear_C(contenedor, ancho= "15"):
	caja = Entry(contenedor, width= ancho)
	return caja


def crear_B(contenedor, titulo= "", ancho= "", comando= ""):
	boton = Button(contenedor, text= titulo, width= ancho, command= comando)
	return boton


# def crear_Rb(contenedor, titulo="", valor= 0, var= var ):
# 	radioBoton = Radiobutton(contenedor, text= titulo, value= valor, variable= var)
# 	return radioBoton


