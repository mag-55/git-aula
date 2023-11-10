#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import componentes as cpt
import re
import claves as clv
from formularios import Manejo_registros

# FORMULARIO DE REGISTRO DE NUEVO USUARIO
class RegistroUsuario:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("REGISTRO DE USUARIOS")
        self.listaEtiqueta = []
        self.listaCaja = []
        self.listaBoton = []
        self.caja_buscar = None
        self.mr = Manejo_registros()
        tablas = ['contraseña', 'personas', 'barrio', 'localidad']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = 'personas.id = contraseña.id_per AND personas.id = barrio.id_per AND barrio.id = ' \
                               'localidad.id_ba AND personas.actividad = \'preceptor\''
        self.mr.seleccionar_columnas = '*'
        self.mr.id_cond = 'id'
        self.mr.activ_perosnas = 'preceptor'

    # ----------- VENTANA REGISTRO DE USUARIO -----------

    def registrarUs(self):

        # ----------- LISTAS NOMB ETIQ, NOMB BOTONES, LLAMADAS A FUNC-----------

        lista = ("USUARIO", "CLAVE", "CONF CLAVE", "NOMBRE", "APELLIDO", "DNI", "FECHA", "TEL", "MAIL", "CALLE", "BARRIO", "LOCALIDAD", "CP")
        lista2 = ("INSERTAR", "PREVIO", "SIGUIENTE", "EDITAR", "BORRAR", "SALIR")
        comando = [self.insert_reg, self.most_prev, self.most_sig, self.editar, self.borrar, self.salirFormulario]

        # ----------- MARCO UNO, DOS Y BUSCAR-----------

        marco_uno = cpt.crear_M(self.ventana, "500",  "400")
        cpt.ordenar(marco_uno, 0, 0)
        
        marco_dos = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(marco_dos, 2, 0)

        marco_buscar = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(marco_buscar, 1, 0)

        # ----------- ETIQUETAS marcoUNO-----------

        for i in range(len(lista)):
            self.listaEtiqueta.append(cpt.crear_E(marco_uno, lista[i]))
            cpt.ordenar(self.listaEtiqueta[i], i, 0, 5, 5)

        # ----------- BOTONES marcoDOS-----------

        for i in range(len(lista2)):
            self.listaBoton.append(cpt.crear_B(marco_dos, lista2[i], "9", comando[i]))
            cpt.ordenar(self.listaBoton[i], 0, i, 1, 5)

        self.listaBoton[1].configure(state='disabled')
        self.listaBoton[3].configure(state='disabled')

        self.mr.obt_lst_botones = self.listaBoton

        cant_de_regitros = self.mr.chequear_cant_registros()

        if cant_de_regitros <= 1:
            self.listaBoton[2].configure(state='disable')

        # ----------- BOTON maroBuscar-----------

        boton_buscar = cpt.crear_B(marco_buscar, "Buscar", "9", self.buscar)
        cpt.ordenar(boton_buscar, 0, 2, 1, 1)

        # ----------- CAJA-BUSCAR mmarcoBUSCAR-----------

        self.caja_buscar = cpt.crear_C(marco_buscar, "20")
        self.caja_buscar.insert(0, "Ingrese DNI:")
        self.caja_buscar.configure(foreground="gray")
        cpt.ordenar(self.caja_buscar, 0, 1, 1, 1)
        self.caja_buscar.bind("<FocusIn>", self.limpiar)
        self.caja_buscar.bind("<FocusOut>", self.limpiar)

        # ----------- CAJAS marcoUNO-----------

        for i in range(len(lista)):
            self.listaCaja.append(cpt.crear_C(marco_uno, "50"))
            
            if self.listaCaja[i] != self.listaCaja[0]:
                self.listaCaja[i].configure(state='disabled')
            cpt.ordenar(self.listaCaja[i], i, 1, 5, 5)

        self.mr.obt_lst_cajas = self.listaCaja

        # ----------- ENLACES PARA LAS FUNC-----------

        self.enlazar_dos_eventos(self.listaCaja[0], self.validarU)
        self.enlazar_dos_eventos(self.listaCaja[1], self.validarC)
        self.enlazar_dos_eventos(self.listaCaja[2], self.chequear_Cl1_Cl2)
        self.enlazar_dos_eventos(self.listaCaja[5], self.func_cheq_guard)

        self.listaCaja[6].bind("<Return>", self.cheq_fecha)
        self.listaCaja[8].bind("<Return>", self.cheq_mail)
        self.listaCaja[i].bind_class("Entry", "<Double-Button-1>", self.ob_pos)

    def enlazar_dos_eventos(self, caja_text, func_val):
        caja_text.bind("<Return>", func_val)
        caja_text.bind("<Tab>", func_val)

    # ----------- FUNC SALIDA DEL FORMULARIO-----------

    def salirFormulario (self):  
        self.mr.activ_perosnas = None
        self.ventana.destroy()

    # ----------- FUNC LIMPIAR CAJA BUSCAR-----------

    def limpiar(self, event):
        event.widget.delete(0, tk.END)

    # ----------- FUNC VALIDA USUARIO Y CLAVE(tabién verifica us != cl y cl == ccl)-----------

    def validarU(self, event):
        return clv.validarUsuario(self.listaCaja)

    def validarC(self, event):
        return clv.validarClave(self.listaCaja)

    def chequear_Cl1_Cl2(self, event):
        return clv.compararClaves(self.listaCaja)
    
    # ----------- FUNC GUARDAR, EDITAR, BORRAR, BUSCAR-----------

    def ob_pos(self, event):
        self.mr.obtenerPosicion(event=event)

    def most_sig(self):
        self.mr.mostrarSiguiente()

    def most_prev(self):
        self.mr.mostarPrevio()

    def insert_reg(self):
        self.mr.insertar_reg()

    def guardar(self):
        self.mr.activar_guardar()

    def editar(self):
        self.mr.editar()

    def borrar(self):
        self.mr.borrar()

    def buscar(self):
        valor = self.caja_buscar.get()

        patron = r"^\d+$"
        resultado = re.match(patron, valor)

        if resultado:
            self.mr.buscar(valor)

        else:
            messagebox.showerror(title="ERROR!", message="Ingrese DNI por favor")
            self.caja_buscar.focus()
            return
    
    # ----------- FUNC PARA CHEQUEO -----------------------------

    def cheq_dni(self, num):
        self.mr.chequear_dni(num) 
    
    def func_cheq_guard(self, event):

        if self.listaCaja[3].get() == '' or self.listaCaja[4].get() == '':
            messagebox.showerror(title="ERROR!", message='Nombre y Apellido deben ser ingresados')
            self.listaCaja[3].focus()
            return

        num = event.widget.get()
        self.cheq_dni(num)
        self.guardar()

    def cheq_fecha(self, event):
        fecha = event.widget.get()
        self.mr.chequear_formateo_fecha(fecha)

    def cheq_mail(self, event):
        mail = event.widget.get()
        self.mr.chequear_mail(mail)