#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class tablaYcontenidos():
    
    def __init__(self, lista_t=[], lista_v=[], condicion=''):
        self.lista_t = lista_t
        self.lista_v = lista_v
        self.lista_v.reverse()
        self.condicion = condicion
        self.campo_id = 0
        self.i = 0 

    def set_i(self, i):
        self.i = i
    
    def get_i(self):
        valor = self.i
        return valor

    # esta func cabia de tablas en el caso de que se tenga mas de una 
    def cambiarTabla(self):
        tabla = self.lista_t[self.get_i()]
        return tabla
    
    # esta func obtiene una lista de campos de una tabla que se suministra sin el campo id
    def obtenerCampos(self):
        tabla = self.cambiarTabla()
        b=Base()
        b.sentencia.execute('SELECT * FROM ' + tabla)
        #lista_c = [ lista[0] for lista in self.sentencia.description if not str(lista[0]).startswith('id_')]
        lista_campo = [ lista[0] for lista in b.sentencia.description ]
        print(lista_campo[0])
        self.campo_id = lista_campo[0]
        lista_c = []
        for i in range(len(lista_campo)):
            if not str(lista_campo[i]).startswith('id_'):
                lista_c.append(lista_campo[i])
        return lista_c

    # esta func hace coincidir los valores ingresados por teclado con los campos de una tabla 
    def igualarCampoValor(self):
        lista_c = self.obtenerCampos()
        lista = []
        lista_seg = []
        y = len(lista_c)
        lista_seg = self.lista_v[:y]
        for x in range(len(lista_seg)):
            x = self.lista_v.pop()
            lista.append(x)
        return lista

    # esta func reemplaza los valores por signos de ? segun se requiere en ciertas sentencias sql
    def reemplazar(self):
        campos = self.obtenerCampos() 
        lista = []
        for c in range(len(campos)):
            if self.condicion == '':
                x = '?'
            else:
                x = c + ' = ' + '?'
            lista.append(x)
        return lista
    pass

class Base():

    def __init__(self, lista_t=[], lista_v=[], condicion=''):
        self.base = 'escuela.db' 
        self.conexion = sqlite3.connect(self.base)
        #self.conexion.row_factory = sqlite3.Row
        self.sentencia = self.conexion.cursor()
        self.lista_t = lista_t
        self.lista_v = lista_v
        self.lista_v.reverse()
        self.condicion = condicion
        #self.campo_id = 0
        self.i = 0 

    def set_i(self, i):
        self.i = i
    
    def get_i(self):
        valor = self.i
        return valor

    # esta func cabia de tablas en el caso de que se tenga mas de una 
    def cambiarTabla(self):
        tabla = self.lista_t[self.get_i()]
        return tabla
    
    # esta func obtiene una lista de campos de una tabla que se suministra sin el campo id
    def obtenerCampos(self):
        tabla = self.cambiarTabla()
        self.sentencia.execute('SELECT * FROM ' + tabla)
        #lista_c = [ lista[0] for lista in self.sentencia.description if not str(lista[0]).startswith('id_')]
        lista_campo = [ lista[0] for lista in self.sentencia.description ]
        lista_c = []
        for i in range(len(lista_campo)):
            if not str(lista_campo[i]).startswith('id_'):
                lista_c.append(lista_campo[i])
        return lista_c

    # esta func hace coincidir los valores ingresados por teclado con los campos de una tabla 
    def igualarCampoValor(self):
        lista_c = self.obtenerCampos()
        lista = []
        lista_seg = []
        y = len(lista_c)
        lista_seg = self.lista_v[:y]
        for x in range(len(lista_seg)):
            x = self.lista_v.pop()
            lista.append(x)
        return lista

    # esta func reemplaza los valores por signos de ? segun se requiere en ciertas sentencias sql
    def reemplazar(self):
        campos = self.obtenerCampos() 
        lista = []
        for c in range(len(campos)):
            if self.condicion == '':
                x = '?'
            else:
                x = c + ' = ' + '?'
            lista.append(x)
        return lista

    # func mostrar, insertar, actualizar, borrar contienen las sentencias basicas de sql
    # a las que se les incluye las tabla y campos correspodientes mediantes func como cambiarTabla 
    # y obtenerCampos
    def mostrar(self):
        campos = ', '.join(self.obtenerCampos())
        if self.condicion == "":
            orden = 'SELECT ' + campos + ' FROM ' + self.cambiarTabla()
        else:
            orden = 'SELECT ' + campos + ' FROM ' + self.cambiarTabla() + ' WHERE ' + self.condicion
        return orden

    def insertar(self):
        campos = ', '.join(self.obtenerCampos()) 
        listado = ', '.join(self.reemplazar()) 
        orden = 'INSERT INTO ' +  self.cambiarTabla() + ' ('+ campos +') VALUES('+ listado +')'
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
        if not self.lista_v == []:
            self.sentencia.execute(orden, self.igualarCampoValor())
            self.conexion.commit()
        else:
            self.sentencia.execute(orden)
            registro = self.sentencia.fetchone() # ver si cada vez que se presiona el boton se reinicia fetchone
            if registro != None:
                print(registro)

        if self.i == len(self.lista_t)-1:
            self.sentencia.close() # no sigue fetchone porque el cursor se cierra
            self.conexion.close()  

        
        
    

    

    