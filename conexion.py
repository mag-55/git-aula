#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import sqlite3

class Base():

    def __init__(self):
        self.base = 'escuela.db' 
        self.conexion = sqlite3.connect(self.base)
        self.sentencia = self.conexion.cursor()
        

class Datos():
    
    def __init__(self, lista_t=[], lista_v=[]):

        self.lista_t = lista_t
        self.lista_v = lista_v
        self.list_rev = self.lista_v[:]
        self.list_rev.reverse()
        self.lista = False
        if not self.lista_v == []:
            self.lista = True
        self.id = ""
        self.tabla = ""
        self.longitud = 0
        self.i = 0 
        self.posicion = []
        self.repetir = True

    def set_i(self, i): #ok
        self.i = i
    
    def get_i(self): #ok
        valor = self.i
        return valor

    def set_posicion(self, indice): #ok
        self.posicion = indice

    def copiar_posicion(self):
        pos = self.posicion[:]
        return pos

    # esta func cabia de tablas en el caso de que se tenga mas de una 
    def cambiarTabla(self): #ok
        self.tabla = self.lista_t[self.get_i()]
        return self.tabla
    
    # esta func obtiene una lista de campos de una tabla que se suministra sin el campo id
    def obtenerCampos(self): #ok

        tabla = self.cambiarTabla()
        b = Base()
        b.sentencia.execute('SELECT * FROM ' + tabla)
        lista = b.sentencia.description

        lista_campo = [item[0] for item in lista if not str(item[0]).startswith('id')]
        
        return lista_campo

    # esta func hace coincidir los valores ingresados por teclado con los campos de una tabla 
    def igualarCampoValor(self): 

        lista_cv = []
        lista_c = self.obtenerCampos()
        longitud = len(lista_c)
        lista_seg = self.list_rev[ :longitud]

        for x in range(len(lista_seg)):

            x = self.list_rev.pop()
            lista_cv.append(x)

        return lista_cv

    def ubicarCampo(self):

        campos = self.obtenerCampos()
        lista = []
        posicion = self.posicion 
        ubicacion = self.copiar_posicion()
        catidad = len(campos) 
        self.longitud = self.longitud + catidad

        for i in range(len(posicion)):

            if int(ubicacion[i]) <= self.longitud: 

                if self.i != 0:
                    x = posicion[i] - 1
                    y = self.longitud -  catidad
                    indice = x - y

                else:
                    indice = posicion[i] - 1

                for i in range(len(campos)):
                    if campos.index(campos[i]) == indice:
                        lista.append(campos[i])

        return lista

    def listarUbicacion(self):
        lista = self.ubicarCampo()

        while lista == []:
            acu =+ 1
            self.i = self.i + acu
            lista = self.ubicarCampo()

        return lista
            
    def ubicarValor(self):

        lista_U = []
        contenido = self.lista_v
        
        for i in range(len(contenido)):
            indice = self.posicion[i] - 1

            if indice > self.longitud:
                x = self.lista_v.index(self.lista_v[i]) - 1
                self.lista_v.pop(x)
                y = self.posicion.index(self.posicion[i]) - 1
                self.posicion.pop(y)
                break
            
            lista_U.append(contenido[i])

        if len(self.lista_v) == 0:
            self.repetir = False
        
        return lista_U
        
    # esta func reemplaza los valores por signos de ? segun se requiere en ciertas sentencias sql
    def reemplazarI(self): #ok

        campos = self.obtenerCampos()
        lista = []

        for c in range(len(campos)):

            x = '?'
            lista.append(x)           
        
        return lista

    def reemplazarU(self): #ok

        listado = self.listarUbicacion()
        lista_r = []

        for c in range(len(listado)):
            x = listado[c] + ' = ?'
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
        listado = ', '.join(self.dato.reemplazarI()) 

        orden = 'INSERT INTO ' +  tabla + ' ('+ campos +') VALUES('+ listado +')'

        return orden

    def actualizar(self): #ok

        listado = ', '.join(self.dato.reemplazarU())
        tabla = self.dato.cambiarTabla()
        
        orden = 'UPDATE ' + tabla + ' SET ' + listado + ' WHERE ' + self.condicion

        return orden

    def borrar(self): #ok

        tabla = self.dato.cambiarTabla()

        orden = 'DELETE FROM ' + tabla + ' WHERE ' + self.condicion

        return orden

    # aqui discrimina entre la lista de valores vacia o no, segun sea para agragar datos 
    # o para extraerlos con una u otra sentencia, es decir esta funcion esta dedicada a 
    # la EJECUCION de sentencias
    def ejecutar(self, orden):
        
        lista = self.dato.lista
        sentencia = self.base.sentencia
        conexion = self.base.conexion
        
        # si la lista contiene elementos (Update, Insert) realiza la primera acción
        if lista:

            if orden.startswith('INSERT'):

                listaCV = tuple(self.dato.igualarCampoValor())
                sentencia.execute(orden, listaCV)

            else:

                listaUV = tuple(self.dato.ubicarValor())
                sentencia.execute(orden, listaUV) 
                
        else:

            sentencia.execute(orden) 
            registro = sentencia.fetchone() 
            return registro
        
        conexion.commit()

        if self.dato.i == len(self.dato.lista_t)-1: 
            sentencia.close() 
            conexion.close()  




        
        
    

    

    