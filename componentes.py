#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import *

def ordenar(obj="", fila=0, col=0, x=0, y=0, coord="", cols=1, rows=1):
	widget=obj.grid(row=fila, column=col,  padx=x, pady=y, sticky=coord, columnspan=cols, rowspan=rows)


def comp_E(contenedor, titulo= ""):
	etiquetaUno = Label(contenedor, text= titulo)
	ordenar(etiquetaUno, 0, 0, 5)

def compo_C():
	cajaUno = Entry(marcoUno, width= "50")
	ordenar()

def comp_B():
	botonUno = Button(marcoUno, text= "Aceptar", width= "25", command= chequear)
	ordenar()