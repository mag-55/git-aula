#!/usr/bin/python3
#-*- coding: utf-8 -*-

import tkinter as tk
import inicio as inc
import componentes as cpt
import claves as clv
import conexion as con 

# FORMULARIO DE INGRESO permite accder a la aplicación en si


class Acceso():

    def __init__(self, raiz):
        self.raiz = raiz
        self.listaCaja = []
        self.listaBoton = []
        self.listaEtiqueta = []

    #----------- VENTANA ACCESO -----------

    def acceder(self):
        lista = ("USUARIO:", "CLAVE:")
        lista2 = ("ENTRAR", "SALIR")
        comando = [self.chequear, quit]

        #----------- MARCO CERO, UNO Y DOS-----------

        marcoCero = cpt.crear_M(self.raiz, "400", "100")
        cpt.ordenar(marcoCero, 0, 0)

        marcoUno = cpt.crear_M(self.raiz, "400", "100")
        cpt.ordenar(marcoUno, 1, 0)

        marcoDos = cpt.crear_M(self.raiz, "400", "50")
        cpt.ordenar(marcoDos, 2, 0)

        #----------- ETIQUETA mUNO-----------

        titulo = cpt.crear_E(marcoCero, "Ingrese su Usuario")
        titulo.configure(font="15")
        cpt.ordenar(titulo, 0, 0, 5, 10)

        #----------- CAJAS TEXTO mUNO-----------

        for i in range(len(lista)):
            self.listaCaja.append(cpt.crear_C(marcoUno, "40"))
            self.listaCaja[i].insert(0, lista[i])
            self.listaCaja[i].configure(foreground="gray")
            cpt.ordenar(self.listaCaja[i], i, 0, 5, 5)

        self.listaCaja[0].bind("<Button-1>", self.limpiar)
        self.listaCaja[1].bind("<Button-1>", self.limpiar)
        self.listaCaja[1].bind("<FocusIn>", self.enmascarar)

        #----------- ETIQUETA mUNO-----------

        crearUs = cpt.crear_E(marcoUno, "Crear nuevo usuario")
        crearUs.configure(foreground="#ff5733", font=("arial", 8, "bold"))
        cpt.ordenar(crearUs, 2, 0, 5, 0, "w")
        crearUs.bind("<Button-1>", self.registrar)

        #----------- BOTONES mDOS-----------

        for i in range(len(lista2)):
            self.listaBoton.append(cpt.crear_B(
                marcoDos, lista2[i], "10", comando[i]))
            cpt.ordenar(self.listaBoton[i], 0, i, 5, 5)

    def limpiar(self, event):
        event.widget.delete(0, tk.END)
        return None

    def enmascarar(self, event):
        self.listaCaja[1].delete(0, tk.END)
        self.listaCaja[1].configure(show="*")

    def registrar(self, event):
        valor = "usuario"
        inc.abrir(valor)

    def chequear(self):
        # self.raiz.withdraw()
        return clv.chequear(self.listaCaja)

    def cerrar(self):
        self.raiz.destroy()

# FORMULARIO DE REGISTRO DE NUEVO USUARIO


class RegistroUsuario():

    def __init__(self, ventana):

        self.ventana = ventana
        self.ventana.title("REGISTRO DE USUARIOS")
        self.listaEtiqueta = []
        self.listaCaja = []
        self.listaBoton = []
        self.lista_v = []
        self.lista_va = []
        self.var = tk.StringVar()
        self.id = 0
        self.pos = []
        self.indice = 0
        self.lista_f = []

        
    def registrarUs(self):

        lista = ( "USUARIO", "CLAVE", "CONF CLAVE", "NOMBRE", "APELLIDO", "DNI", "FECHA", "TEL", "MAIL", "CALLE", "BARRIO",
                 "LOCALIDAD", "CP")
        lista2 = ("GUARDAR", "PREVIO", "SIGUIENTE", "EDITAR", "BORRAR", "SALIR")
        comando = [self.guardar, self.mostarPrevio, self.mostarSiguiente, self.editar, self.borrar, quit]

        #----------- MARCO UNO Y DOS-----------

        marcoUno = cpt.crear_M(self.ventana, "500",  "400")
        cpt.ordenar(marcoUno, 0, 0)

        marcoDos = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(marcoDos, 1, 0)

        #----------- ETIQUETAS mUNO-----------

        for i in range(len(lista)):

            self.listaEtiqueta.append(cpt.crear_E(marcoUno, lista[i]))
            cpt.ordenar(self.listaEtiqueta[i], i, 0, 5, 5)

        #----------- CAJAS mUNO-----------

        for i in range(len(lista)):
            self.listaCaja.append(cpt.crear_C(marcoUno, "50"))
            if self.listaCaja[i] != self.listaCaja[0]:
                self.listaCaja[i].configure(state='disabled')
            cpt.ordenar(self.listaCaja[i], i, 1, 5, 5)

        #----------- BOTONES mDOS-----------

        for i in range(len(lista2)):
            self.listaBoton.append(cpt.crear_B(marcoDos, lista2[i], "9", comando[i]))
            cpt.ordenar(self.listaBoton[i], 0, i, 1, 5)
        
        self.listaBoton[1].configure(state='disabled')
        self.listaBoton[3].configure(state='disabled')

        #----------- ENLACES PARA LAS FUC-----------

        self.listaCaja[0].bind("<Return>", self.validarU)
        self.listaCaja[1].bind("<Return>", self.validarC)
        self.listaCaja[2].bind("<Return>", self.chequear_Cl1_Cl2)
        #self.listaCaja[i].bind_all("<Double-Button-1>", self.obtenerPosicion)
        self.listaCaja[i].bind_class("Entry", "<Double-Button-1>", self.obtenerPosicion)

    #----------- FUNC VALIDA USUARIO Y CLAVE(tabién verifica us != cl y cl == ccl)-----------

    def validarU(self,event):
        return clv.validarUsuario(self.listaCaja)

    def validarC(self, event):
        return clv.validarClave(self.listaCaja)

    def chequear_Cl1_Cl2(self, event):
        return clv.compararClaves(self.listaCaja)
    
    #----------- FUNC GUARDAR, EDITAR, BORRAR----------- 

    def obtenerValores(self): #ok

        for i in range(len(self.listaCaja)):
            self.lista_v.append(self.listaCaja[i].get())

        return self.lista_v

    def obtenerPosicion(self, event): #ok
        #ver que se haga solo dentro de marco uno!!!!
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
        
    def mostrarValores(self, listado): #ok

        self.lista_f.extend(listado)

        if len(self.lista_f) == len(self.listaCaja):
            
            for i in range(len(self.lista_f)):
                self.listaCaja[i].insert(0, self.lista_f[i])
            
            self.lista_f = []

    def mostarPrevio(self): #ok
        self.listaBoton[2].configure(state='normal')
        x =+ 1
        self.id = self.id - x
            
        for i in range(len(self.listaCaja)):
            self.listaCaja[i].delete(0, tk.END)
            if self.listaCaja[i] != self.listaCaja[0]: #VER SOLUCIONAR ESTE DETALLE
                self.listaCaja[i].configure(state='normal')

        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(self.id)
        datos = con.Datos(lista_t)
        consulta = con.Consultas(datos, condicion)

        for i in range(len(lista_t)):
            datos.set_i(i)
            listado = consulta.ejecutar(consulta.mostrar())
            if listado == None:
                x =+ 1
                self.id = self.id - x
                condicion = "id = " + str(self.id)
                consulta = con.Consultas(datos, condicion)
                listado = consulta.ejecutar(consulta.mostrar())
                if listado == None:
                    self.listaBoton[1].configure(state='disabled')
                    self.listaBoton[0].configure(state='normal')
                    break
            self.mostrarValores(listado)

    def mostarSiguiente(self): #ok
        self.listaBoton[1].configure(state='normal')
        self.listaBoton[0].configure(state='disable')
        x =+ 1
        self.id = self.id + x

        for i in range(len(self.listaCaja)):
            self.listaCaja[i].delete(0, tk.END)
            if self.listaCaja[i] != self.listaCaja[0]: #VER SOLUCIONAR ESTE DETALLE
                self.listaCaja[i].configure(state='normal')

        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(self.id)
        datos = con.Datos(lista_t)
        consulta = con.Consultas(datos, condicion)

        for i in range(len(lista_t)):
            datos.set_i(i)
            listado = consulta.ejecutar(consulta.mostrar())
            if listado == None:
                x =+ 1
                self.id = self.id + x
                condicion = "id = " + str(self.id)
                consulta = con.Consultas(datos, condicion)
                listado = consulta.ejecutar(consulta.mostrar())
                if listado == None:
                    self.listaBoton[2].configure(state='disabled')
                    break
            self.mostrarValores(listado)

    def guardar(self): #ok

        lista_v = self.obtenerValores() 
        lista_t = ['preceptores', 'barrio', 'localidad']

        datos = con.Datos(lista_t, lista_v)
        consulta = con.Consultas(datos)

        for i in range(len(lista_t)): #de esta manera va cambiando las tablas, de lo contrario solo rellena la primera
            datos.set_i(i)
            consulta.ejecutar(consulta.insertar())

    def editar(self): #ok

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
            if datos.repetido <= 1:
                datos.set_i(0)
                datos.longitud = 0
                consulta.ejecutar(consulta.actualizar())
            else:
                datos.posicion = []
            
    def borrar(self): #ok

        lista_t = ['preceptores', 'barrio', 'localidad']
        condicion = "id = " + str(self.id)
        datos = con.Datos(lista_t)
        consulta = con.Consultas(datos, condicion)

        for i in range(len(lista_t)):
            datos.set_i(i)
            consulta.ejecutar(consulta.borrar())

        for i in range(len(self.listaCaja)):
            self.listaCaja[i].delete(0, tk.END)
          
    

# FORMULARIO DE INGRESO DE DATOS


class RegistroGral():

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("BIENVENIDO AL AULA")
        self.list_spin = None
        self.marcoSpin = cpt.crear_M(self.ventana, "500", "50")
        cpt.ordenar(self.marcoSpin, 0, 0)
        self.marcoDos = cpt.crear_M(self.ventana, "500", "0")
        self.ocultar(self.marcoDos)
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
        lista = ("SELECCIONE UNA OPCION", "PROFESORES",
                 "ALUMNOS", "CURSOS", "MATERIAS")
        lista2 = ("GUARDAR", "PREVIO", "SIGUIENTE",
                  "EDITAR", "BORRAR", "SALIR")
        listaBoton = []
        comando = quit
        seleccion = self.ventana.register(self.capturar)

        self.list_spin = cpt.crear_Sp(
            self.marcoSpin, lista, "80", "normal", "center", comando=seleccion)
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
            self.mostar(self.marcoDos)
        elif captura == "ALUMNOS":
            self.ocultar(self.marcoDos)
            self.ocultar(self.marcoCuatro)
            self.mostar(self.marcoTres)
        elif captura == "CURSOS":
            self.ocultar(self.marcoTres)
            self.ocultar(self.marcoCinco)
            self.mostar(self.marcoCuatro)
        elif captura == "MATERIAS":
            self.ocultar(self.marcoCuatro)
            self.mostar(self.marcoCinco)
        else:
            self.ocultar(self.marcoDos)

    def mostrarProfesor(self):
        listaEtiqueta = []
        listaCaja = []
        lista = ("NOMBRE", "APELLIDO", "DNI",
                 "FECHA", "DIRECCION", "TEL", "MAIL")

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marcoDos, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        for i in range(len(lista)):
            listaCaja.append(cpt.crear_C(self.marcoDos, "70"))
            cpt.ordenar(listaCaja[i], i, 1, 5, 5)

    def mostrarAlumnos(self):
        listaEtiqueta = []
        listaCaja = []
        lista = ("NOMBRE", "APELLIDO", "DNI", "FECHA", "DIRECCION", "TEL",
                 "PADRE", "TRABAJO", "TEL", "MADRE", "TRABAJO", "TEL", "MAIL", "CURSO")

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

        etiqueta_curso = cpt.crear_E(self.marcoCuatro, "AÑO")
        cpt.ordenar(etiqueta_curso, 0, 0, 5, 5)
        list_spin1 = cpt.crear_Sp(
            self.marcoCuatro, lista, "15", "normal", "center")
        cpt.ordenar(list_spin1, 0, 1, 5, 5)

        for i in range(len(lista2)):
            listaRb.append(cpt.crear_Rb(self.marcoCuatro, lista2[i], i, selec))
            cpt.ordenar(listaRb[i], 0, i + 2, 5, 5)

        for i in range(len(lista3)):
            listaRb2.append(cpt.crear_Rb(self.marcoCuatro, lista3[i], i, selec2))
            cpt.ordenar(listaRb2[i], 0, i + 4, 5, 5)

        etiqueta_materias = cpt.crear_E(self.marcoCuatro, "LISTA DE MATERIAS")
        cpt.ordenar(etiqueta_materias, 1, 0, 5, 5, "", 6)
        caja = cpt.crear_Lb(self.marcoCuatro, "60", "4")
        cpt.ordenar(caja, 2, 0, 5, 5, "", 6)

        etiqueta_profesor = cpt.crear_E(self.marcoCuatro, "LISTA DE PROFESORES")
        cpt.ordenar(etiqueta_profesor, 3, 0, 5, 5, "", 6)
        caja1 = cpt.crear_Lb(self.marcoCuatro, "60", "4")
        cpt.ordenar(caja1, 4, 0, 5, 5, "", 6)

        etiqueta_alunmos = cpt.crear_E(self.marcoCuatro, "LISTA DE ALUMNOS")
        cpt.ordenar(etiqueta_alunmos, 5, 0, 5, 5, "", 6)
        caja3 = cpt.crear_Lb(self.marcoCuatro, "60", "4")
        cpt.ordenar(caja3, 6, 0, 5, 5, "", 6)

    def mostrarMaterias(self):
        listaEtiqueta = []
        listaCaja = []
        lista = ("ALUMNO", "NOTA")

        for i in range(len(lista)):
            listaEtiqueta.append(cpt.crear_E(self.marcoCinco, lista[i]))
            cpt.ordenar(listaEtiqueta[i], i, 0, 5, 5)

        for i in range(len(lista)):
            listaCaja.append(cpt.crear_C(self.marcoCinco, "70"))
            cpt.ordenar(listaCaja[i], i, 1, 5, 5)
