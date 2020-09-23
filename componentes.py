#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk

"""
Este módulo está orientado a crear componentes sencillos de un formulario,
se divide en dos partes, crear elementos, aqui hay distintas func que devuelven
distintos obj correspondientes a diferentes widges tk.
Luego todas estas funciones son llamadas por la func ordenar la cual tiene distintos 
parametros para ubicar los widges donde corresponda. 
"""

# ---------- ORDENAR ELEMENTOS ------------------


def ordenar(obj="", fila=0, col=0, x=0, y=0, coord="", cols=1, rows=1):
    obj.grid(row=fila, column=col, padx=x, pady=y, sticky=coord, columnspan=cols, rowspan=rows)


# ---------- CREAR ELEMENTOS ------------------

def crear_M(contenedor, ancho="10", alto="10"):
    marco = tk.Frame(contenedor, width=ancho, height=alto)
    return marco


def crear_E(contenedor, titulo=""):
    etiqueta = tk.Label(contenedor, text=titulo)
    return etiqueta


def crear_C(contenedor, ancho="15", texv=""):
    caja = tk.Entry(contenedor, width=ancho, textvariable=texv)
    return caja


def crear_B(contenedor, titulo="", ancho="10", comando=""):
    boton = tk.Button(contenedor, text=titulo, width=ancho, command=comando)
    return boton


def crear_Sp(contenedor, valores="", ancho="20", estado="", posicion="", texv="", comando=""):
    listaSpin = tk.Spinbox(contenedor, values=valores, width=ancho, state=estado, justify=posicion, textvariable=texv, command=comando)
    return listaSpin


def crear_Rb(contenedor, titulo="", valor=0, var=""):
   radioBoton = tk.Radiobutton(contenedor, text=titulo, value=valor, variable=var)
   return radioBoton


def crear_Lb(contenedor, ancho="", alto="", modo="SINGLE"):
    cajaList = tk.Listbox(contenedor, width=ancho, height=alto, selectmode=modo)
    return cajaList
