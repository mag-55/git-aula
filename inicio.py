# !/usr/local/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import formularios as form

def iniciar():
	raiz=tk.Tk()
	raiz.resizable(0, 0)
	raiz.title("Acceso")
	acc=form.Acceso(raiz)
	acc.acceder()		
	raiz.mainloop()		


def abrir(valor=""):
	ventana=tk.Toplevel()							
	ventana.resizable(0, 0)
	
	if valor=="usuario":
		regU=form.registroUsuario(ventana)
		regU.registrarUs()
	else:
		regG=form.registroGral(ventana)
		regG.registrarGral()


if __name__=="__main__":
	iniciar()	