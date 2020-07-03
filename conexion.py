#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class Base():
     def __init__(self):
        self.base = 'escuela.db' 
        self.conexion = sqlite3.connect(self.base)
        self.sentencia = self.conexion.cursor()
        

class Datos():
    
    def __init__(self, lista_t=[], lista_v=[], condicion=''):
        self.lista_t = lista_t
        self.lista_v = lista_v
        self.lista_v.reverse()
        self.condicion = condicion
        self.tabla = ""
        self.lista_c = []
        self.lista_cv = []
        self.lista_r = []
        self.i = 0 

    def set_i(self, i):
        self.i = i
    
    def get_i(self):
        valor = self.i
        return valor

    # esta func cabia de tablas en el caso de que se tenga mas de una 
    def cambiarTabla(self):
        self.tabla = self.lista_t[self.get_i()]
        return self.tabla
    
    # esta func obtiene una lista de campos de una tabla que se suministra sin el campo id
    def obtenerCampos(self):
        tabla = self.cambiarTabla()
        b = Base()
        b.sentencia.execute('SELECT * FROM ' + tabla)
        lista_campo = [lista[0] for lista in b.sentencia.description]
        for i in range(len(lista_campo)):
            if not str(lista_campo[i]).startswith('id_'):
                self.lista_c.append(lista_campo[i])
        return self.lista_c

    # esta func hace coincidir los valores ingresados por teclado con los campos de una tabla 
    def igualarCampoValor(self):
        lista_c = self.lista_c
        lista_seg = []
        y = len(lista_c)
        lista_seg = self.lista_v[:y]
        for x in range(len(lista_seg)):
            x = self.lista_v.pop()
            self.lista_cv.append(x)
        return self.lista_cv

    # esta func reemplaza los valores por signos de ? segun se requiere en ciertas sentencias sql
    def reemplazar(self):
        campos = self.lista_c
        for c in range(len(campos)):
            if self.condicion == '':
                x = '?'
            else:
                x = c + ' = ' + '?'
            self.lista_r.append(x)
        return self.lista_r
    

class Tablas():
    def __init__(self):
        self.base = Base()
        # self.dato = Datos() #problema toma los datos vacios ya a la clase Datos y esta los reinicia  
    # func mostrar, insertar, actualizar, borrar contienen las sentencias basicas de sql
    # a las que se les incluye las tabla y campos correspodientes mediantes func como cambiarTabla 
    # y obtenerCampos
    def mostrar(self):
        campos = ', '.join(self.dato.lista_c)
        tabla = self.dato.tabla 
        condicion = self.dato.condicion
        if self.dato.condicion == "":
            orden = 'SELECT ' + campos + ' FROM ' + tabla
        else:
            orden = 'SELECT ' + campos + ' FROM ' + tabla + ' WHERE ' + condicion
        return orden

    def insertar(self):
        tabla = Datos.cambiarTabla()
        campos = ', '.join(self.dato.lista_c) 
        listado = ', '.join(self.dato.lista_r) 
        orden = 'INSERT INTO ' +  tabla + ' ('+ campos +') VALUES('+ listado +')'
        return orden

    def actualizar(self):
        listado = ', '.join(self.reemplazar())
        orden = 'UPDATE ' + self.cambiarTabla() + ' SET ' + listado + ' WHERE ' + self.condicion
        return orden

    def borrar(self):
        orden = 'DELETE FROM ' + self.cambiarTabla() + ' WHERE ' + self.condicion
        return orden

    # aqui discrimina entre la lista de valores vacia o no, segun sea para agragar datos 
    # o para extraerlos con una u otra sentencia, es decir esta funcion esta dedicada a 
    # la EJECUCION de sentencias
    def ejecutar(self, orden):

        listaV = self.dato.lista_v
        listaCV = self.dato.lista_cv
        sentencia = self.base.sentencia
        conexion = self.base.conexion

        if not listaV == []:
            sentencia.execute(orden, listaCV)
            conexion.commit()
        else:
            sentencia.execute(orden)
            registro = sentencia.fetchone() # ver si cada vez que se presiona el boton se reinicia fetchone
            if registro != None:
                print(registro)

        if self.dato.i == len(self.dato.lista_t)-1:
            sentencia.close() # no sigue fetchone porque el cursor se cierra
            conexion.close()  

        
        
    

    

    