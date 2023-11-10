#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import componentes as cpt
from formularios import Manejo_registros

# FORMULARIO DE INGRESO DE DATOS
class RegistroGral:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("BIENVENIDO AL AULA")
        self.mr = Manejo_registros()
        self.listaBoton = []
        self.lista_c_ed = []
        self.list_spin = None
        self.marcoSpin = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(self.marcoSpin, 0, 0)
        self.marco_prof = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marco_prof)
        self.marco_alum = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marco_alum)
        self.marco_mat = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marco_mat)
        self.marco_curso = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marco_curso)
        self.marcoBoton = cpt.crear_M(self.ventana, "500", "15")
        cpt.ordenar(self.marcoBoton, 2, 0)
        self.caja_buscar = None
        self.spin1_prof = None
        self.cant = 0
        self.valor_selec_spbox = None
        self.dni_ok = False
        self.spin_X = None
        self.num_func = 0
        self.comp_num_func = 0
        self.pos_spbox = None
        self.comp_num_spb = None
        self.conjunto_spb = []
        self.list_valor_spb = []
        self.actual = 1
        self.cantidad_reg = 0
        self.paso = True
        self.id_alumno = None
        self.cur_origen = None

    # ----------- VENTANA REGISTRO DE GRAL -----------

    def registrarGral(self):
        lista = ("SELECCIONE UNA OPCION", "PROFESORES", "ALUMNOS", "MATERIAS", "CURSOS")
        lista2 = ("INSERTAR", "PREVIO", "SIGUIENTE", "EDITAR", "BORRAR", "SALIR")

        # ----------- MARCO Y LISTA SPIN-----------

        seleccion = self.ventana.register(self.capturar)
        self.list_spin = cpt.crear_Sp(self.marcoSpin, lista, "80", "normal", "center", comando=seleccion)
        cpt.ordenar(self.list_spin, 0, 0, 5, 5, "N")
        self.list_spin['state'] = 'readonly' 
        self.list_spin['foreground'] = 'black'

        # ----------- MARCO Y LISTA DE BOTONES-----------

        for i in range(len(lista2)):
            self.listaBoton.append(cpt.crear_B(self.marcoBoton, lista2[i], "10"))
            cpt.ordenar(self.listaBoton[i], 0, i, 0, 5)

        self.mr.obt_lst_botones = self.listaBoton
        self.conf_btns_princ()

    # ----------- FUNC MOSTRAR, OCULTAR Y CAPTURAR MARCOS-----------

    def ocultar(self, marco):
        marco.grid_forget()

    def mostar(self, marco):
        cpt.ordenar(marco, 1, 0)

    def capturar(self):
        captura = self.list_spin.get()

        if captura == "PROFESORES":
            self.ocultar(self.marco_alum)
            self.mostrarProfesor()
            self.mostar(self.marco_prof)
            self.conf_btns()

        elif captura == "ALUMNOS":
            self.ocultar(self.marco_prof)
            self.ocultar(self.marco_mat)
            self.mostrarAlumnos()
            self.mostar(self.marco_alum)
            self.conf_btns()

        elif captura == "MATERIAS":
            self.ocultar(self.marco_alum)
            self.ocultar(self.marco_curso)
            self.mostrarMaterias()
            self.mostar(self.marco_mat)
            self.conf_btns_materias()

        elif captura == "CURSOS":
            self.ocultar(self.marco_mat)
            self.mostrarCursos()
            self.mostar(self.marco_curso)
            self.conf_btns_princ()

        else:
            self.ocultar(self.marco_prof)
            self.conf_btns_princ()

    # ----------- FUNC SETEO DE BTNs-----------

    def conf_btns_princ(self):

        for i in range(len(self.listaBoton) - 1):
            self.listaBoton[i].configure(state='disable')

        self.listaBoton[-1].configure(command=self.salirFormulario)

    def editar_cajas_spb(self):
        self.recorrer_spboxs_editar()
        self.editar()

    def conf_btns(self):
        cant_de_regitros = self.mr.chequear_cant_registros()

        if cant_de_regitros == 0:
            self.conf_btns_princ()

        elif cant_de_regitros == 1:
            self.listaBoton[0].configure(text='INSERTAR')
            self.listaBoton[0].configure(state='normal')
            self.listaBoton[0].configure(command=self.insert_reg)
            self.listaBoton[2].configure(state='disable')
            self.listaBoton[2].configure(command=self.most_sig)
            self.listaBoton[3].configure(command=self.editar_cajas_spb)
            self.listaBoton[4].configure(state='normal')
            self.listaBoton[4].configure(command=self.borrar)

        else:
            
            for i in range(len(self.listaBoton)):

                if i != 1 and i != 3:
                    self.listaBoton[i].configure(state='normal')

            self.listaBoton[0].configure(text='INSERTAR')
            self.listaBoton[0].configure(command=self.insert_reg)
            self.listaBoton[1].configure(command=self.most_prev)
            self.listaBoton[2].configure(command=self.most_sig)
            self.listaBoton[3].configure(command=self.editar_cajas_spb)
            self.listaBoton[4].configure(command=self.borrar)

    def reasignar_func_editar_insertar_spb(self):
        self.listaBoton[0].configure(command=self.cond_insertar_mostrarMaterias_spbox)
        self.listaBoton[3].configure(command=self.cond_editar_mostrarMaterias_spbox)

    def reconf_btns_ed_inst(self):

        if self.spin_X['value'] != 0:
            self.listaBoton[0].configure(state='disable')
            self.listaBoton[3].configure(state='normal')

        else:
            self.listaBoton[0].configure(state='normal')
            self.listaBoton[3].configure(state='disable')

    def conf_btns_materias(self):
        self.listaBoton[4].configure(state='disable')

        if self.cantidad_reg == 0:
            self.conf_btns_princ()

        elif self.cantidad_reg == 1:
            self.listaBoton[2].configure(state='disable')
            self.reconf_btns_ed_inst()
            self.reasignar_func_editar_insertar_spb()

        else:
            self.reconf_btns_ed_inst()
            self.reasignar_func_editar_insertar_spb()

    # ----------- FUNC SETEO DE CAJAS TEXTO-----------

    def enlazar_dos_eventos(self, caja_text, func_val):
        caja_text.bind("<Return>", func_val)
        caja_text.bind("<Tab>", func_val)

    def conf_cajas_text(self, listaCaja):
        self.enlazar_dos_eventos(listaCaja[0], self.cheq_contenido)
        self.enlazar_dos_eventos(listaCaja[1], self.cheq_contenido)
        self.enlazar_dos_eventos(listaCaja[2], self.cheq_dni)
        listaCaja[3].bind("<Return>", self.cheq_fecha)
        listaCaja[5].bind("<Return>", self.cheq_mail)

    # ----------- FUNC SETEO DE SPINBOXs-----------

    def definir_spboxs(self, marco, elemento, fila_num, col, ancho):
        self.valor_selec_spbox = tk.StringVar()
        self.spin_X = cpt.crear_Sp(marco, elemento, ancho, "readonly", "center", self.valor_selec_spbox)
        cpt.ordenar(self.spin_X, fila_num, col, 5, 5)
        self.spin_X['foreground'] = 'black'
        self.spin_X['wrap'] = True
        self.conjunto_spb.append(self.spin_X)

    # ----------- FUNC MARCOS CON SUS ETIQUETAS Y CAJAS-----------

    def mostrarProfesor(self):

        if self.comp_num_func != self.num_func:
            self.comp_num_func = 0

        self.num_func = 1
        self.mr.cargar_num_func = self.num_func
        listaCaja = []
        listaEtiqueta = []
        lista = ("NOMBRE", "APELLIDO", "DNI", "FECHA", "TEL", "MAIL", "CALLE", "BARRIO", "LOCALIDAD", "CP")
        tablas = ['personas', 'barrio', 'localidad', 'materias', 'mat_nota']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = 'personas.id = barrio.id_per AND barrio.id = localidad.id_ba ' \
                               'AND personas.id = mat_nota.id_per AND mat_nota.id_mat = materias.id ' \
                               'AND personas.actividad =\'profesor\''
        self.mr.seleccionar_columnas = '*'
        self.mr.id_cond = 'id'
        self.mr.activ_perosnas = 'profesor'

        # ----------- ETIQUETAS mDOS-----------

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marco_prof, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        # ----------- CAJAS mDOS-----------

        for i in range(len(lista)):
            listaCaja.append(cpt.crear_C(self.marco_prof, "70"))
            cpt.ordenar(listaCaja[i], i, 1, 5, 5)

        self.mr.obt_lst_cajas = listaCaja
        self.conf_cajas_text(listaCaja)

        listaCaja[2].bind("<FocusOut>", self.activar)
        listaCaja[i].bind_class("Entry", "<Double-Button-1>", self.ob_pos)

        # ----------- SPINBOX mDOS-----------
        self.conjunto_spb.clear()

        etiqueta_curso = cpt.crear_E(self.marco_prof, "ASIGNATURA")
        cpt.ordenar(etiqueta_curso, 11, 0, 5, 5)

        elemento = [self.mr.mostrar_valor_spbox]
        marco = self.marco_prof
        self.definir_spboxs(marco, elemento, 11, 1, "65")
        self.cant = 0
        self.spin_X.bind('<Button-1>', lambda event, spbox=self.spin_X: self.ob_pos_spbox(event, spbox))
        self.spin_X['command'] = self.cambiar_valores

        self.listaBoton[0].bind('<Button-1>', self.recorrer_spboxs_gaurdar)

    def mostrarAlumnos(self):

        if self.comp_num_func != self.num_func:
            self.comp_num_func = 0

        self.num_func = 2
        self.mr.cargar_num_func = self.num_func
        listaCaja = []
        listaEtiqueta = []
        lista = ("NOMBRE", "APELLIDO", "DNI", "FECHA", "TEL-CONT", "MAIL-CONT", "CALLE", "BARRIO", "LOCALIDAD", "CP")
        tablas = ['personas', 'barrio', 'localidad', 'curso', 'division', 'turno', 'curso_division_turno']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = 'personas.id = barrio.id_per AND barrio.id = localidad.id_ba ' \
                               'AND personas.id = curso_division_turno.id_per ' \
                               'AND division.id = curso_division_turno.id_div ' \
                               'AND curso.id = curso_division_turno.id_cur ' \
                               'AND turno.id = curso_division_turno.id_tur AND personas.actividad = \'alumno\''
        self.mr.seleccionar_columnas = '*'
        self.mr.id_cond = 'id'
        self.mr.activ_perosnas = 'alumno'

        # ----------- ETIQUETAS mTRES-----------

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marco_alum, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        # ----------- CAJAS mTRES-----------

        for i in range(len(lista)):
            listaCaja.append(cpt.crear_C(self.marco_alum, "70"))
            cpt.ordenar(listaCaja[i], i, 1, 5, 5)

        self.mr.obt_lst_cajas = listaCaja
        self.conf_cajas_text(listaCaja)

        listaCaja[2].bind("<FocusOut>", self.activar)
        listaCaja[i].bind_class("Entry", "<Double-Button-1>", self.ob_pos)

        # ----------- MARCO GRUPO PARA SPINBOXs-----------

        marco_grupo = cpt.crear_M(self.marco_alum, "500", "50")
        cpt.ordenar(marco_grupo, 13, 1)

        # ----------- ETIQUETAS y SPINBOXs-----------
        self.conjunto_spb.clear()

        etiqueta_curso = cpt.crear_E(marco_grupo, "CURSO")
        cpt.ordenar(etiqueta_curso, 0, 0, 5, 5)

        elemento = self.mr.mostrar_valor_spbox[0]
        self.cur_origen = elemento
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 0, 1, "15")
        self.cant = 0
        self.spin_X.bind('<Button-1>', lambda event, spbox=self.spin_X: self.ob_pos_spbox(event, spbox))
        self.spin_X['command'] = self.cambiar_valores

        etiqueta_curso = cpt.crear_E(marco_grupo, "DIVISION")
        cpt.ordenar(etiqueta_curso, 0, 2, 5, 5)

        elemento = self.mr.mostrar_valor_spbox[1]
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 0, 3, "2")
        self.cant = 0
        self.spin_X.bind('<Button-1>', lambda event, spbox=self.spin_X: self.ob_pos_spbox(event, spbox))
        self.spin_X['command'] = self.cambiar_valores

        etiqueta_curso = cpt.crear_E(marco_grupo, "TURNO")
        cpt.ordenar(etiqueta_curso, 0, 4, 5, 5)

        elemento = self.mr.mostrar_valor_spbox[2]
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 0, 5, "10")
        self.cant = 0
        self.spin_X.bind('<Button-1>', lambda event, spbox=self.spin_X: self.ob_pos_spbox(event, spbox))
        self.spin_X['command'] = self.cambiar_valores

        self.listaBoton[0].bind('<Button-1>', self.recorrer_spboxs_gaurdar)

    def mostrarMaterias(self):
        self.num_func = 3
        self.mr.cargar_num_func = self.num_func

        # ----------- MARCO GRUPO PARA SPINBOXs-----------

        marco_grupo = cpt.crear_M(self.marco_mat, "500", "50")
        cpt.ordenar(marco_grupo, 6, 1)

        marco_texto = cpt.crear_M(self.marco_mat, "500", "50")
        cpt.ordenar(marco_texto, 7, 1)

        # ----------- ETIQUETAS y SPINBOXs-----------
        self.conjunto_spb.clear()
        self.list_valor_spb.clear()

        etiqueta_aclaracion = cpt.crear_E(marco_grupo, "CURSO")
        cpt.ordenar(etiqueta_aclaracion, 0, 0, 5, 5)

        elemento = self.mr.obtener_lista_spbox('anio', 'curso')
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 1, 0, "15")
        self.list_valor_spb.append(self.spin_X.get())
        valor_spbox1 = self.list_valor_spb[0]

        self.spin_X.bind('<Button-1>', lambda event, spbox=self.spin_X: self.obt_foco_spbox(event, spbox))
        self.spin_X.bind('<Return>', lambda event, valor=self.spin_X: self.actualizacion_combinada(event, valor))
        self.cantidad_reg = self.mr.chequear_cant_registros_por_anio(valor_spbox1)

        # ---------------------------------------------------

        etiqueta_aclaracion = cpt.crear_E(marco_grupo, "MATERIA")
        cpt.ordenar(etiqueta_aclaracion, 0, 1, 5, 5)

        self.obt_cond_sql_spbox_mat(valor_spbox1)
        elemento = self.mr.obtener_cond_lista_spbox()
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 1, 1, "35")
        self.list_valor_spb.append(self.spin_X.get())
        valor_spbox2 = self.list_valor_spb[1]

        self.spin_X.bind('<Button-1>', lambda event, spbox=self.spin_X: self.obt_foco_spbox(event, spbox))
        self.spin_X.bind('<Return>', lambda event: self.llamar_act_spb_nota(event))

        # ---------------------------------------------------

        etiqueta_aclaracion = cpt.crear_E(marco_grupo, "NOTA")
        cpt.ordenar(etiqueta_aclaracion, 0, 2, 5, 5)

        self.obt_cond_sql_spbox_nota(valor_spbox2)
        elemento = self.mr.obtener_cond_lista_spbox()
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 1, 2, "2")

        self.spin_X.bind('<Button-1>', lambda event, spbox=self.spin_X: self.mostrar_lista_nota(event, spbox))

        texto_guia = 'Selecione el Curso y presione Enter, haga lo mismo con Materia, finalmente seleccione Nota y presione Editar \n' \
                     'o Insertar segun corresponda, Previo y Siguiente permiten buscar los distintos alumnos del curso seleccionado.'

        etiqueta_aclaracion = cpt.crear_E(marco_texto, texto_guia)
        cpt.ordenar(etiqueta_aclaracion, 0, 0, 5, 5,)
        etiqueta_aclaracion.config(font=("Helvetica", 8))

        # ----------- ETIQUETAS mCUATRO-----------

        listaEtiqueta = []
        lista = ("NOMBRE", "APELLIDO", "DNI")
        self.obt_cond_sql_cajas_texto(valor_spbox1)
        self.mr.id_cond = 'personas.id'
        self.mr.activ_perosnas = 'alumno'

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marco_mat, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        # ----------- CAJAS mCUATRO-----------
        self.lista_c_ed.clear()

        for i in range(len(lista)):
            self.lista_c_ed.append(cpt.crear_C(self.marco_mat, "70"))
            cpt.ordenar(self.lista_c_ed[i], i, 1, 5, 5)

        self.mr.obt_lst_cajas = self.lista_c_ed

    # ----------- FUNC CARGA DE SPBOXs(mostrarMaterias) -----------

    def obt_foco_spbox(self, event, spbox):
        spbox.focus()
        self.listaBoton[3].configure(state='disable')

    def actualizacion_combinada(self, event, valor):
        self.actualizar_spboX_mat(valor)
        self.actualizar_cajas_text(valor)
        self.cantidad_reg = self.mr.chequear_cant_registros_por_anio(valor.get())
        self.conf_btns_materias()

    def actualizar_spboX_mat(self, spbox):
        valor_spbox1 = spbox.get()
        self.obt_cond_sql_spbox_mat(valor_spbox1)
        self.spin_X = self.conjunto_spb[1]
        self.spin_X['value'] = self.mr.obtener_cond_lista_spbox()

    def mostrar_lista_nota(self, event, spbox):
        self.mr.obt_pos_spbox = self.conjunto_spb.index(spbox)

        if self.paso:
            spbox['value'] = self.mr.mostrar_lista_spbox(self.num_func)
            self.paso = False

    def llamar_act_spb_nota(self, event):
        self.id_alumno = self.mr.dar_id_m_materias
        self.actualizar_spboX_nota()

    def actualizar_spboX_nota(self):
        self.spin_X = self.conjunto_spb[1]
        valor_spbox2 = self.spin_X.get()

        if self.id_alumno:
            self.obt_cond_sql_spbox_nota_dos(valor_spbox2)

        else:
            self.obt_cond_sql_spbox_nota(valor_spbox2)

        self.spin_X = self.conjunto_spb[2]                                  # en que spibox coloco la calificacion

        if self.mr.obtener_cond_lista_spbox:
            lista = self.mr.obtener_cond_lista_spbox()

            if lista:
                self.spin_X['value'] = lista                                # asigno la calificacion
                self.listaBoton[0].configure(state='disable')
                self.listaBoton[3].configure(state='normal')

            else:
                self.spin_X['value'] = 0
                self.listaBoton[0].configure(state='normal')
                self.listaBoton[3].configure(state='disable')

            self.paso = True

    def capturar_valor_spb(self):
        self.spin_X = self.conjunto_spb[1]
        asignatura = self.spin_X.get()
        self.spin_X = self.conjunto_spb[2]
        valor_nota = self.spin_X.get()

        return asignatura, valor_nota

    def cond_insertar_mostrarMaterias_spbox(self):
        asignatura, valor_nota = self.capturar_valor_spb()
        columnas = ['id_mat', 'id_nota', 'id_per', 'id']
        tablas = ['mat_nota', 'materias']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'asignatura = \'{asignatura}\''
        self.mr.insertar_mostrarMaterias_spbox(valor_nota, columnas)

    def cond_editar_mostrarMaterias_spbox(self): 
        asignatura, valor_nota = self.capturar_valor_spb()
        columnas = ['id_nota', 'id']
        tablas = ['mat_nota', 'materias']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'asignatura = \'{asignatura}\''
        self.mr.editar_mostrarMaterias_spbox(valor_nota, columnas)

    def obt_cond_sql_spbox_mat(self, valor_spbox1):
        self.mr.seleccionar_columnas = 'asignatura'
        tablas = ['materias', 'curso']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'materias.id_cur = curso.id AND anio = \'{valor_spbox1}\''

    def obt_cond_sql_spbox_nota(self, valor_spbox2):
        self.mr.seleccionar_columnas = 'calific'
        tablas = ['personas', 'materias', 'notas', 'mat_nota']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'personas.id = mat_nota.id_per AND materias.id = mat_nota.id_mat \
                                        AND notas.id = mat_nota.id_nota AND personas.actividad = \'alumno\' \
                                        AND asignatura = \'{valor_spbox2}\''

    def obt_cond_sql_spbox_nota_dos(self, valor_spbox2):
        self.mr.seleccionar_columnas = 'calific'
        tablas = ['personas', 'materias', 'notas', 'mat_nota']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'personas.id = mat_nota.id_per AND materias.id = mat_nota.id_mat \
                                       AND notas.id = mat_nota.id_nota AND asignatura = \'{valor_spbox2}\' \
                                       AND personas.id = \'{self.mr.dar_id_m_materias}\''

        # ----------- FUNC CARGA DE CAJAS DE TEXTO(mostrarMaterias) -----------

    def actualizar_cajas_text(self, valor):
        valor_spbox1 = valor.get()
        self.obt_cond_sql_cajas_texto(valor_spbox1)
        self.mr.obt_lst_cajas = self.lista_c_ed

    def obt_cond_sql_cajas_texto(self, valor_spbox1):
        self.mr.seleccionar_columnas = 'personas.id, nombre, apellido, dni'
        tablas = ['personas', 'curso', 'curso_division_turno']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'personas.id = curso_division_turno.id_per \
                                AND curso.id = curso_division_turno.id_cur \
                                AND curso.anio = \'{valor_spbox1}\' AND personas.actividad = \'alumno\''

    def mostrarCursos(self):
        self.num_func = 4
        self.mr.cargar_num_func = self.num_func

        # ----------- LISTBOXs -----------

        self.mr.obt_lstbox_caja.clear()

        etiqueta_materias = cpt.crear_E(self.marco_curso, "LISTA DE MATERIAS")
        cpt.ordenar(etiqueta_materias, 1, 0, 5, 5, "", 6)

        caja = cpt.crear_Lb(self.marco_curso, "60", "4")
        cpt.ordenar(caja, 2, 0, 5, 5, "", 6)

        self.mr.obt_lstbox_caja = caja

        etiqueta_profesor = cpt.crear_E(self.marco_curso, "LISTA DE PROFESORES")
        cpt.ordenar(etiqueta_profesor, 3, 0, 5, 5, "", 6)

        caja1 = cpt.crear_Lb(self.marco_curso, "60", "4")
        cpt.ordenar(caja1, 4, 0, 5, 5, "", 6)

        self.mr.obt_lstbox_caja = caja1

        etiqueta_alunmos = cpt.crear_E(self.marco_curso, "LISTA DE ALUMNOS")
        cpt.ordenar(etiqueta_alunmos, 5, 0, 5, 5, "", 6)

        caja2 = cpt.crear_Lb(self.marco_curso, "60", "4")
        cpt.ordenar(caja2, 6, 0, 5, 5, "", 6)

        self.mr.obt_lstbox_caja = caja2

        # ----------- MARCO GRUPO PARA SPINBOXs-----------

        marco_grupo = cpt.crear_M(self.marco_curso, "500", "50")
        cpt.ordenar(marco_grupo, 0, 1)

        # ----------- ETIQUETAS y SPINBOXs-----------
        self.conjunto_spb.clear()
        self.list_valor_spb.clear()

        etiqueta_curso = cpt.crear_E(marco_grupo, "CURSO")
        cpt.ordenar(etiqueta_curso, 0, 0, 5, 5)

        elemento = self.mr.obtener_lista_spbox('anio', 'curso')
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 0, 1, "15")
        self.list_valor_spb.append(self.spin_X.get())
        valor_spbox1 = self.list_valor_spb[0]

        self.obt_cond_sql_listbox1(valor_spbox1)

        # ---------------------------------------------------

        etiqueta_curso = cpt.crear_E(marco_grupo, "DIVISION")
        cpt.ordenar(etiqueta_curso, 0, 2, 5, 5)

        elemento = self.mr.obtener_lista_spbox('seccion', 'division')
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 0, 3, "2")
        self.list_valor_spb.append(self.spin_X.get())
        valor_spbox1 = self.list_valor_spb[0]

        self.obt_cond_sql_listbox2(valor_spbox1)

        # ---------------------------------------------------

        etiqueta_curso = cpt.crear_E(marco_grupo, "TURNO")
        cpt.ordenar(etiqueta_curso, 0, 4, 5, 5)

        elemento = self.mr.obtener_lista_spbox('mt', 'turno')
        marco = marco_grupo
        self.definir_spboxs(marco, elemento, 0, 5, "10")
        self.list_valor_spb.append(self.spin_X.get())
        valor_spbox = self.list_valor_spb

        self.obt_cond_sql_listbox3(valor_spbox)

        # ----------- BTN-SPBXs -----------

        marco = marco_grupo
        btn_buscar = cpt.crear_B(marco, 'BUSCAR', "10", comando=self.buscar_list_spb)
        cpt.ordenar(btn_buscar, 0, 6, 15, 5)

    # ----------- FUNC CARGA DE LISTBOXs(mostrarCursos) -----------
   
    ''' Estas 3 funciones generan las consultas adecuadas para que se muestren en los 3 listboxs
    del formulario, 1º las materias, 2º los profesores que dan esas materias y por ultimo los alumnos,
    todo en funcion del curso, division y turno'''

    def obt_cond_sql_listbox1(self, valor_spbox1):
        num_listb = 0
        self.mr.seleccionar_columnas = 'asignatura'
        tablas = ['materias', 'curso']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'materias.id_cur = curso.id AND anio = \'{valor_spbox1}\''
        self.mr.obt_listado_para_lbox(num_listb)

    def obt_cond_sql_listbox2(self, valor_spbox1):
        num_listb = 1
        self.mr.seleccionar_columnas = 'apellido, nombre'
        tablas = ['personas', 'materias', 'curso', 'mat_nota']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'personas.id = mat_nota.id_per AND materias.id = mat_nota.id_mat \
                        AND curso.id = materias.id_cur AND actividad = \'profesor\' AND anio = \'{valor_spbox1}\''
        self.mr.obt_listado_para_lbox(num_listb)

    def obt_cond_sql_listbox3(self, valor_spbox):
        num_listb = 2
        self.mr.seleccionar_columnas = 'apellido, nombre'
        tablas = ['personas', 'curso', 'division', 'turno', 'curso_division_turno']
        self.mr.obt_lts_tablas = tablas
        self.mr.obt_cond_sql = f'personas.id = curso_division_turno.id_per AND curso.id = curso_division_turno.id_cur \
               AND division.id = curso_division_turno.id_div AND turno.id = curso_division_turno.id_tur AND anio = \'{valor_spbox[0]}\' \
               AND seccion = \'{valor_spbox[1]}\' AND mt = \'{valor_spbox[2]}\' AND actividad = \'alumno\''
        self.mr.obt_listado_para_lbox(num_listb)

    # ----------- FUNC SALIDA DEL FORMULARIO-----------

    def salirFormulario(self):
        self.mr.activ_perosnas = None
        self.ventana.destroy()

    # ----------- FUNC PARA MOV POR REGISTROS Y GUARDAR, EDITAR, CARGAR LISTAS EN SPBOXs -----------

    def recorrer_spboxs(self):

        for i in range(len(self.conjunto_spb)):

            if self.conjunto_spb.index(self.conjunto_spb[i]) == self.pos_spbox:
                self.spin_X = self.conjunto_spb[i]
                lista_materias = self.mr.mostrar_lista_spbox(self.num_func)
                self.spin_X['values'] = lista_materias

    def recorrer_spboxs_editar_gaurdar(self):

        for i in range(len(self.conjunto_spb)):
            self.spin_X = self.conjunto_spb[i]
            self.mr.valor_spbox_seleccionado = self.spin_X.get()

    def recorrer_spboxs_gaurdar(self, event):
        tex_btn = self.listaBoton[0].cget('text')

        if tex_btn == 'GUARDAR':
            self.recorrer_spboxs_editar_gaurdar()

    def recorrer_spboxs_editar(self):
        self.recorrer_spboxs_editar_gaurdar()

    def cambiar_valores(self):

        if self.cant < 1:
            self.cant = +1

            if self.num_func == 1:
                self.recorrer_spboxs()

            if self.num_func == 2:
                self.recorrer_spboxs()

            if self.num_func == 3:
                self.recorrer_spboxs()

        tex_btn = self.listaBoton[0].cget('text')

        if tex_btn != 'GUARDAR':
            self.listaBoton[3].configure(state='normal')
        else:
            self.listaBoton[3].configure(state='disable')

    def ob_pos(self, event):
        self.mr.obtenerPosicion(event=event)

    def ob_pos_spbox(self, event, spbox):
        self.pos_spbox = self.conjunto_spb.index(spbox)

        if self.pos_spbox != self.comp_num_spb or self.comp_num_func != self.num_func:
            self.cant = 0
            self.comp_num_func = self.num_func
            self.comp_num_spb = self.pos_spbox
            self.mr.obt_pos_spbox = self.pos_spbox

    def llamar_cambiar_valor(self):
        self.cant = 0
        self.spin_X['command'] = self.cambiar_valores

    # ----------- FUNC QUE COMPLEMENTAN A mostarSig, Prev, editar, etc de la Clase Manejo_registros -----------

    ''' Estas dos funciones complementan a mostrarSig y Prev agregando el manejo de los spinboxs en
    mostrarProfesores, mostrarAlumnos y mostrarMaterias segun el numero de funcion asignado'''
    
    def resetear_spb(self):

        if self.num_func == 1:
            self.spin_X['values'] = [self.mr.mostrar_valor_spbox]

        elif self.num_func == 2:

            for i in range(len(self.conjunto_spb)):
                self.spin_X = self.conjunto_spb[i]                    
                self.spin_X['values'] = self.mr.mostrar_valor_spbox[i]

            spin = self.conjunto_spb[0]
            self.cur_origen = spin.get()

        self.llamar_cambiar_valor()

    def blanquear_spb(self):

        if self.num_func == 1:
            self.spin_X['values'] = '---'

        elif self.num_func == 2:

            for i in range(len(self.conjunto_spb)):
                self.spin_X = self.conjunto_spb[i]
                self.spin_X['values'] = '---'

    def most_sig(self):

        if self.num_func == 3:
            self.spin_X = self.conjunto_spb[0]
            valor = self.spin_X.get()
            self.obt_cond_sql_cajas_texto(valor)
            self.mr.mostrarSiguiente()
            self.id_alumno = self.mr.dar_id_m_materias
            self.actualizar_spboX_nota()
            self.reasignar_func_editar_insertar_spb()
            self.listaBoton[4].configure(state='disable')
        else:
            self.mr.mostrarSiguiente()
            self.resetear_spb()

    def most_prev(self):

        if self.num_func == 3:
            self.spin_X = self.conjunto_spb[0]
            valor = self.spin_X.get()
            self.obt_cond_sql_cajas_texto(valor)
            self.mr.mostarPrevio()
            self.id_alumno = self.mr.dar_id_m_materias
            self.actualizar_spboX_nota()
            self.reasignar_func_editar_insertar_spb()
            self.listaBoton[4].configure(state='disable')
        else:
            self.mr.mostarPrevio()
            self.resetear_spb()

    # ----------- FUNC GUARDAR, EDITAR, BORRAR, BUSCAR-----------

    def insert_reg(self):
        self.mr.insertar_reg()

    def activar(self, event):

        if self.dni_ok is True:
            self.dni_ok = False
            self.mr.activar_guardar()

    def editar(self):
        self.mr.editar()

        if self.num_func == 2:
            spin = self.conjunto_spb[0]
            nuevo = spin.get()

            if nuevo != self.cur_origen:
                self.mr.borrar_rel_mat_nota()

    def borrar(self):
        self.blanquear_spb()
        self.mr.borrar()
    
    def buscar(self):
        valor = self.caja_buscar.get()
        self.mr.buscar(valor)

    def buscar_list_spb(self):
        self.list_valor_spb.clear()

        for i in range(len(self.conjunto_spb)):
            self.spin_X = self.conjunto_spb[i]
            self.list_valor_spb.append(self.spin_X.get())

        valor_spbox = self.list_valor_spb
        self.obt_cond_sql_listbox1(valor_spbox[0])
        self.obt_cond_sql_listbox2(valor_spbox[0])
        self.obt_cond_sql_listbox3(valor_spbox)

    # ----------- FUNC PARA CHEQUEO -----------------------------

    def cheq_contenido(self, event):

        if event.widget.get() == '':
            messagebox.showerror(title="ERROR!", message='Nombre y Apellido deben ser ingresados')
            return

    def cheq_dni(self, event):
        num = event.widget.get()
        resultado = self.mr.chequear_dni(num)
        if resultado is True:
            self.dni_ok = True

    def cheq_fecha(self, event):
        fecha = event.widget.get()
        self.mr.chequear_formateo_fecha(fecha)

    def cheq_mail(self, event):
        mail = event.widget.get()
        self.mr.chequear_mail(mail)