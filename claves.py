# !/usr/local/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import inicio as inc 

#CHEQUEO DE INGRESO de usuarios al sistema 

def chequear(lista):
	if lista[0].get() == "adm" and lista[1].get() == "gral":
		inc.abrir()
	else:
		messagebox.showwarning(title= "DENEGADO!", message= "Su autenticación es Incorrecta")
		lista[0].delete(0, tk.END)
		lista[0].focus()

#VERIFICAION DE REGISTRO DE CLAVES de usuarios 

#----------- FUNC VERIF LONGITUD -----------

def verificar_Long(cont, l1, l2):
	longitud=len(cont)
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

def validarUsuario(usuario):
	longitud=verificar_Long(usuario[7].get(), 6, 12)
	sinSimbolos=verifcar_Simb(usuario[7].get())

	if longitud == False:
		messagebox.showinfo(title="ATENCION!", message="El nombre de usuario debe tener un largo de entre 6 y 12 caracteres")
		usuario[7].focus()
	elif sinSimbolos == False:
		messagebox.showinfo(title="ATENCION!", message="El nombre de usuario debe tener unicamente letras y numeros")
		usuario[7].focus()
	else:
		print("ok usuario") #se guarda

#----------- FUNC VALIDAR CLAVE -----------

def validarClave(clave):
	longitud=verificar_Long(clave[8].get(), 8, 0)
	sinSimbolos=verifcar_Simb(clave[8].get())

	if longitud == False:
		messagebox.showinfo(title="ATENCION!", message="La clave debe tener un minimo de 8 caracteres")
	elif sinSimbolos == False:
		messagebox.showinfo(title="ATENCION!", message="La clave debe tener solo letras y/o números sin espaios u otros simbolos")
	elif clave[8].get().isalpha() == False and clave[8].get().isdigit() == False and clave[8].get().islower() == False and clave[8].get().isupper() == False:
		print("OK CLAVE")
	else:
		messagebox.showinfo(title="ATENCION!", message="La clave debe ser alfanumerica y tener almenos una letra mayúscula")

#----------- FUNC CHEQUEAR Us != Cl -----------

def comparar_Us_Cl(lista):
	usuario=lista[7].get()
	clave=lista[8].get()
	if usuario == clave:
		messagebox.showinfo(title="ATENCION!", message="EL USUARIO Y LA CLAVE NO PUEDEN SER IGUALES")
		lista[8].delete(0, tk.END)
		lista[8].focus()

#----------- FUNC CHEQUEAR Us != Cl -----------

def compararClaves(lista):
	clave1=lista[8].get()
	clave2=lista[9].get()
	if clave1 != clave2:
		messagebox.showinfo(title="ATENCION!", message="LA CLAVE Y LA CONFIMACION DE ESTA DEBEN SER IGUALES")
		lista[9].delete(0, tk.END)
		lista[9].focus()


