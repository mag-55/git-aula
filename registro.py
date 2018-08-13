
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from componentes import *

""" Esta clase agrupa los distintos formularios de registro"""

class Registros():

	def registrarUs(self):
		ventana = Toplevel()
		ventana.geometry("500x700")
		ventana.resizable(0, 1)
		ventana.title("REGISTRO DE USUARIOS")

		marcoUno = Frame(ventana, width= "500", height= "650", bg= "red")
		marcoUno.grid()
		marcoDos = Frame(ventana, width= "500", height= "50", bg= "green")
		marcoDos.grid()

		lista = ["NOMBRE", "APELLIDO", "DNI", "FECHA", "EDAD", "DIRECCION", "TEL", "MAIL"]
		lista2 = ["ACEPTAR", "SALIR"]
		comando = [quit, quit]
		duplicarEtiqueta(marcoUno, lista)
		duplicarCaja(marcoUno, lista)
		duplicarBoton(marcoDos, lista2, comando, 0)
		
		if duplicarCaja(marcoUno, lista)[0].get() == "x":
			print("ok")
		
		ventana = Toplevel()
		ventana.title("BIENVENIDO AL AULA")
		




	