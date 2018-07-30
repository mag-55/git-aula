#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from componentes import comp_E

""" Esta clase agrupa los distintos formularios de registro"""

class Registros():

	def registrarUs(self):
		ventana = Toplevel()
		ventana.geometry("500x700")
		ventana.resizable(0, 0)
		ventana.title("REGISTRO DE USUARIOS")
		marcoUno = Frame(ventana, width= "500", height= "650")
		marcoUno.grid()
		comp_E(marcoUno, "NOMBRE:")                                  
		#etiquetaUno = Label(marcoUno, text= "Nombre:")
		#etiquetaUno.grid(row= 0, column= 0, padx= 5)
		cajaUno = Entry(marcoUno, width= "50")
		cajaUno.grid(row= 0, column= 1, padx= 5, pady= 5)


	def registrarGral(self):
		ventana = Toplevel()
		ventana.title("BIENVENIDO AL AULA")
		





	