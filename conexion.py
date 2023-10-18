#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from tkinter import messagebox

def ejec_mostrar(func):  # mostrar

    def inner(self, *args, **kwargs):
        try:
            conexion = sqlite3.connect('bd/escuela_ok.db')
            conexion.execute("PRAGMA foreign_keys = ON")
            cursor = conexion.cursor()
            sentencia, clave = func(self, *args, **kwargs)
            cursor.execute(sentencia)

            if clave == 'one':
                self._registro = cursor.fetchone()

            elif clave == 'many':
                self._registro = cursor.fetchmany()

            elif clave == 'all':
                self._registro = cursor.fetchall()

            else:
                self._registro = cursor.description

        except sqlite3.OperationalError as e:
            messagebox.showerror(title="ERROR!", message=e)

        else:
            cursor.close()
            conexion.close()

    return inner


def ejecutar(func):

    def inner(self, *args, **kwargs):

        try:
            conexion = sqlite3.connect('bd/escuela_ok.db')
            conexion.execute("PRAGMA foreign_keys = ON")
            cursor = conexion.cursor()
            sentencia, valor = func(self, *args, **kwargs)
            cursor.execute(sentencia, valor)

        except sqlite3.OperationalError as e:
            messagebox.showerror(title="ERROR!", message=e)
            conexion.rollback() 
            
        else:
            
            if conexion.total_changes > 0:
                self.confirmar_cambios = 'ok'

            conexion.commit()
            cursor.close()
            conexion.close()

    return inner


class Consulta:
    '''esta clase agrupa metodos por los que se llevan a cabo operaciones basicas sobre las
    tablas de la base consultas, actualizaciones, inserciones, etc mas la ejecucion de las
    mismas por medio de un metodo en comun, hereda de la clase Base'''

    def __init__(self):
        self._registro = None
        self._confirmacion = None

    @property
    def registro(self):
        return self._registro

    @registro.setter
    def registro(self, valor):
        self._registro = valor

    @property
    def confirmar_cambios(self):
        return self._confirmacion

    @confirmar_cambios.setter
    def confirmar_cambios(self, valor):
        self._confirmacion = valor

    @ejec_mostrar
    def mostrar(self, columnas='', tabla='', condicion='', clave=''):

        if condicion:
            orden = f'SELECT {columnas} FROM {tabla} {condicion}'
        else:
            orden = f'SELECT {columnas} FROM {tabla}'

        return orden, clave
            
    @ejecutar
    def insertar(self, tabla='', columnas='', listado='', contenido=''):  # OK!!!
        orden = f"INSERT INTO {tabla}({columnas}) VALUES({listado})"
        return orden, contenido

    @ejecutar
    def actualizar(self, tabla='', listado='', condicion='', contenido=''):  # OK!!!
        orden = f'UPDATE {tabla} SET {listado} {condicion}'
        return orden, contenido  

    @ejecutar
    def borrar(self, tabla='', condicion='', valor=''):  # OK!!!
        id_valor = (valor, ) 
        orden = f'DELETE FROM {tabla} WHERE {condicion}'
        return orden, id_valor

class Busquedas(Consulta):
    '''
    en esta clase se trata de realizar solo las busquedas correspondiente
    a los botones siguiente, anterior o algun campo puntual
    trabaja con las funcion decorada mostrar de la clase heredada Consulta
    que a su vez esta decorada por ejec_mostrar, todo en este mismo modulo
    '''

    index = 0  # VARIABLE de clase para retener el valor, si estuviese en __init__ se resetearia
    num = 0
    id_min = 0
    id_max = 0

    def __init__(self):
        super().__init__()
        self._ids = None
        self._posicion_ids = None
        self._posicion_fkids = None
        self._nomb_col = None

    @property
    def obt_listado_pos_ids_fkids(self):
        return self._ids

    @obt_listado_pos_ids_fkids.setter
    def obt_listado_pos_ids_fkids(self, valor):
        self._ids = valor

    @property
    def obt_posicion_ids(self):
        return self._posicion_ids

    @obt_posicion_ids.setter
    def obt_posicion_ids(self, lista):

        self._posicion_ids = [indice for indice in range(len(lista)) if not lista[indice].startswith('id_') and lista[indice].startswith('id')]

    @property
    def obt_posicion_fkids(self):
        return self._posicion_fkids

    @obt_posicion_fkids.setter
    def obt_posicion_fkids(self, lista):

        self._posicion_fkids = [indice for indice in range(len(lista)) if lista[indice].startswith('id_')]

    def obt_indice_columnas(self, tabla):                           # obt nombre col, tan si es una o varias tabla
        list_col_comp = []

        if type(tabla) != list:
            self.mostrar('*', tabla, '', 'des')
            reg = self.registro

            col_list = [campo[0] for campo in reg if campo is not None]

            list_col_comp.extend(col_list)

        else:

            for i in range(len(tabla)):
                self.mostrar('*', tabla[i], '', 'des')
                reg = self.registro

                col_list = [campo[0] for campo in reg if campo is not None]

                list_col_comp.extend(col_list)

        self.obt_posicion_ids = list_col_comp
        self.obt_posicion_fkids = list_col_comp
        list_ids = self.obt_posicion_ids[:]
        list_ids.extend(self.obt_posicion_fkids)
        list_ids.sort()
        self.obt_listado_pos_ids_fkids = list_ids

    def registro_inic(self, col, tabla, cond, clave):
        self.mostrar(col, tabla, cond, clave)
        self.id_registro()

    def registro_sig(self, col, tabla, cond, clave):
        Busquedas.num = 1
        self.mostrar(col, tabla, cond, clave)
        self.id_registro()

    def registro_previo(self, col, tabla, cond, clave):
        Busquedas.num = 2
        self.mostrar(col, tabla, cond, clave)
        self.id_registro()

    def id_registro(self):

        '''extrae el id registro, chequea que no sea None y almacena el valor en var de clase index'''

        TOTAL_COL_PRECEPTOR = 21

        if self.registro is not None:

            if len(self.registro) == TOTAL_COL_PRECEPTOR:
                Busquedas.index = self.registro[5]
                
            else:
                Busquedas.index = self.registro[0]

    def id_minimo(self, col, tabla, cond, clave):
        col_min = f'min({col})'
        self.mostrar(col_min, tabla, cond, clave)
        mini = list(self.registro)
        Busquedas.id_min = mini[0]

    def id_maximo(self, col, tabla, cond, clave):
        col_max = f'max({col})'
        self.mostrar(col_max, tabla, cond, clave)
        maxi = list(self.registro)
        Busquedas.id_max = maxi[0]
