#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
#import componentes as cpt
#import claves as clv
import conexion as con
import re
from datetime import datetime

# MANEJO DE REGISTROS
class Manejo_registros:
    '''Esta clase tiene por objetivo administrar o hace de nexo entre los formularios junto con
    la inofrmacion que se maneja en estos y la propia base de datos por eso se importa conexion'''

    def __init__(self):
        self._listaCaja = []
        self._listaBoton = []
        self._listaBox = []
        self._lista_t = []
        self.lista_v = []
        self.pos = []
        self.lista_f = []
        self.list_aux = []
        self._cond = ''
        self.cant_dos = 0
        self._sel_col = ''
        self._id_cond = ''
        self._activ_personas = ''
        self.dic_spbox = {}
        self._valor_spbox_selec = []
        self._valor_spbox = None
        self.col_spbox = None
        self.col_cond_spbox = None
        self._pos_spbox = None
        self._num_spbox = None
        self._id_m_materiales_spbox = None
        self.accion = con.Consulta()
        self.busq = con.Busquedas()
        self.hab_obt_posicion = True
        self._num_func_reg_gral = None
        self.num_fun_guard = 0

    @property
    def activ_perosnas(self):
        return self._activ_personas

    @activ_perosnas.setter
    def activ_perosnas(self, activ):
        self._activ_personas = activ

    @property
    def id_cond(self):
        return self._id_cond

    @id_cond.setter
    def id_cond(self, valor):
        self._id_cond = valor

    @property
    def obt_cond_sql(self):
        return self._cond

    @obt_cond_sql.setter
    def obt_cond_sql(self, cond):
        self._cond = cond

    @property
    def seleccionar_columnas(self):
        return self._sel_col

    @seleccionar_columnas.setter
    def seleccionar_columnas(self, columnas):
        self._sel_col = columnas

    @property
    def obt_pos_spbox(self):
        return self._pos_spbox

    @obt_pos_spbox.setter
    def obt_pos_spbox(self, valor):
        self._pos_spbox = valor

    @property
    def dar_id_m_materias(self):
        return self._id_m_materiales_spbox

    @dar_id_m_materias.setter
    def dar_id_m_materias(self, valor):
        self._id_m_materiales_spbox = valor

    # SE OBTIENEN LISTAS DE TABLAS, CAJAS DE TEXTO Y BOTONES DE REG DE US Y REG GRAL --------
   
    @property
    def obt_lts_tablas(self):  # ok
        return self._lista_t

    @obt_lts_tablas.setter
    def obt_lts_tablas(self, lista_t):  # ok
        self._lista_t.clear()
        self._lista_t = lista_t

    @property
    def obt_lst_cajas(self):
        return self._listaCaja

    @obt_lst_cajas.setter
    def obt_lst_cajas(self, lista_c):  # ok --> se obtienen e insertan valores mediante este metodo en los dist form
        self._listaCaja = lista_c

        if not self._listaCaja[0].get() == 'USUARIO:':
            self.mostrar_valor_inic()

    @property
    def obt_lst_botones(self):  
        return self._listaBoton

    @obt_lst_botones.setter
    def obt_lst_botones(self, lista_b):  # ok
        self._listaBoton = lista_b

    # SE PASA EL NUMERO DE FUNCION DE REG GRAL PARA OBTENER O NO POSICION DE CAJAS --------

    @property
    def cargar_num_func(self):
        return self._num_func_reg_gral

    @cargar_num_func.setter
    def cargar_num_func(self, num):
        self._num_func_reg_gral = num

    # SE OBTIENEN DATOS PARA LOS LISTBOX --------

    @property
    def obt_lstbox_caja(self):
        return self._listaBox

    @obt_lstbox_caja.setter
    def obt_lstbox_caja(self, caja):
        self._listaBox.append(caja)

    # SE OBTIENEN DATOS PARA LOS SPINBOX --------

    @property
    def mostrar_valor_spbox(self):
        return self._valor_spbox

    @mostrar_valor_spbox.setter
    def mostrar_valor_spbox(self, reg):
        self._valor_spbox = reg

    @property
    def valor_spbox_seleccionado(self):
        return self._valor_spbox_selec

    @valor_spbox_seleccionado.setter
    def valor_spbox_seleccionado(self, valor):
        self._valor_spbox_selec.append(valor)

    # FUNC DE USO COMUN EN DISTINTOS FORMs --------

    def cambiar_a_tab_personas(self):  # ok
        ''' Aqui se acomoda siempre a la tabla personas en 1º lugar para poder facilitar su 
        posterior tratamiento y del resto de la informacion'''

        if self.obt_lts_tablas[0] != 'personas':
            tabla = self.obt_lts_tablas[1]
        else:
            tabla = self.obt_lts_tablas[0]

        return tabla

    # ----------- FUNC PARA AVISO DE EXITO DE OPERACIONES CON BD -----------

    def op_exitosa(self):
        messagebox.showinfo(title="ESTADO", message="Operación exitosa!!!")

    def op_fallida(self):
        messagebox.showinfo(title="ESTADO", message="Operación fallida")

    def respuesta_opracion(self):

        if self.accion.confirmar_cambios == 'ok':
            self.op_exitosa()

            if self.cargar_num_func == 3:
                return

            self.actualizar_id_max_min()
           
        else:
            self.op_fallida()

    # ----------- FUNC PARA FORMATEO DE LISTAS, TABLAS --------------------

    def dar_formato_listado(self, listado):  # ok
        listado_ok = ', '.join(listado)
        return listado_ok

    def dar_formato_tablas(self):  # ok
        listado_ok = ', '.join(self.obt_lts_tablas)
        return listado_ok

    # ----------- FUNC PARA CONDICON WHERE  Y ORDER --------------------

    def cond_where(self, val):
        where = f'WHERE {val}'
        return where

    def cond_order(self, val, sent):
        order = f' ORDER BY {val} {sent} LIMIT 1'
        return order

    # ----------- FUNC PARA CHEQUEO DE DISTINTOS CAMPOS --------------------

    def chequear_dni(self, num_dni):
        patron = r"^\d+$"
        resultado = re.match(patron, num_dni)

        if not resultado or len(num_dni) < 7 or len(num_dni) > 8:
            messagebox.showerror(title="ERROR!", message='El DNI debe tener entre 7 y 8 numeros')

            if self.activ_perosnas == 'preceptor':
                self.obt_lst_cajas[5].focus()
            else:
                self.obt_lst_cajas[2].focus()

            return False
        else:
            return True

    def chequear_mail(self, mail): 
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        resultado = re.match(patron, mail)

        if not resultado:
            messagebox.showerror(title="ERROR!", message='El email esta mal conformado... revise el mismo')
            self.obt_lst_cajas[8].focus()

    def chequear_formateo_fecha(self, fecha): 
        formato = "%d/%m/%Y"

        try:
            datetime.strptime(fecha, formato)
        except ValueError:
            messagebox.showerror(title="ERROR!", message='El formato de fecha de ser el siguiente dd/mm/aaaa')
            self.obt_lst_cajas[6].focus()

    def chequear_cant_registros(self):
        col = 'count(id)'
        tabla_inicial = self.cambiar_a_tab_personas()
        cond = self.cond_where(f'actividad = \'{self.activ_perosnas}\'')
        self.accion.mostrar(col, tabla_inicial, cond, 'one')
        cantidad = self.accion.registro[0]

        return cantidad

    def chequear_cant_registros_por_anio(self, anio):
        col = 'count(curso_division_turno.id_cur)'
        tabla_inicial = 'curso, curso_division_turno'
        cond = self.cond_where(f'curso_division_turno.id_cur = curso.id AND curso.anio = \'{anio}\'')
        self.accion.mostrar(col, tabla_inicial, cond, 'all')
        cantidad = self.accion.registro[0]

        return cantidad[0]

    # ----------- FUNC PARA COMPARAR USUARIO Y CLAVE EN FORM PRINCIPAL --------------------

    def comp_us_clv(self):
        col = 'usuario, clave'
        tabla = 'contraseña'
        usuario = self.obt_lst_cajas[0].get()
        clave = self.obt_lst_cajas[1].get()
        condicion = self.cond_where(f'usuario = \'{usuario}\'')
        self.accion.mostrar(col, tabla, condicion, 'one')
        consulta = self.accion.registro

        if consulta is None:
            return False

        if consulta[0] == usuario and consulta[1] == clave:
            return True

    # ----------- FUNC PARA COMUNES A CAJAS, SPINBOX Y LISTBOX --------------------

    def limpiar_lista(self, reg):

        '''Quita los campos con id a traves de su eliminacion por medio de sus indices en registro'''

        list_ids = self.busq.obt_listado_pos_ids_fkids
        list_reg = list(reg)

        for i in reversed(list_ids):  # utilizo reversed porque si no no me toma bien las posiciones para quitar los ids
            del list_reg[i]

        self.busq.obt_listado_pos_ids_fkids.clear()
        self.lista_f = list_reg

    def obt_nombre_columnas(self, tabla):
        '''Obtener colunmas de una tabla por vez, sin ids ni columna actividad'''

        self.accion.mostrar('*', tabla, '', 'des')
        reg = self.accion.registro

        col_list = [campo[0] for campo in reg if not str(campo[0]).startswith('id') if not campo[0] == 'actividad']
        
        return col_list

    def mostrarValores(self):  # ok

        '''Muestra los valores de las tablas en los formularios'''

        if len(self.lista_f) == len(self.obt_lst_cajas) + 1:
            self.lista_f = list(self.lista_f)
            self.dar_id_m_materias = self.lista_f[0]
            del self.lista_f[0]

        if len(self.lista_f) > len(self.obt_lst_cajas):
            self.limpiar_lista(self.lista_f)

        self.mostrar_reg_spbox(self.lista_f)

        if self.activ_perosnas in self.lista_f:
            self.lista_f.remove(self.activ_perosnas)

        for i in range(len(self.lista_f)):
            self.obt_lst_cajas[i].insert(0, self.lista_f[i])

        self.lista_f = []

    # ESTE BLOQUE MANEJA EL PASO DE LOS REGISTROS EN LOS SPIN-BOX --------------------

    def obtener_lista_spbox(self, campo, tabla):
        self.accion.mostrar(campo, tabla, '', 'all')
        lista = self.accion.registro
        elementos = [item for tupla in lista for item in tupla]
        return elementos

    def obtener_cond_lista_spbox(self):
        campo = self.seleccionar_columnas
        tabla = self.dar_formato_tablas()
        cond = self.cond_where(self.obt_cond_sql)
        self.accion.mostrar(campo, tabla, cond, 'all')
        lista = self.accion.registro
        elementos = [item for tupla in lista for item in tupla]
        return elementos

    def mostrar_lista_spbox(self, num_fun):

        if num_fun == 1:

            if self.obt_pos_spbox == 0:
                campo = 'asignatura'
                tabla = 'materias'
                resultado = self.obtener_lista_spbox(campo, tabla)

                return resultado

        if num_fun == 2:

            if self.obt_pos_spbox == 0:
                campo = 'anio'
                tabla = 'curso'
                resultado = self.obtener_lista_spbox(campo, tabla)

                return resultado

            if self.obt_pos_spbox == 1:
                campo = 'seccion'
                tabla = 'division'
                resultado = self.obtener_lista_spbox(campo, tabla)

                return resultado

            if self.obt_pos_spbox == 2:
                campo = 'mt'
                tabla = 'turno'
                resultado = self.obtener_lista_spbox(campo, tabla)

                return resultado

        if num_fun == 3:

            if self.obt_pos_spbox == 2:
                campo = 'calific'
                tabla = 'notas'
                resultado = self.obtener_lista_spbox(campo, tabla)

                return resultado

    def mostrar_reg_spbox(self, reg):

        if self.activ_perosnas != 'preceptor':

            if self.activ_perosnas == 'profesor':
                self.mostrar_valor_spbox = reg[-1]
                del reg[-1]

            elif self.activ_perosnas == 'alumno' and len(reg) > 3:
                self.mostrar_valor_spbox = reg[-3:]
                del reg[-3:]

    def insertar_valores_spb(self, num):
        self.obt_lstbox_caja[num].delete(0, tk.END)

        if len(self.lista_f) == 0:
            nombre_completo = 'NO HAY REGISTROS PARA ESTE ITEM'
            self.obt_lstbox_caja[num].insert(0, nombre_completo)

        elif num == 0:
            for i in range(len(self.lista_f)):
                self.obt_lstbox_caja[num].insert(0, self.lista_f[i][0])

        else:
            for i in range(len(self.lista_f)):
                nombre_completo = self.lista_f[i][0] + ' ' + self.lista_f[i][1]
                self.obt_lstbox_caja[num].insert(0, nombre_completo)

    # ESTE BLOQUE MANEJA EL PASO DE LOS REGISTROS EN LOS LIST-BOX --------------------

    def mostrar_valores_lbox(self, num_listb):

        if num_listb == 0:
            self.insertar_valores_spb(num_listb)
            return

        if num_listb == 1:
            self.insertar_valores_spb(num_listb)
            return

        if num_listb == 2:
            self.insertar_valores_spb(num_listb)
            return

    def obt_listado_para_lbox(self, num_listb):
        self.lista_f.clear()
        cond = self.cond_where(self.obt_cond_sql)
        tabla = self.dar_formato_tablas()
        col = self.seleccionar_columnas
        self.accion.mostrar(col, tabla, cond, 'all')
        reg = self.accion.registro
        self.lista_f = reg
        self.mostrar_valores_lbox(num_listb)

    # ESTE BLOQUE MANEJA LOS BOTONES PARA EL PASO DE LOS REGISTROS EN EL FORMULARIO (cajas de texto)--------------------

    def obtenerValores(self):
        self.lista_v.clear()

        for i in range(len(self.obt_lst_cajas)):
            self.lista_v.append(self.obt_lst_cajas[i].get())

        return self.lista_v

    def limpiar_casilleros(self):

        for i in range(len(self.obt_lst_cajas)):
            self.obt_lst_cajas[i].delete(0, tk.END)
            if self.obt_lst_cajas[i] != self.obt_lst_cajas[0]:
                self.obt_lst_cajas[i].configure(state='normal')

    def habilitar_desabilitar_btns(self):
        self.obt_lst_botones[0].configure(text='INSERTAR')
        self.obt_lst_botones[0].configure(command=self.insertar_reg)
        self.obt_lst_botones[0].configure(state='normal')
        self.obt_lst_botones[3].configure(state='disable')
        self.obt_lst_botones[4].configure(state='normal')

    def contar_habilitar_sig(self):
        cant_de_regitros = self.chequear_cant_registros()

        if cant_de_regitros == 0:
            self.obt_lst_botones[1].configure(state='disable')
            self.obt_lst_botones[2].configure(state='disable')
            self.obt_lst_botones[4].configure(state='disable')
            
        elif cant_de_regitros <= 1:
            self.obt_lst_botones[2].configure(state='disable')

        else:
            self.obt_lst_botones[2].configure(state='normal')

    def actualizar_id_max_min(self): 
        cond_max_min = self.cond_where(f'actividad = \'{self.activ_perosnas}\'')
        col_inic = 'id'
        tabla_inicial = self.cambiar_a_tab_personas()
        self.busq.id_minimo(col_inic, tabla_inicial, cond_max_min, 'one')  # obtiene id inicial
        self.busq.id_maximo(col_inic, tabla_inicial, cond_max_min, 'one')  # obtiene id final
        
        if self.chequear_cant_registros() >= 1:
            self.obt_lst_botones[0].configure(text='INSERTAR')
            self.obt_lst_botones[0].configure(command=self.insertar_reg)
            self.obt_lst_botones[0].configure(state='normal')

        self.contar_habilitar_sig()

    def cargar_valor_inic(self):
        tabla = self.dar_formato_tablas()
        col = self.seleccionar_columnas
        condicion = self.cond_where(self.obt_cond_sql)
        self.actualizar_id_max_min()
        self.limpiar_casilleros()

        if col == '*':
            self.busq.obt_indice_columnas(self.obt_lts_tablas)       # se obtiene el indice de las col para luego borar los ids

        self.busq.registro_inic(col, tabla, condicion, 'one')

    def mostrar_valor_inic(self):  # ok
        self.cargar_valor_inic()
        reg = self.busq.registro

        if reg is None:                                                     # en caso de que no haya mas registros
            messagebox.showinfo(title="ATENCION!", message="No se encuentran registros en la base")
            self.insertar_reg()
            return

        self.lista_f = reg
        self.mostrarValores()
        self.contar_habilitar_sig()
        self.obt_lst_botones[0].configure(text='INSERTAR')
        self.obt_lst_botones[0].configure(command=self.insertar_reg)
        self.obt_lst_botones[0].configure(state='normal')
        self.obt_lst_botones[1].configure(state='disabled')
        self.obt_lst_botones[3].configure(state='disabled')
        self.obt_lst_botones[4].configure(state='normal')

    def mostrarSiguiente(self):  # ok
        self.hab_obt_posicion = True
        tabla = self.dar_formato_tablas()
        col = self.seleccionar_columnas
        tabla_inicial = self.cambiar_a_tab_personas()
        siguiente = f' AND {tabla_inicial}.id > {str(con.Busquedas.index)}' + self.cond_order(f'{self.id_cond}', 'ASC')
        cond = self.cond_where(self.obt_cond_sql)
        cond_compuesta = cond + siguiente
        self.obt_lst_botones[1].configure(state='normal')
        self.limpiar_casilleros()

        if col == '*':
            self.busq.obt_indice_columnas(self.obt_lts_tablas)  # llamada p/obtener nombre de columnas si se necesitan todas

        self.busq.registro_sig(col, tabla, cond_compuesta, 'one')

        if self.busq.registro is None:
            self.cargar_valor_inic()

        reg = self.busq.registro
        self.lista_f = reg
        self.habilitar_desabilitar_btns()
        self.mostrarValores()

    def mostarPrevio(self):  # ok
        self.hab_obt_posicion = True
        tabla = self.dar_formato_tablas()
        col = self.seleccionar_columnas
        tabla_inicial = self.cambiar_a_tab_personas()
        previo = f' AND {tabla_inicial}.id < {str(con.Busquedas.index)}' + self.cond_order(f'{self.id_cond}', 'DESC')
        cond = self.cond_where(self.obt_cond_sql)
        cond_comp = cond + previo
        self.obt_lst_botones[2].configure(state='normal')
        self.limpiar_casilleros()

        if col == '*':
            self.busq.obt_indice_columnas(self.obt_lts_tablas)

        self.busq.registro_previo(col, tabla, cond_comp, 'one')

        if self.busq.registro is None:
            previo = f' AND {tabla_inicial}.id <= {str(self.busq.id_max)}' + self.cond_order(f'{self.id_cond}', 'DESC')
            cond = self.cond_where(self.obt_cond_sql)
            cond_comp = cond + previo
            self.busq.registro_previo(col, tabla, cond_comp, 'one')

        reg = self.busq.registro
        self.lista_f = reg
        self.habilitar_desabilitar_btns()
        self.mostrarValores()

    # ESTE BLOQUE MANEJA BOTONES DE EDICION, BORRADO E INSERCION EN EL FORMULARIO --------------------

    # este grupo de metodos son comunes a guardar y editar -------------------------------------------

    def chaquear_nomb_tab_union(self, cadena):
        '''Comprueba que sean tablas de union'''

        patron = r"^[a-z]+\_"
        resultado = re.match(patron, cadena)

        return resultado

    def obt_2da_col_y_tab(self, i):
        '''obtiene el --> nombre de las tablas <-- materias, notas, curso,
        division y turno... junto con el --> nombre de sus segundas columnas <--'''

        tabla = self.obt_lts_tablas[i]

        if tabla:

            if tabla == 'materias' or tabla == 'notas':
                self.dic_spbox[tabla] = self.accion.registro[1][0]

            if tabla == 'curso' or tabla == 'division' or tabla == 'turno':
                self.dic_spbox[tabla] = self.accion.registro[1][0]

    def obt_num_id_tab_union(self, tabla, col_cond, valor):
        condicion = f'WHERE {col_cond} = \'{valor}\''
        self.accion.mostrar('id', tabla, condicion, 'one')
        id_col_ref = self.accion.registro

        return id_col_ref

    def listar_ids_tab_union(self):
        lista = [self.accion.registro[i][0] for i in range(len(self.accion.registro)) if
                 self.accion.registro[i][0] != self.accion.registro[0][0]]
        return lista

    # ------------------------- Conjunto de Metodos que operan con el btn guardar ------------------------------------

    def insertar_reg(self):  # ok
        self.hab_obt_posicion = False
        self.limpiar_casilleros()
        self.obt_lst_cajas[0].focus()
        self.obt_lst_botones[0].configure(text='GUARDAR')
        self.obt_lst_botones[0].configure(state='disable')
        self.obt_lst_botones[0].configure(command=self.guardar)
        self.obt_lst_botones[3].configure(state='disable')
        self.obt_lst_botones[4].configure(state='disable')

    def activar_guardar(self):  # ok
        self.obt_lst_botones[0].configure(state='normal')
        if self.cant_dos:
            self.cant_dos = 0

    def igualar_columna_valor(self, cant):  # ok

        '''Se utiliza con la instruccion insert de la funcion guardar.
        Dado que se trabaja con el valor cantidad que representa el nº de columnas por cada tabla que compone la
        lista self.obt_lts_tablas esta cantidad marca en primer lugar hasta donde se llegan a tomar elementos de la lista
        self.lista_v (mediante slice), luego el contenido de la variable cant pasa a la auxiliar self.cant_dos y se
        retornan la cantidad exacta de valores que se corresponde con las columnas de la tabla que se esta tratando,
        luego se vuelve a llamar a esta func tantas veces como tablas contenga la lista self.lista_v pero esta vez
        self.cant_dos ya no vale cero y se obtendran los valores de la diferencia entre self.cant_dos y cant'''

        if self.cant_dos != 0:
            valores = self.lista_v[self.cant_dos:self.cant_dos + cant]
            self.cant_dos = self.cant_dos + cant
            return valores
        else:
            valores = self.lista_v[:cant]
            self.cant_dos = cant
            return valores

    # ultimo_id, obt_valor_fkey e insertar_calves_foraneas
    # USADOS PARA EDITAR LAS TABLA DE UNION, SOLO CAJAS DE TEXTO, NO SPINBOX ---------------------------

    def ultimo_id(self, tabla):
        col = 'id'
        self.busq.id_maximo(col, tabla, '', 'one')
        ult_id = con.Busquedas.id_max
        return ult_id

    def obt_valor_fkey(self, tabla, persona_id, lista_fkeys, i):
        valor_id_fkey = []
        if lista_fkeys[i].startswith('id_'):

            if tabla == 'localidad':
                listado = f' {lista_fkeys[i]} = ?'
                valor_id_ba = self.ultimo_id('barrio')
                valor_id = self.ultimo_id('localidad')
                cond = self.cond_where(f'{tabla}.{self.accion.registro[0][0]} = {valor_id}')
                valor_id_fkey.append(valor_id_ba)
            else:
                listado = f' {lista_fkeys[i]} = ?'                              # obt nombre de columna fkey--> "id_per"
                cond = self.cond_where(f'{tabla}.{self.accion.registro[0][0]} = {self.ultimo_id(tabla)}')
                valor_id_fkey.append(persona_id)
        else:
            listado = None
            cond = None
            valor_id_fkey = None

        return listado, cond, valor_id_fkey

    def insertar_calves_foraneas(self, lista_tablas, persona_id, lista_fkeys):

        for i in range(len(lista_tablas)):
            listado, cond, valor_id_fkey = self.obt_valor_fkey(lista_tablas[i], persona_id, lista_fkeys, i)

            if listado is not None and cond is not None and valor_id_fkey is not None:
                self.accion.actualizar(lista_tablas[i], listado, cond, valor_id_fkey)

    # CODIGO PARA GUARDAR CAMPO DE TABLA POR MEDIO DE SPBOX ----------------------------------
    
    def guardar_valor_spbox(self, id_persona):
        i = 0
        id_union = []

        for clave, valor in self.dic_spbox.items():
            segunda_col = valor
            tabla = clave
            numero = self.obt_num_id_tab_union(tabla, segunda_col, self.valor_spbox_seleccionado[i])
            id_union.append(numero[0])
            i += 1

        id_union.append(id_persona)

        if len(id_union) != len(self.col_spbox):
            del self.col_spbox[1]

        lista_signos = ['?' for c in range(len(self.col_spbox))]
        lista_signos_ok = self.dar_formato_listado(lista_signos)
        lista_col_ok = self.dar_formato_listado(self.col_spbox)
        self.accion.insertar(self.obt_lts_tablas[-1], lista_col_ok, lista_signos_ok, id_union)
        self.dic_spbox.clear()
        self.col_spbox.clear()
        self.valor_spbox_seleccionado.clear()

    def obt_col_tab_union_guardar(self):
        '''obtiene el --> nombre de las columnas <-- de la tablas de UNION'''

        self.col_spbox = self.listar_ids_tab_union()

    def insertar_mostrarMaterias_spbox(self, valor_nota, columnas):
        col = columnas
        list_col = f'{col[0]}, {col[1]}, {col[2]}'
        list_sig = f'?, ?, ?'
        cond = self.cond_where(self.obt_cond_sql)
        self.accion.mostrar(col[3], self.obt_lts_tablas[1], cond, 'one')
        valor_mat = self.accion.registro[0]
        valor_per = self.dar_id_m_materias
        valores = [valor_mat, valor_nota, valor_per]
        self.accion.insertar(self.obt_lts_tablas[0], list_col, list_sig, valores)
        self.respuesta_opracion()

    def guardar(self):  # ok
        acum = 0
        lista_fkeys = []
        lista_tab_tex = []
        self.hab_obt_posicion = True
        self.obtenerValores()                                       # lista de valores obtenidos del fromulario

        for i in range(len(self.obt_lts_tablas)):                          # por cada tabla en la lista hacer....
            lista_col = self.obt_nombre_columnas(self.obt_lts_tablas[i])   # obtener lista con nomb de columnas
            cant = len(lista_col)                                   # se obtiene la cantidad
            acum += cant
            valores = self.igualar_columna_valor(cant)              # se obtienen valores a insertar por cada tabla

            lista_signos = ['?' for c in range(cant)]               # se obtiene lista de '?' segun cantidad de columnas

            if self.obt_lts_tablas[i] == 'personas':                       # solo si es la tabla personas se agrega su actividad
                valor_actividad = self.activ_perosnas
                valores.append(valor_actividad)
                lista_col.append('actividad')
                lista_signos.append('?')

            if acum <= len(self.obt_lst_cajas):
                lista_signos_ok = self.dar_formato_listado(lista_signos)  # se da formato a los listados
                lista_col_ok = self.dar_formato_listado(lista_col)
                self.accion.insertar(self.obt_lts_tablas[i], lista_col_ok, lista_signos_ok, valores)  # ejecucion de sent insert
                lista_fkeys.append(self.accion.registro[-1][0])  # ver si toma actividad con preceptores
                lista_tab_tex.append(self.obt_lts_tablas[i])
            else:
                self.obt_2da_col_y_tab(i)

                if self.chaquear_nomb_tab_union(self.obt_lts_tablas[i]):
                    self.obt_col_tab_union_guardar()

        # SEGUNDO PASO... ACTUALIZACION DE FKEYS PARA LOGRAR RELACION ENTRE LAS DISTINTAS TABLAS

        persona_id = self.ultimo_id('personas')
        self.insertar_calves_foraneas(lista_tab_tex, persona_id, lista_fkeys)

        # TERCER PASO... ALMACENADO DE FKEYS PARA LOGRAR RELACION ENTRE LAS DISTINTAS TABLAS, EN TABLAS DE UNION
        print(persona_id)
        if self.dic_spbox is not None and self.col_spbox is not None:   # dic(tabla:col) --- col[col-tabla-union]
            self.guardar_valor_spbox(persona_id)

        self.lista_v.clear()
        self.respuesta_opracion()

    # ------------------------- Conjunto de Metodos que operan con el btn editar ------------------------------------

    def obtenerPosicion(self, event):  # ok

        '''Se obtiene una lista con las posiciones de los entrys en los formularios'''

        if self.activ_perosnas is None:
            return

        if self.cargar_num_func == 3:
            return

        if not self.hab_obt_posicion:
            return

        pos = str(event.widget.focus_get())

        if pos == '.!toplevel.!frame3.!entry':
            return

        self.obt_lst_botones[3].configure(state='normal')
        event.widget.delete(0, tk.END)

        for i in range(len(self.obt_lst_cajas)):
            caja = str(self.obt_lst_cajas[i])

            if caja == pos:
                indice = self.obt_lst_cajas.index(self.obt_lst_cajas[i])
        
        indice = indice + 1
        self.pos.append(indice)

        if self.pos.count(indice) > 1:                  # verifica que no se almacene dos veces el mismo valor
            self.pos.remove(indice)

        self.pos.sort()

    def obt_valores_editados(self, indice):  # ok
        valor = self.obt_lst_cajas[indice].get()
        self.lista_v.append(valor)

    def obtener_campos_editados(self, aux, cant_camp, lista_camp, ind, col_nomb):  # ok
        '''Aqui se obtiene la posicion(q da el valor) y el indice(q da el campo) a editar dentro de las cajas de texto del form'''

        posicion = self.pos

        for i in range(len(posicion)):

            if posicion[i] <= aux:

                if ind != 0: # ind es indice de tabla no tiene que ver con la posicion o el i del for
                    pos_a_editar = posicion[i] - 1
                    dif_aux_cant_camp = aux - cant_camp
                    indice = pos_a_editar - dif_aux_cant_camp
                    self.obt_valores_editados(pos_a_editar)

                else:
                    indice = posicion[i] - 1
                    self.obt_valores_editados(indice)
               
                col_nomb.append(f'{lista_camp[indice]} = ?')
                self.list_aux.append(posicion[i]) # ---> ok

        for i in range(len(self.list_aux)):
            self.pos.remove(self.list_aux[i])

        self.list_aux.clear()

    def obt_fkey_localidad(self, tabla, col_cond):
        indice = self.busq.index
        self.accion.mostrar('id', tabla, 'WHERE id_per = ' + str(indice), 'one')
        numero_fkey_dos = self.accion.registro[0]
        condicion = self.cond_where(f'{col_cond} = {numero_fkey_dos}')

        return condicion

    # CODIGO PARA EDITAR CAMPO DE TABLA POR MEDIO DE SPBOX ----------------------------------

    def comparar_valor_spbox(self):
        valor = self.valor_spbox_seleccionado

        if self.mostrar_valor_spbox != valor and valor is not None:
            return True
        else:
            return False

    def editar_valor_spbox(self):
        col_nom = []
        id_union = []
        i = 0
        cont = 0

        for clave, valor in self.dic_spbox.items():
            segunda_col = valor
            tabla = clave
            numero = self.obt_num_id_tab_union(tabla, segunda_col, self.valor_spbox_seleccionado[i])
            print(numero[0])
            id_union.append(numero[0])
            cont += 1
            col_nom.append(f'{self.col_spbox[cont - 1]} = ?')
            i += 1

        condicion = self.nun_id_personas_selec(self.col_cond_spbox)
        campo_nom_format = self.dar_formato_listado(col_nom)
        self.accion.actualizar(self.obt_lts_tablas[-1], campo_nom_format, condicion, id_union)
        self.dic_spbox.clear()
        self.col_spbox.clear()
        self.valor_spbox_seleccionado.clear()
        self.col_cond_spbox = None

    def obt_col_tab_union_editar(self):
        '''obtiene el --> nombre de las columnas <-- de la tablas de UNION'''

        self.col_spbox = self.listar_ids_tab_union()

        if not self.col_cond_spbox:
            self.col_cond_spbox = self.col_spbox[-1]
            del self.col_spbox[-1]

    def nun_id_personas_selec(self, col_cond):
        '''obtiene --> numero id <-- de la tabla personas porque esto se
        usa en la mayoria de las tablas para relacionarlas'''

        numero_id = self.busq.index
        condicion = self.cond_where(f'{col_cond} = {numero_id}')

        return condicion

    def editar_mostrarMaterias_spbox(self, valor_nota, columnas):
        col = columnas
        col_signo= f'{col[0]} = ?'
        cond_sel = self.cond_where(self.obt_cond_sql)
        self.accion.mostrar(col[1], self.obt_lts_tablas[1], cond_sel, 'one')
        valor_id_mat = self.accion.registro[0]
        valor_per = self.dar_id_m_materias
        cond_up = self.cond_where(f'mat_nota.id_per = \'{valor_per}\' AND mat_nota.id_mat = \'{valor_id_mat}\'')
        valor = [valor_nota]
        self.accion.actualizar(self.obt_lts_tablas[0], col_signo, cond_up, valor)
        self.respuesta_opracion()

    def editar(self):  # ok
        acum = 0
        col_nom = []

        for i in range(len(self.obt_lts_tablas)):
            lista_col = self.obt_nombre_columnas(self.obt_lts_tablas[i])

            if self.comparar_valor_spbox():
                self.obt_2da_col_y_tab(i)

                if self.chaquear_nomb_tab_union(self.obt_lts_tablas[i]):
                    self.obt_col_tab_union_editar()
                    self.editar_valor_spbox()

            cant_camp = len(lista_col)
            acum += cant_camp
            self.obtener_campos_editados(acum, cant_camp, lista_col, i, col_nom)  # llena la lista de col_nom

            if col_nom and self.lista_v:

                if self.obt_lts_tablas[i] == 'personas':
                    col_cond = self.accion.registro[0][0]               # obtiene nomb de col --> 'id'
                else:
                    col_cond = self.accion.registro[-1][0]              # obtiene nomb de col --> 'id_' que son f kyes

                if self.obt_lts_tablas[i] == 'localidad':
                    tabla = self.obt_lts_tablas[i - 1]
                    condicion = self.obt_fkey_localidad(tabla, col_cond)
                else:
                    condicion = self.nun_id_personas_selec(col_cond)

                lista_valores_format = self.lista_v
                campo_nom_format = self.dar_formato_listado(col_nom)
            
                self.accion.actualizar(self.obt_lts_tablas[i], campo_nom_format, condicion, lista_valores_format)

            col_nom.clear()
            self.lista_v.clear()

        self.respuesta_opracion()

        self.obt_lst_botones[3].configure(state='disable')

    def borrar(self):
        self.hab_obt_posicion = True
        confirmar = messagebox.askokcancel(title="CUIDADO!!!", message="Esta por borrar el registro completo de esta persona... desea continuar?")

        if confirmar is False:
            return

        tabla_inicial = self.cambiar_a_tab_personas()
        condicion = "id = ?"
        valor = self.busq.index
        self.accion.borrar(tabla_inicial, condicion, valor)

        for i in range(len(self.obt_lst_cajas)):
            self.obt_lst_cajas[i].delete(0, tk.END)

        self.respuesta_opracion()
        
    def borrar_rel_mat_nota(self):
        tabla = 'mat_nota'
        condicion = 'id_per = ?'
        valor = self.busq.index
        self.accion.borrar(tabla, condicion, valor)

    # ----------- FUNC BUSCAR DNI-----------

    def buscar(self, valor):  
        tablas = self.dar_formato_tablas()
        condicion = self.cond_where(f'dni = {valor}')
        col = 'id'
        self.accion.mostrar(col, self.obt_lts_tablas[1], condicion, 'one')

        try:
            id_reg = self.accion.registro[0]
        except TypeError as e:
            messagebox.showerror(title="ERROR!", message="No se encontro este DNI en la base de datos")
            return

        self.limpiar_casilleros()
        cond = self.cond_where(f'{self.obt_cond_sql} AND personas.id = {id_reg}')
        self.accion.mostrar('*', tablas, cond, 'one')
        self.lista_f = self.accion.registro
        self.busq.obt_indice_columnas(self.obt_lts_tablas)
        self.mostrarValores()
