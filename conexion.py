#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class Base():

     def __init__(self):
        self.base = 'escuela.db' 
        self.conexion = sqlite3.connect(self.base)
        self.sentencia = self.conexion.cursor()
        

class Datos():
    
    def __init__(self, lista_t=[], lista_v=[]):# aca no va condicion, van en consultas
        self.lista_t = lista_t
        self.lista_v = lista_v
        self.lista_v.reverse()
        self.lista = False
        if not self.lista_v == []:
            self.lista = True
        self.id = ""
        self.tabla = ""
        self.lista_c = []
        #self.lista_cv = []
        #self.lista_r = []
        self.i = 0 
        self.posicion = 0

    def set_i(self, i):
        self.i = i
    
    def get_i(self):
        valor = self.i
        return valor

    def set_posicion(self, pos):
        self.posicion = pos

    # def get_posicion(self):
    #     return self.posicion

    # esta func cabia de tablas en el caso de que se tenga mas de una 
    def cambiarTabla(self):
        self.tabla = self.lista_t[self.get_i()]
        return self.tabla
    
    # esta func obtiene una lista de campos de una tabla que se suministra sin el campo id
    def obtenerCampos(self):
        tabla = self.tabla
        b = Base()
        b.sentencia.execute('SELECT * FROM ' + tabla)
        lista = b.sentencia.description
        lista_campo = [item[0] for item in lista if not str(item[0]).startswith('id')]
        return lista_campo

    # esta func hace coincidir los valores ingresados por teclado con los campos de una tabla 
    def igualarCampoValor(self): #ok

        lista_c = self.obtenerCampos()
        lista_cv = []
        lista_seg = []
        y = len(lista_c)
        lista_seg = self.lista_v[:y]

        for x in range(len(lista_seg)):
            x = self.lista_v.pop()
            lista_cv.append(x)
        return lista_cv

    def ubicarCampo(self, campos):

        lista_c =  campos #tengo la lista de campos por tabla
        longitud = len(lista_c) #tengo la longitud
        #esto nos da la tabla en la cual trabajar
        for i in range(len(self.lista_t)):
            if longitud < self.posicion:
                self.set_i(i)
                ubicacion = longitud - self.posicion
                self.posicion = ubicacion
            else:
                for i in range(len(lista_c)):
                    #esto me da la posicion dentro de la tabla 
                    posicionC = lista_c.index(lista_c[i])
                    if self.posicion == posicionC:
                        return lista_c[i] #retorna el campo

    # esta func reemplaza los valores por signos de ? segun se requiere en ciertas sentencias sql
    def reemplazar(self, insert='True'):

        campos = self.obtenerCampos()
        lista_r = []

        if insert:
            for c in range(len(campos)):
                x = '?'
                lista_r.append(x)
        else:
            c = self.ubicarCampo(campos)
            x = c + ' = ' + '?'
            lista_r.append(x)
            
        return lista_r


class Consultas():

    def __init__(self, datos, condicion=''):
        self.base = Base()
        self.dato = datos
        self.condicion = condicion
         
    # func mostrar, insertar, actualizar, borrar contienen las sentencias basicas de sql
    # a las que se les incluye las tabla y campos correspodientes mediantes func como cambiarTabla 
    # y obtenerCampos
    def mostrar(self): #ok

        tabla = self.dato.cambiarTabla()
        campos = ', '.join(self.dato.obtenerCampos())

        if self.condicion == "":
            orden = 'SELECT ' + campos + ' FROM ' + tabla
        else:
            orden = 'SELECT ' + campos + ' FROM ' + tabla + ' WHERE ' + self.condicion
        return orden

    def insertar(self): #ok

        tabla = self.dato.cambiarTabla()
        campos = ', '.join(self.dato.obtenerCampos()) 
        listado = ', '.join(self.dato.reemplazar()) 

        orden = 'INSERT INTO ' +  tabla + ' ('+ campos +') VALUES('+ listado +')'
        return orden

    def actualizar(self):

        listado = ', '.join(self.dato.reemplazar(insert='False'))
        tabla = self.dato.cambiarTabla()

        orden = 'UPDATE ' + tabla + ' SET ' + listado + ' WHERE ' + self.condicion
        return orden

    def borrar(self):

        tabla = self.dato.cambiarTabla()

        orden = 'DELETE FROM ' + tabla + ' WHERE ' + self.condicion
        return orden

    # aqui discrimina entre la lista de valores vacia o no, segun sea para agragar datos 
    # o para extraerlos con una u otra sentencia, es decir esta funcion esta dedicada a 
    # la EJECUCION de sentencias
    def ejecutar(self, orden):
        
        lista = self.dato.lista
        listaCV = tuple(self.dato.igualarCampoValor())
        sentencia = self.base.sentencia
        conexion = self.base.conexion
        
        # si la lista contiene elementos (Update, Insert) realiza la primera acción
        if lista:
            print(orden)
            print(listaCV)
            sentencia.execute(orden, listaCV)
            sentencia
            conexion.commit()
        else:
            print(orden)
            sentencia.execute(orden)
            registro = sentencia.fetchone() 
            if registro != None:
                print(registro)

        if self.dato.i == len(self.dato.lista_t)-1:
            sentencia.close() 
            conexion.close()  

        
        
    

    

    