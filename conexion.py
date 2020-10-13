#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from tkinter import messagebox


class Base:

    def __init__(self):
        try:
            self.base = 'escuela.db'
            self.conexion = sqlite3.connect(self.base)
        except sqlite3.OperationalError as e:
            messagebox.showerror(title="ERROR!", message=e)


class Datos:

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
        self.repetido = 0

    def set_i(self, i):  # ok
        self.i = i

    def get_i(self):  # ok
        valor = self.i
        return valor

    def set_posicion(self, indice):  # ok
        self.posicion = indice

    def copiar_posicion(self):
        pos = self.posicion[:]
        return pos

    # esta func cabia de tablas en el caso de que se tenga mas de una 
    def cambiarTabla(self):  # ok
        self.tabla = self.lista_t[self.get_i()]
        return self.tabla

    # esta func obtiene una lista de campos de una tabla que se suministra sin el campo id
    def obtenerCampos(self):  # ok

        tabla = self.cambiarTabla()
        b = Base()
        sentencia = b.conexion.cursor()
        lista = sentencia.execute('SELECT * FROM ' + tabla).description
        lista_campo = [item[0] for item in lista if not str(item[0]).startswith('id')]

        return lista_campo

    # esta func hace coincidir los valores ingresados por teclado con los campos de una tabla 
    def igualarCampoValor(self):

        lista_cv = []
        lista_c = self.obtenerCampos()
        longitud = len(lista_c)
        lista_seg = self.list_rev[:longitud]

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
                    y = self.longitud - catidad
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
            acu = + 1
            self.i = self.i + acu
            lista = self.ubicarCampo()

        return lista

    def ubicarValor(self):

        lista_U = []
        longitud_P = len(self.copiar_posicion())
        contenido = self.lista_v

        for i in range(len(contenido)):
            indice = self.posicion[i] - 1

            if indice >= self.longitud:

                for i in range(len(lista_U)):
                    x = self.lista_v.index(self.lista_v[i]) - i
                    self.lista_v.pop(x)
                    y = self.posicion.index(self.posicion[i]) - i
                    self.posicion.pop(y)

                break

            lista_U.append(contenido[i])

        longitud_U = len(lista_U)

        if longitud_U == longitud_P:
            self.posicion = []

        return lista_U

    # esta func reemplaza los valores por signos de ? segun se requiere en ciertas sentencias sql
    def reemplazarI(self):  # ok

        campos = self.obtenerCampos()
        lista = []

        for c in range(len(campos)):
            x = '?'
            lista.append(x)

        return lista

    def reemplazarU(self):  # ok

        listado = self.listarUbicacion()
        lista_r = []

        for c in range(len(listado)):
            x = listado[c] + ' = ?'
            lista_r.append(x)

        return lista_r

    def comp_us_clv(self, usuario, clave):
        db = Base()
        consulta = 'SELECT id FROM preceptores WHERE usuario = ?'
        sentencia = db.conexion.cursor()
        sentencia.execute(consulta, (usuario,))
        id = sentencia.fetchone()
        if id:
            consulta1 = 'SELECT usuario, clave FROM preceptores WHERE id = ?'
            sentencia.execute(consulta1, (id[0],))
            valores_us = sentencia.fetchone()

            if valores_us[0] == usuario and valores_us[1] == clave:
                return True
        else:
            return False

    def contar_filas(self, tabla):
        db = Base()
        consulta = 'SELECT id FROM ' + tabla
        sentencia = db.conexion.cursor()
        sentencia.execute(consulta)
        cantidad = (len(sentencia.fetchall()))
        return cantidad


class Consultas:

    def __init__(self, datos, condicion=''):
        self.base = Base()
        self.dato = datos
        self.condicion = condicion

    # func mostrar, insertar, actualizar, borrar contienen las sentencias basicas de sql
    # a las que se les incluye las tabla y campos correspodientes mediantes func como cambiarTabla 
    # y obtenerCampos
    def mostrar(self):  # ok

        tabla = self.dato.cambiarTabla()
        campos = ', '.join(self.dato.obtenerCampos())

        if self.condicion == "":
            orden = 'SELECT ' + campos + ' FROM ' + tabla
        else:
            orden = 'SELECT ' + campos + ' FROM ' + tabla + ' WHERE ' + self.condicion

        return orden

    def insertar(self):  # ok

        tabla = self.dato.cambiarTabla()
        campos = ', '.join(self.dato.obtenerCampos())
        listado = ', '.join(self.dato.reemplazarI())

        orden = 'INSERT INTO ' + tabla + ' (' + campos + ') VALUES(' + listado + ')'

        return orden

    def actualizar(self):  # ok

        listado = ', '.join(self.dato.reemplazarU())
        tabla = self.dato.cambiarTabla()

        orden = 'UPDATE ' + tabla + ' SET ' + listado + ' WHERE ' + self.condicion

        return orden

    def borrar(self):  # ok

        tabla = self.dato.cambiarTabla()

        orden = 'DELETE FROM ' + tabla + ' WHERE ' + self.condicion

        return orden

    def buscar_id(self, tabla, condicion, valor):
        orden = 'SELECT id FROM ' + tabla + ' WHERE ' + condicion + '=' + valor
        campo_id = self.ejecutar(orden)
        return campo_id

    # aqui discrimina entre la lista de valores vacia o no, segun sea para agragar datos 
    # o para extraerlos con una u otra sentencia, es decir esta funcion esta dedicada a 
    # la EJECUCION de sentencias
    def ejecutar(self, orden):
        try:
            lista = self.dato.lista
            sentencia = self.base.conexion.cursor()
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
                if orden.startswith('SELECT'):
                    registro = sentencia.fetchone()
                    return registro

            conexion.commit()

        except sqlite3.ProgrammingError as e:
            messagebox.showerror(title="ERROR!", message=e)
            conexion.rollback()

        except sqlite3.OperationalError as e:
            messagebox.showerror(title="ERROR!", message=e)
            conexion.rollback()

        except sqlite3.DataError as e:
            messagebox.showerror(title="ERROR!", message=e)
            conexion.rollback()

        finally:
            if self.dato.i == len(self.dato.lista_t) - 1:
                sentencia.close()
                conexion.close()
