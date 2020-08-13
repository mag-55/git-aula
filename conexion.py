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
        self.i = 0 
        self.posicion = []

    def set_i(self, i): #ok
        self.i = i
    
    def get_i(self): #ok
        valor = self.i
        return valor

    def set_posicion(self, indice): #ok
        self.posicion = indice
        print("clase datos", self.posicion)

    def get_posicion(self): 
        valor = self.posicion
        return valor
         
    # esta func cabia de tablas en el caso de que se tenga mas de una 
    def cambiarTabla(self): #ok
        self.tabla = self.lista_t[self.get_i()]
        return self.tabla
    
    # esta func obtiene una lista de campos de una tabla que se suministra sin el campo id
    def obtenerCampos(self): #ok
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
        longitud = len(lista_c)
        lista_seg = self.lista_v[:longitud]

        for x in range(len(lista_seg)):
            x = self.lista_v.pop()
            lista_cv.append(x)

        return lista_cv

    def ubicarCampo(self, campos):

        lista = []
        lista_c =  campos #tengo la lista de campos por tabla
        posicion = self.posicion #tengo la lista de posiciones
        print("la posicion ", posicion)

        for i in range(len(posicion)):
            indice = posicion[i]
            for i in range(len(lista_c)):
                if lista_c.index(lista_c[i]) == indice:
                    lista.append(lista_c[i])
                # else:
                #     return
                #     como vuelvo a buscar la siguiente tabla?
                #     como guardo la tabla segun los campos
        print("datos lista", lista)
        return lista

    def ubicarValor(self):

        lista = []
        posicion = self.posicion
        contenido = self.lista_v

        for i in range(len(posicion)):
            indice = posicion[i]
            lista.append(contenido[indice])
        
        return lista
        
    # esta func reemplaza los valores por signos de ? segun se requiere en ciertas sentencias sql
    def reemplazarI(self): #ok

        campos = self.obtenerCampos()
        lista = []

        for c in range(len(campos)):
            x = '?'
            lista.append(x)           
        
        return lista

    def reemplazarU(self):

        campos = self.obtenerCampos()
        listado = self.ubicarCampo(campos)
        lista = []

        for c in range(len(listado)):
            campo = lista[c]
            x = campo + ' = ?'
            lista.append(x)
        
        return lista
        
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
        listado = ', '.join(self.dato.reemplazarI()) 

        orden = 'INSERT INTO ' +  tabla + ' ('+ campos +') VALUES('+ listado +')'

        return orden

    def actualizar(self):

        tabla = self.dato.cambiarTabla()
        listado = ', '.join(self.dato.reemplazarU())
        
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
        listaUV = tuple(self.dato.ubicarValor())
        sentencia = self.base.sentencia
        conexion = self.base.conexion
        
        # si la lista contiene elementos (Update, Insert) realiza la primera acción
        if lista:

            print(orden)
            print(listaCV)

            if orden.startswith('INSERT'):
                sentencia.execute(orden, listaCV)
            else:
                sentencia.execute(orden, listaUV) #poner 2do parametro para cambiar campo

            conexion.commit()
        else:

            sentencia.execute(orden) 
            registro = sentencia.fetchone() 

            if registro != None:
                return registro

        if self.dato.i == len(self.dato.lista_t)-1:
             
            sentencia.close() 
            conexion.close()  

        
        
    

    

    