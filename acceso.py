#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import componentes as cpt
import claves as clv
from formularios import Manejo_registros

# FORMULARIO DE INGRESO permite accder a la aplicación en si
class Acceso:

    def __init__(self, raiz):
        self.raiz = raiz
        self.listaCaja = []
        self.listaBoton = []
        self.listaEtiqueta = []
        self.mr = Manejo_registros()

    # ----------- VENTANA ACCESO -----------

    def acceder(self):
        lista = ("USUARIO:", "CLAVE:")
        lista2 = ("ENTRAR", "SALIR")
        comando = [self.chequear, self.cerrar]

        # ----------- MARCO CERO, UNO Y DOS-----------

        marcoCero = cpt.crear_M(self.raiz, "400", "100")
        cpt.ordenar(marcoCero, 0, 0)

        marco_uno = cpt.crear_M(self.raiz, "400", "100")
        cpt.ordenar(marco_uno, 1, 0)

        marco_dos = cpt.crear_M(self.raiz, "400", "50")
        cpt.ordenar(marco_dos, 2, 0)

        # ----------- ETIQUETA mUNO-----------

        titulo = cpt.crear_E(marcoCero, "Ingrese su Usuario")
        titulo.configure(font="15")
        cpt.ordenar(titulo, 0, 0, 5, 10)

        # ----------- CAJAS TEXTO mUNO-----------

        for i in range(len(lista)):
            self.listaCaja.append(cpt.crear_C(marco_uno, "40"))
            self.listaCaja[i].insert(0, lista[i])
            cpt.ordenar(self.listaCaja[i], i, 0, 5, 5)

        self.mr.obt_lst_cajas = self.listaCaja
        self.listaCaja[0].bind("<Button-1>", self.limpiar)
        self.listaCaja[1].bind("<Button-1>", self.limpiar)
        self.listaCaja[1].bind("<FocusIn>", self.enmascarar)

        # ----------- ETIQUETA mUNO-----------

        crearUs = cpt.crear_E(marco_uno, "Crear nuevo usuario")
        crearUs.configure(foreground="#ff5733", font=("arial", 8, "bold"))
        cpt.ordenar(crearUs, 2, 0, 5, 0, "w")
        crearUs.bind("<Button-1>", self.registrar)

        # ----------- BOTONES mDOS-----------

        for i in range(len(lista2)):
            self.listaBoton.append(cpt.crear_B(marco_dos, lista2[i], "10", comando[i]))
            cpt.ordenar(self.listaBoton[i], 0, i, 5, 5)

    def limpiar(self, event):
        event.widget.delete(0, tk.END)
        return None

    def enmascarar(self, event):
        self.listaCaja[1].delete(0, tk.END)
        self.listaCaja[1].configure(show="*")

    def registrar(self, event):
        self.raiz.iconify()
        return clv.chequear_a(self.listaCaja)

    def chequear(self):
        self.raiz.iconify()
        respuesta = self.mr.comp_us_clv()

        if respuesta is False:
            self.listaCaja[0].delete(0, tk.END)
            self.listaCaja[0].focus()

        return clv.chequear_u(respuesta)

    def cerrar(self):
        quit()