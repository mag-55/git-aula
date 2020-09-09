#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import sqlite3

conexion = sqlite3.connect('escuela.db')

conexion.execute("""CREATE TABLE IF NOT EXISTS alumnos(
	id_alu INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre 	TEXT,
	apellido TEXT,
	dni INTEGER UNIQUE,
	fecha TEXT,
	telefono TEXT,
	mail TEXT,
	modificado TEXT,
	id_ba1 INTEGER,
	id_loc1 INTEGER,
	id_pre1 INTEGER,
	id_curso1 INTEGER,
	FOREIGN KEY(id_curso1) REFERENCES curso(id_curso),
	FOREIGN KEY(id_pre1) REFERENCES preceptores(id_pre),
	FOREIGN KEY(id_loc1) REFERENCES localidad(id_loc),
	FOREIGN KEY(id_ba1) REFERENCES barrio(id_ba));""")
	

conexion.execute("""CREATE TABLE IF NOT EXISTS profesores(
	id_prof INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre TEXT,
	apellido TEXT,
	dni INTEGER UNIQUE,
	fecha TEXT,
	telefono TEXT,
	mail TEXT,
	modificado TEXT,
	id_ba1 INTEGER,
	id_loc1 INTEGER,
	FOREIGN KEY(id_loc1) REFERENCES localidad(id_loc),
	FOREIGN KEY(id_ba1) REFERENCES barrio(id_ba));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS preceptores(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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
	id_loc INTEGER,
	FOREIGN KEY(id_loc) REFERENCES localidad(id),
	FOREIGN KEY(id_ba) REFERENCES barrio(id));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS localidad(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	localidad TEXT,
	CP INTEGER);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS barrio(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	calle TEXT,
	barrio TEXT,
	id_loc INTEGER,
	FOREIGN KEY(id_loc) REFERENCES localidad(id));""")


conexion.execute("""CREATE TABLE IF NOT EXISTS materias(
	id_mat INTEGER PRIMARY KEY AUTOINCREMENT,
	asignatura TEXT,
	id_curso1 INTEGER,
	FOREIGN KEY(id_curso1) REFERENCES curso(id_curso));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS notas(
	id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
	calific INTEGER(2));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS curso(
	id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
	anio TEXT);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS division(
	id_div INTEGER PRIMARY KEY AUTOINCREMENT,
	seccion TEXT,
	id_curso1 INTEGER,
	FOREIGN KEY(id_curso1) REFERENCES curso(id_curso));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS turno(
	id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
	mt TEXT,
	id_curso1 INTEGER,
	FOREIGN KEY(id_curso1) REFERENCES curso(id_curso));""")

# ------------------------------------------------------- #

conexion.execute("""CREATE TABLE IF NOT EXISTS alum_prof(
	id_alum_prof INTEGER PRIMARY KEY AUTOINCREMENT,
	id_alu1 INTEGER,
	id_prof1 INTEGER,
	FOREIGN KEY(id_alu1) REFERENCES alumnos(id_alu),
	FOREIGN KEY(id_prof1) REFERENCES profesores(id_prof));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS alum_mat(
	id_alum_mat INTEGER PRIMARY KEY AUTOINCREMENT,
	id_alu1 INTEGER,
	id_mat1 INTEGER,
	FOREIGN KEY(id_alu1) REFERENCES alumnos(id_alu),
	FOREIGN KEY(id_mat1) REFERENCES materias(id_mat));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS prof_mat(
	id_prof_mat INTEGER PRIMARY KEY AUTOINCREMENT,
	id_prof1 INTEGER,
	id_mat1 INTEGER,
	FOREIGN KEY(id_prof1) REFERENCES profesores(id_prof),
	FOREIGN KEY(id_mat1) REFERENCES materias(id_mat));""")

conexion.execute("""CREATE TABLE IF NOT EXISTS mat_nota(
	id_mat_nota INTEGER PRIMARY KEY AUTOINCREMENT,
	id_mat1 INTEGER,
	id_nota1 INTEGER,
	FOREIGN KEY(id_mat1) REFERENCES materias(id_mat),
	FOREIGN KEY(id_nota1) REFERENCES notas(id_nota));""")

conexion.close()


