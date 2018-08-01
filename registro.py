
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from componentes import *

""" Esta clase agrupa los distintos formularios de registro"""

class Registros():

	def registrarUs(self):
		ventana = Toplevel()
		ventana.geometry("500x700")
		ventana.resizable(0, 0)
		ventana.title("REGISTRO DE USUARIOS")

		marcoUno = Frame(ventana, width= "500", height= "650")
		marcoUno.grid()

		lista = ["NOMBRE", "APELLIDO", "DNI", "FECHA", "EDAD", "DIRECCION", "TEL", "MAIL"]
		duplicar(marcoUno, lista, e=True, c=True)
		
		
		#ordenar(crear_Rb(marcoUno, "Masculino", 1), 8, 1, 5)

		ordenar(crear_B(ventana, "SALIR", "10"), 8, 0)




	def registrarGral(self):
		ventana = Toplevel()
		ventana.title("BIENVENIDO AL AULA")
		





	