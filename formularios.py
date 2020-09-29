#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import inicio as inc
import componentes as cpt
import claves as clv
import conexion as con 

# FORMULARIO DE INGRESO permite accder a la aplicación en si


class Acceso:

    def __init__(self, raiz):
        self.raiz = raiz
        self.listaCaja = []
        self.listaBoton = []
        self.listaEtiqueta = []

    # ----------- VENTANA ACCESO -----------

    def acceder(self):
        lista = ("USUARIO:", "CLAVE:")
        lista2 = ("ENTRAR", "SALIR")
        comando = [self.chequear, self.cerrar]

        # ----------- MARCO CERO, UNO Y DOS-----------

        marcoCero = cpt.crear_M(self.raiz, "400", "100")
        cpt.ordenar(marcoCero, 0, 0)

        marco_uno = cpt.crear_M(self.raiz, "400", "100")
        cpt.ordenar(marco_uno, 1, 0)

        marco_dos = cpt.crear_M(self.raiz, "400", "50")
        cpt.ordenar(marco_dos, 2, 0)

        # ----------- ETIQUETA mUNO-----------

        titulo = cpt.crear_E(marcoCero, "Ingrese su Usuario")
        titulo.configure(font="15")
        cpt.ordenar(titulo, 0, 0, 5, 10)

        # ----------- CAJAS TEXTO mUNO-----------

        for i in range(len(lista)):
            self.listaCaja.append(cpt.crear_C(marco_uno, "40"))
            self.listaCaja[i].insert(0, lista[i])
            self.listaCaja[i].configure(foreground="gray")
            cpt.ordenar(self.listaCaja[i], i, 0, 5, 5)

        self.listaCaja[0].bind("<Button-1>", self.limpiar)
        self.listaCaja[1].bind("<Button-1>", self.limpiar)
        self.listaCaja[1].bind("<FocusIn>", self.enmascarar)

        # ----------- ETIQUETA mUNO-----------

        crearUs = cpt.crear_E(marco_uno, "Crear nuevo usuario")
        crearUs.configure(foreground="#ff5733", font=("arial", 8, "bold"))
        cpt.ordenar(crearUs, 2, 0, 5, 0, "w")
        crearUs.bind("<Button-1>", self.registrar)

        # ----------- BOTONES mDOS-----------

        for i in range(len(lista2)):
            self.listaBoton.append(cpt.crear_B(marco_dos, lista2[i], "10", comando[i]))
            cpt.ordenar(self.listaBoton[i], 0, i, 5, 5)

    def limpiar(self, event):
        event.widget.delete(0, tk.END)
        return None

    def enmascarar(self, event):
        self.listaCaja[1].delete(0, tk.END)
        self.listaCaja[1].configure(show="*")

    def registrar(self, event):
        return clv.chequear_a(self.raiz, self.listaCaja)

    def chequear(self):
        return clv.chequear_u(self.listaCaja)

    def cerrar(self):
        quit()


# FORMULARIO DE INGRESO permite accder a la aplicación en si


class Manejo_registros:

    def __init__(self, lista_caja=[], lista_boton=[]):
        self.listaCaja = lista_caja
        self.listaBoton = lista_boton
        self.lista_v = []
        self.id = 0
        self.pos = []
        self.lista_f = []

    def obtenerValores(self):  # ok
        for i in range(len(self.listaCaja)):
            self.lista_v.append(self.listaCaja[i].get())

        return self.lista_v

    def obtenerPosicion(self, event):  # ok
        self.listaBoton[3].configure(state='normal')
        event.widget.delete(0, tk.END)
        pos = str(event.widget.focus_get())

        if pos[-1] == "y":
            indice = 1
        elif pos[-3] == "y":
            indice = int(pos[-2: ])
        else:
            indice = int(pos[-1])

        self.pos.append(indice)

    def mostrarValores(self, listado):  # ok
        self.lista_f.extend(listado)

        if len(self.lista_f) == len(self.listaCaja):
            for i in range(len(self.lista_f)):
                self.listaCaja[i].insert(0, self.lista_f[i])

            self.lista_f = []

    def limpiar_casilleros(self):
        for i in range(len(self.listaCaja)):
            self.listaCaja[i].delete(0, tk.END)
            if self.listaCaja[i] != self.listaCaja[0]:  # VER SOLUCIONAR ESTE DETALLE
                self.listaCaja[i].configure(state='normal')

    def mostarPrevio(self):  # ok
        self.listaBoton[2].configure(state='normal')
        x = + 1
        self.id = self.id - x
        self.limpiar_casilleros()
        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(self.id)
        datos = con.Datos(lista_t)
        consulta = con.Consultas(datos, condicion)

        for i in range(len(lista_t)):
            datos.set_i(i)
            listado = consulta.ejecutar(consulta.mostrar())
            if listado is None:
                x = + 1
                self.id = self.id - x
                condicion = "id = " + str(self.id)
                consulta = con.Consultas(datos, condicion)
                listado = consulta.ejecutar(consulta.mostrar())
                if listado is None:
                    self.listaBoton[1].configure(state='disabled')
                    self.listaBoton[0].configure(state='normal')
                    break
            self.mostrarValores(listado)

    def mostarSiguiente(self):  # ok
        self.listaBoton[1].configure(state='normal')
        self.listaBoton[0].configure(state='disable')
        x = + 1
        self.id = self.id + x
        self.limpiar_casilleros()
        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(self.id)
        datos = con.Datos(lista_t)
        consulta = con.Consultas(datos, condicion)

        for i in range(len(lista_t)):
            datos.set_i(i)
            listado = consulta.ejecutar(consulta.mostrar())
            if listado is None:
                x = + 1
                self.id = self.id + x
                condicion = "id = " + str(self.id)
                consulta = con.Consultas(datos, condicion)
                listado = consulta.ejecutar(consulta.mostrar())
                if listado is None:
                    self.listaBoton[2].configure(state='disabled')
                    break
            self.mostrarValores(listado)

    def guardar(self):  # ok
        lista_v = self.obtenerValores()
        lista_t = ['preceptores', 'barrio', 'localidad']
        datos = con.Datos(lista_t, lista_v)
        consulta = con.Consultas(datos)

        for i in range(len(lista_t)):  # de esta manera va cambiando las tablas, de lo contrario solo rellena la primera
            datos.set_i(i)
            consulta.ejecutar(consulta.insertar())

    def editar(self):  # ok
        lista_v = []
        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(self.id)
        posicion = self.pos

        for i in range(len(self.pos)):
            x = posicion[i] - 1
            lista_v.append(self.listaCaja[x].get())

        datos = con.Datos(lista_t, lista_v)
        datos.set_posicion(posicion)
        consulta = con.Consultas(datos, condicion)
        consulta.ejecutar(consulta.actualizar())

        while not datos.posicion == []:
            datos.set_i(0)
            datos.longitud = 0
            consulta.ejecutar(consulta.actualizar())

        clv.op_exitosa()

    def borrar(self):  # ok
        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(self.id)
        datos = con.Datos(lista_t)
        consulta = con.Consultas(datos, condicion)

        for i in range(len(lista_t)):
            datos.set_i(i)
            consulta.ejecutar(consulta.borrar())

        for i in range(len(self.listaCaja)):
            self.listaCaja[i].delete(0, tk.END)

    # ----------- FUNC BUSCAR DNI-----------

    def buscar(self, valor):
        tabla = "preceptores"
        condicion = "dni"
        datos = con.Datos()
        consulta = con.Consultas(datos)
        id = consulta.buscar_id(tabla, condicion, valor)

        self.limpiar_casilleros()
        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(id[0])
        datos = con.Datos(lista_t)
        consulta = con.Consultas(datos, condicion)

        for i in range(len(lista_t)):
            datos.set_i(i)
            listado = consulta.ejecutar(consulta.mostrar())
            self.mostrarValores(listado)


# FORMULARIO DE REGISTRO DE NUEVO USUARIO


class RegistroUsuario:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("REGISTRO DE USUARIOS")
        self.listaEtiqueta = []
        self.listaCaja = []
        self.listaBoton = []
        #self.lista_v = []
        #self.id = 0
        #self.pos = []
        #self.lista_f = []
        self.caja_buscar = None
        list_caja = self.listaCaja
        list_boton = self.listaBoton
        self.mr = Manejo_registros(list_caja, list_boton)

    # ----------- VENTANA REGISTRO DE USUARIO -----------

    def registrarUs(self):
        lista = ("USUARIO", "CLAVE", "CONF CLAVE", "NOMBRE", "APELLIDO", "DNI", "FECHA", "TEL", "MAIL", "CALLE", "BARRIO", "LOCALIDAD", "CP")
        lista2 = ("GUARDAR", "PREVIO", "SIGUIENTE", "EDITAR", "BORRAR", "SALIR")
        comando = [self.guardar, self.most_prev, self.most_sig, self.editar, self.borrar, self.salirFormulario]

        # ----------- MARCO UNO Y DOS-----------

        marco_uno = cpt.crear_M(self.ventana, "500",  "400")
        cpt.ordenar(marco_uno, 0, 0)
        
        marco_buscar = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(marco_buscar, 1, 0)

        marco_dos = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(marco_dos, 2, 0)

        # ----------- ETIQUETAS mUNO-----------

        for i in range(len(lista)):
            self.listaEtiqueta.append(cpt.crear_E(marco_uno, lista[i]))
            cpt.ordenar(self.listaEtiqueta[i], i, 0, 5, 5)

        # ----------- CAJAS mUNO-----------

        for i in range(len(lista)):
            self.listaCaja.append(cpt.crear_C(marco_uno, "50"))
            if self.listaCaja[i] != self.listaCaja[0]:
                self.listaCaja[i].configure(state='disabled')
            cpt.ordenar(self.listaCaja[i], i, 1, 5, 5)

        # ----------- CAJA-BUSCAR mBUSCAR-----------

        self.caja_buscar = cpt.crear_C(marco_buscar, "20")
        self.caja_buscar.insert(0, "Ingrese DNI:")
        self.caja_buscar.configure(foreground="gray")
        cpt.ordenar(self.caja_buscar, 0, 1, 1, 1)
        self.caja_buscar.bind("<FocusIn>", self.limpiar)

        boton_buscar = cpt.crear_B(marco_buscar, "Buscar", "9", self.buscar)
        cpt.ordenar(boton_buscar, 0, 2, 1, 1)

        # ----------- BOTONES mDOS-----------

        for i in range(len(lista2)):
            self.listaBoton.append(cpt.crear_B(marco_dos, lista2[i], "9", comando[i]))
            cpt.ordenar(self.listaBoton[i], 0, i, 1, 5)
        
        self.listaBoton[1].configure(state='disabled')
        self.listaBoton[3].configure(state='disabled')

        # ----------- ENLACES PARA LAS FUC-----------

        self.listaCaja[0].bind("<Return>", self.validarU)
        self.listaCaja[1].bind("<Return>", self.validarC)
        self.listaCaja[2].bind("<Return>", self.chequear_Cl1_Cl2)
        self.listaCaja[i].bind_class("Entry", "<Double-Button-1>", self.ob_pos)

    # ----------- FUNC SALIDA DEL FORMULARIO-----------

    def salirFormulario (self): # VER ESTO NO SE COMPORTA COMO DEBERIA!!!!
        self.ventana.destroy()
        inc.iniciar()

    # ----------- FUNC LIMPIAR CAJA BUSCAR-----------

    def limpiar(self, event):
        event.widget.delete(0, tk.END)
        return None

    # ----------- FUNC VALIDA USUARIO Y CLAVE(tabién verifica us != cl y cl == ccl)-----------

    def validarU(self, event):
        return clv.validarUsuario(self.listaCaja)

    def validarC(self, event):
        return clv.validarClave(self.listaCaja)

    def chequear_Cl1_Cl2(self, event):
        return clv.compararClaves(self.listaCaja)
    
    # ----------- FUNC GUARDAR, EDITAR, BORRAR-----------

    def ob_val(self):
        self.mr.obtenerValores()

    def ob_pos(self, event):
        self.mr.obtenerPosicion(event=event)

    def most_val(self, listado):
        self.mr.mostrarValores(listado)

    def lim_caslleros(self):
        self.mr.limpiar_casilleros()

    def most_prev(self):
        self.mr.mostarPrevio()

    def most_sig(self):
        self.mr.mostarSiguiente()

    def guardar(self):
        self.mr.guardar()

    def editar(self):
        self.mr.editar()

    def borrar(self):
        self.mr.borrar()

    def buscar(self):
        valor = self.caja_buscar.get()
        self.mr.buscar(valor)
# ----------------------------------------------------------------
#     def obtenerValores(self): #ok
#         for i in range(len(self.listaCaja)):
#             self.lista_v.append(self.listaCaja[i].get())
#
#         return self.lista_v
#
#     def obtenerPosicion(self, event): #ok
#         self.listaBoton[3].configure(state='normal')
#         event.widget.delete(0, tk.END)
#         pos = str(event.widget.focus_get())
#
#         if pos[-1] == "y":
#             indice = 1
#         elif pos[-3] == "y":
#             indice = int(pos[-2: ])
#         else:
#             indice = int(pos[-1])
#
#         self.pos.append(indice)
#
#     def mostrarValores(self, listado): #ok
#         self.lista_f.extend(listado)
#
#         if len(self.lista_f) == len(self.listaCaja):
#             for i in range(len(self.lista_f)):
#                 self.listaCaja[i].insert(0, self.lista_f[i])
#
#             self.lista_f = []
#
#     def limpiar_casilleros(self):
#         for i in range(len(self.listaCaja)):
#             self.listaCaja[i].delete(0, tk.END)
#             if self.listaCaja[i] != self.listaCaja[0]:  # VER SOLUCIONAR ESTE DETALLE
#                 self.listaCaja[i].configure(state='normal')
#
#     def mostarPrevio(self):  # ok
#         self.listaBoton[2].configure(state='normal')
#         x = + 1
#         self.id = self.id - x
#         self.limpiar_casilleros()
#         lista_t = ['preceptores', 'barrio', 'localidad']
#         condicion = "id = " + str(self.id)
#         datos = con.Datos(lista_t)
#         consulta = con.Consultas(datos, condicion)
#
#         for i in range(len(lista_t)):
#             datos.set_i(i)
#             listado = consulta.ejecutar(consulta.mostrar())
#             if listado is None:
#                 x = + 1
#                 self.id = self.id - x
#                 condicion = "id = " + str(self.id)
#                 consulta = con.Consultas(datos, condicion)
#                 listado = consulta.ejecutar(consulta.mostrar())
#                 if listado is None:
#                     self.listaBoton[1].configure(state='disabled')
#                     self.listaBoton[0].configure(state='normal')
#                     break
#             self.mostrarValores(listado)
#
#     def mostarSiguiente(self):  # ok
#         self.listaBoton[1].configure(state='normal')
#         self.listaBoton[0].configure(state='disable')
#         x = + 1
#         self.id = self.id + x
#         self.limpiar_casilleros()
#         lista_t = ['preceptores', 'barrio', 'localidad']
#         condicion = "id = " + str(self.id)
#         datos = con.Datos(lista_t)
#         consulta = con.Consultas(datos, condicion)
#
#         for i in range(len(lista_t)):
#             datos.set_i(i)
#             listado = consulta.ejecutar(consulta.mostrar())
#             if listado is None:
#                 x = + 1
#                 self.id = self.id + x
#                 condicion = "id = " + str(self.id)
#                 consulta = con.Consultas(datos, condicion)
#                 listado = consulta.ejecutar(consulta.mostrar())
#                 if listado is None:
#                     self.listaBoton[2].configure(state='disabled')
#                     break
#             self.mostrarValores(listado)
#
#     def guardar(self):  # ok
#         lista_v = self.obtenerValores()
#         lista_t = ['preceptores', 'barrio', 'localidad']
#         datos = con.Datos(lista_t, lista_v)
#         consulta = con.Consultas(datos)
#
#         for i in range(len(lista_t)):  # de esta manera va cambiando las tablas, de lo contrario solo rellena la primera
#             datos.set_i(i)
#             consulta.ejecutar(consulta.insertar())
#
#     def editar(self):  # ok
#         lista_v = []
#         lista_t = ['preceptores', 'barrio', 'localidad']
#         condicion = "id = " + str(self.id)
#         posicion = self.pos
#
#         for i in range(len(self.pos)):
#             x = posicion[i] - 1
#             lista_v.append(self.listaCaja[x].get())
#
#         datos = con.Datos(lista_t, lista_v)
#         datos.set_posicion(posicion)
#         consulta = con.Consultas(datos, condicion)
#         consulta.ejecutar(consulta.actualizar())
#
#         while not datos.posicion == []:
#             datos.set_i(0)
#             datos.longitud = 0
#             consulta.ejecutar(consulta.actualizar())
#
#         clv.op_exitosa()
#
#     def borrar(self):  # ok
#         lista_t = ['preceptores', 'barrio', 'localidad']
#         condicion = "id = " + str(self.id)
#         datos = con.Datos(lista_t)
#         consulta = con.Consultas(datos, condicion)
#
#         for i in range(len(lista_t)):
#             datos.set_i(i)
#             consulta.ejecutar(consulta.borrar())
#
#         for i in range(len(self.listaCaja)):
#             self.listaCaja[i].delete(0, tk.END)
#
#     # ----------- FUNC BUSCAR DNI-----------
#
#     def buscar(self):
#         tabla = "preceptores"
#         valor = self.caja_buscar.get()
#         datos = con.Datos()
#         consulta = con.Consultas(datos)
#         id = consulta.buscar_id(tabla, valor)
#
#         self.limpiar_casilleros()
#         lista_t = ['preceptores', 'barrio', 'localidad']
#         condicion = "id = " + str(id[0])
#         datos = con.Datos(lista_t)
#         consulta = con.Consultas(datos, condicion)
#
#         for i in range(len(lista_t)):
#             datos.set_i(i)
#             listado = consulta.ejecutar(consulta.mostrar())
#             self.mostrarValores(listado)


# FORMULARIO DE INGRESO DE DATOS


class RegistroGral:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("BIENVENIDO AL AULA")
        self.list_spin = None
        self.marcoSpin = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(self.marcoSpin, 0, 0)
        self.marco_dos = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marco_dos)
        self.marcoTres = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marcoTres)
        self.marcoCuatro = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marcoCuatro)
        self.marcoCinco = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marcoCinco)
        self.marcoBoton = cpt.crear_M(self.ventana, "500", "15")
        cpt.ordenar(self.marcoBoton, 2, 0)
        self.mostrarProfesor()
        self.mostrarAlumnos()
        self.mostrarCursos()
        self.mostrarMaterias()

    def registrarGral(self):
        lista = ("SELECCIONE UNA OPCION", "PROFESORES", "ALUMNOS", "MATERIAS", "CURSOS")
        lista2 = ("GUARDAR", "PREVIO", "SIGUIENTE", "EDITAR", "BORRAR", "SALIR")
        listaBoton = []
        comando = quit

        seleccion = self.ventana.register(self.capturar)
        self.list_spin = cpt.crear_Sp(self.marcoSpin, lista, "80", "normal", "center", comando=seleccion)
        cpt.ordenar(self.list_spin, 0, 0, 5, 5, "N")

        for i in range(len(lista2)):
            listaBoton.append(cpt.crear_B(
                self.marcoBoton, lista2[i], "10", comando))
            cpt.ordenar(listaBoton[i], 0, i, 0, 5)

    def ocultar(self, marco):
        marco.grid_forget()

    def mostar(self, marco):
        cpt.ordenar(marco, 1, 0)

    def capturar(self):
        captura = self.list_spin.get()

        if captura == "PROFESORES":
            self.ocultar(self.marcoTres)
            self.mostar(self.marco_dos)
        elif captura == "ALUMNOS":
            self.ocultar(self.marco_dos)
            self.ocultar(self.marcoCuatro)
            self.mostar(self.marcoTres)
        elif captura == "MATERIAS":
            self.ocultar(self.marcoTres)
            self.ocultar(self.marcoCinco)
            self.mostar(self.marcoCuatro)
        elif captura == "CURSOS":
            self.ocultar(self.marcoCuatro)
            self.mostar(self.marcoCinco)
        else:
            self.ocultar(self.marco_dos)

    def mostrarProfesor(self):
        listaEtiqueta = []
        listaCaja = []
        lista = ("NOMBRE", "APELLIDO", "DNI", "FECHA", "DIRECCION", "TEL", "MAIL")

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marco_dos, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        for i in range(len(lista)):
            listaCaja.append(cpt.crear_C(self.marco_dos, "70"))
            cpt.ordenar(listaCaja[i], i, 1, 5, 5)

    def mostrarAlumnos(self):
        listaEtiqueta = []
        listaCaja = []
        lista = ("NOMBRE", "APELLIDO", "DNI", "FECHA", "DIRECCION", "TEL", "PADRE", "TRABAJO", "TEL", "MADRE", "TRABAJO", "TEL", "MAIL", "CURSO")

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marcoTres, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        for i in range(len(lista)):
            listaCaja.append(cpt.crear_C(self.marcoTres, "70"))
            cpt.ordenar(listaCaja[i], i, 1, 5, 5)

    def mostrarCursos(self):
        list_spin1 = None
        listaRb = []
        listaRb2 = []
        lista = ("PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO")
        lista2 = ("A", "B")
        lista3 = ("M", "T")
        selec = tk.IntVar()
        selec2 = tk.IntVar()

        etiqueta_curso = cpt.crear_E(self.marcoCinco, "AÑO")
        cpt.ordenar(etiqueta_curso, 0, 0, 5, 5)
        list_spin1 = cpt.crear_Sp(
            self.marcoCinco, lista, "15", "normal", "center")
        cpt.ordenar(list_spin1, 0, 1, 5, 5)

        for i in range(len(lista2)):
            listaRb.append(cpt.crear_Rb(self.marcoCinco, lista2[i], i, selec))
            cpt.ordenar(listaRb[i], 0, i + 2, 5, 5)

        for i in range(len(lista3)):
            listaRb2.append(cpt.crear_Rb(self.marcoCinco, lista3[i], i, selec2))
            cpt.ordenar(listaRb2[i], 0, i + 4, 5, 5)

        etiqueta_materias = cpt.crear_E(self.marcoCinco, "LISTA DE MATERIAS")
        cpt.ordenar(etiqueta_materias, 1, 0, 5, 5, "", 6)
        caja = cpt.crear_Lb(self.marcoCinco, "60", "4")
        cpt.ordenar(caja, 2, 0, 5, 5, "", 6)

        etiqueta_profesor = cpt.crear_E(self.marcoCinco, "LISTA DE PROFESORES")
        cpt.ordenar(etiqueta_profesor, 3, 0, 5, 5, "", 6)
        caja1 = cpt.crear_Lb(self.marcoCinco, "60", "4")
        cpt.ordenar(caja1, 4, 0, 5, 5, "", 6)

        etiqueta_alunmos = cpt.crear_E(self.marcoCinco, "LISTA DE ALUMNOS")
        cpt.ordenar(etiqueta_alunmos, 5, 0, 5, 5, "", 6)
        caja3 = cpt.crear_Lb(self.marcoCinco, "60", "4")
        cpt.ordenar(caja3, 6, 0, 5, 5, "", 6)

    def mostrarMaterias(self):
        listaEtiqueta = []
        listaCaja = []
        lista = ("ALUMNO", "NOTA")

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marcoCuatro, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        for i in range(len(lista)):
            listaCaja.append(cpt.crear_C(self.marcoCuatro, "70"))
            cpt.ordenar(listaCaja[i], i, 1, 5, 5)
