#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sqlite3

# Conexión a la base de datos
conexion = sqlite3.connect('escuela_ok.db')

# ------------ Tablas de union --------------------

conexion.execute("""CREATE TABLE IF NOT EXISTS mat_nota (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_mat INTEGER,
	id_nota INTEGER,
	id_per INTEGER,
	FOREIGN KEY(id_mat) REFERENCES materias(id),
	FOREIGN KEY(id_nota) REFERENCES notas(id),
	FOREIGN KEY(id_per) REFERENCES personas(id) ON DELETE CASCADE
	);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS curso_division_turno (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_cur INTEGER,
	id_div INTEGER,
	id_tur INTEGER,
	id_per INTEGER,
	FOREIGN KEY(id_div) REFERENCES division(id),
	FOREIGN KEY(id_cur) REFERENCES curso(id),
	FOREIGN KEY(id_tur) REFERENCES turno(id),
	FOREIGN KEY(id_per) REFERENCES personas(id) ON DELETE CASCADE
	);""")

# ------------ Datos de contraseñas --------------------

conexion.execute("""CREATE TABLE IF NOT EXISTS contraseña (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	usuario TEXT UNIQUE,
	clave TEXT UNIQUE,
	conf_clave TEXT UNIQUE,
	id_per INTEGER, 
	FOREIGN KEY(id_per) REFERENCES personas(id) ON DELETE CASCADE
	);""")

# ------------ Datos de personales --------------------

conexion.execute("""CREATE TABLE IF NOT EXISTS personas (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre 	TEXT,
	apellido TEXT,
	dni INTEGER UNIQUE NOT NULL,
	fecha TEXT,
	telefono TEXT,
	mail TEXT,
	actividad TEXT
	);""")

# ------------ Datos de ubicacion --------------------

conexion.execute("""CREATE TABLE IF NOT EXISTS barrio (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	calle TEXT,
	barrio TEXT,
	id_per INTEGER,
	FOREIGN KEY(id_per) REFERENCES personas(id) ON DELETE CASCADE
	);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS localidad(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	localidad TEXT,
	CP INTEGER,
	id_ba INTEGER,
	FOREIGN KEY(id_ba) REFERENCES barrio(id) ON DELETE CASCADE
	);""")

# ------------ Datos de Cursado --------------------

conexion.execute("""CREATE TABLE IF NOT EXISTS materias (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	asignatura TEXT,
	id_cur INTEGER,
	FOREIGN KEY(id_cur) REFERENCES curso(id)
	);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS notas (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	calific INTEGER(2)
	);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS division (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	seccion TEXT
	);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS curso (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	anio TEXT
	);""")

conexion.execute("""CREATE TABLE IF NOT EXISTS turno (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	mt TEXT
	);""")

conexion.close()




