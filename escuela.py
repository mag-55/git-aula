#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sqlite3

conexion = sqlite3.connect('escuela.db')

conexion.execute("""CREATE TABLE IF NOT EXISTS alumnos(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre 	TEXT,
	apellido TEXT,
	dni INTEGER UNIQUE,
	fecha TEXT,
	telefono TEXT,
	mail TEXT,
	id_ba INTEGER,
	id_pre INTEGER,
	id_curso INTEGER,
	FOREIGN KEY(id_curso) REFERENCES curso(id),
	FOREIGN KEY(id_pre) REFERENCES preceptores(id),
	FOREIGN KEY(id_ba) REFERENCES barrio(id));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS profesores(
	id_prof INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre TEXT,
	apellido TEXT,
	dni INTEGER UNIQUE,
	fecha TEXT,
	telefono TEXT,
	mail TEXT,
	id_ba INTEGER,
	FOREIGN KEY(id_ba) REFERENCES barrio(id_ba));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS preceptores(
	id_pre INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	usuario TEXT,
	clave TEXT,
	conf_clave TEXT,
	nombre TEXT,
	apellido TEXT,
	dni INTEGER UNIQUE,
	fecha TEXT,
	telefono TEXT,
	mail TEXT, 
	id_ba INTEGER,
	FOREIGN KEY(id_ba) REFERENCES barrio(id_ba));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS barrio(
	id_ba INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	calle TEXT,
	barrio TEXT,
	id_loc INTEGER,
	FOREIGN KEY(id_loc) REFERENCES localidad(id_loc));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS localidad(
	id_loc INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	localidad TEXT,
	CP INTEGER);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS materias(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	asignatura TEXT,
	id_curso INTEGER,
	FOREIGN KEY(id_curso) REFERENCES curso(id));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS notas(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	calific INTEGER(2));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS curso(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	anio TEXT);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS division(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	seccion TEXT,
	id_curso INTEGER,
	FOREIGN KEY(id_curso) REFERENCES curso(id));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS turno(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	mt TEXT,
	id_curso INTEGER,
	FOREIGN KEY(id_curso) REFERENCES curso(id));""")

# ------------------------------------------------------- #

conexion.execute("""CREATE TABLE IF NOT EXISTS alum_prof(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_alu INTEGER,
	id_prof INTEGER,
	FOREIGN KEY(id_alu) REFERENCES alumnos(id),
	FOREIGN KEY(id_prof) REFERENCES profesores(id));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS alum_mat(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_alu INTEGER,
	id_mat INTEGER,
	FOREIGN KEY(id_alu) REFERENCES alumnos(id),
	FOREIGN KEY(id_mat) REFERENCES materias(id));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS prof_mat(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_prof INTEGER,
	id_mat INTEGER,
	FOREIGN KEY(id_prof) REFERENCES profesores(id),
	FOREIGN KEY(id_mat) REFERENCES materias(id));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS mat_nota(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_mat INTEGER,
	id_nota INTEGER,
	FOREIGN KEY(id_mat) REFERENCES materias(id),
	FOREIGN KEY(id_nota) REFERENCES notas(id));""")

conexion.close()


