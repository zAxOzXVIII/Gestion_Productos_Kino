CREATE DATABASE Bienes_Muebles CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish2_ci;

USE Bienes_Muebles;

CREATE TABLE Bienes_Muebles.supervisor_area_kino(
	id_supervisor INT(4) AUTO_INCREMENT NOT NULL,
	nombre VARCHAR(42) NOT NULL,
	apellido VARCHAR(32) NOT NULL,
	cedula VARCHAR(9) NOT NULL,
	PRIMARY KEY(id_supervisor)
);

CREATE TABLE Bienes_Muebles.areas_trabajo_kino(
	id_area INT(4) AUTO_INCREMENT NOT NULL,
	nombre_area VARCHAR(42) NOT NULL,
	codigo_zona VARCHAR(42) NOT NULL,
	id_supervisor INT(4) NOT NULL,
	PRIMARY KEY(id_area),
	FOREIGN KEY(id_supervisor) REFERENCES Bienes_Muebles.supervisor_area_kino(id_supervisor)
);

CREATE TABLE Bienes_Muebles.personal_laborando(
	id_persona INT(4) AUTO_INCREMENT NOT NULL,
	nombre VARCHAR(42) NOT NULL,
	apellido VARCHAR(42) NOT NULL,
	cedula VARCHAR(9) NOT NULL,
	fecha_nacimiento DATE NOT NULL,
	id_area INT(4) NOT NULL,
	PRIMARY KEY(id_persona),
	FOREIGN KEY(id_area) REFERENCES Bienes_Muebles.areas_trabajo_kino(id_area)
);

CREATE TABLE Bienes_Muebles.bienes_por_zona(
	id_bienes INT(4) NOT NULL AUTO_INCREMENT,
	id_area INT(4) NOT NULL,
	cantidad INT(4) NOT NULL,
	num_cons INT(6) NOT NULL,
	desc_item VARCHAR(64) NOT NULL,
	valor FLOAT(6) NOT NULL,
	observacion VARCHAR(42),
	PRIMARY KEY(id_bienes),
	FOREIGN KEY(id_area) REFERENCES Bienes_Muebles.areas_trabajo_kino(id_area)
);

CREATE TABLE Bienes_Muebles.movimientos_bienes_muebles(
	id_movimiento INT(4) NOT NULL AUTO_INCREMENT,
	id_area INT(4) NOT NULL,
	concepto_movimiento VARCHAR(48) NOT NULL,
	cantidad INT(4) NOT NULL,
	id_bienes INT(4) NOT NULL,
	descripcion_movimiento VARCHAR(128) NOT NULL,
	incorporaciones FLOAT(9),
	desincorporaciones FLOAT(9),
	PRIMARY KEY(id_movimiento),
	FOREIGN KEY(id_area) REFERENCES Bienes_Muebles.areas_trabajo_kino(id_area),
	FOREIGN KEY(id_bienes) REFERENCES Bienes_Muebles.bienes_por_zona(id_bienes)
);

CREATE TABLE Bienes_Muebles.supervisor_sesion(
	id_sesion INT(4) NOT NULL AUTO_INCREMENT,
	clave_sup VARCHAR(16) NOT NULL,
	id_supervisor INT(4) NOT NULL,
	PRIMARY KEY(id_sesion),
	FOREIGN KEY(id_supervisor) REFERENCES Bienes_Muebles.supervisor_area_kino(id_supervisor)
);

CREATE TABLE Bienes_Muebles.administrador(
	id_sesion_admin INT(3) NOT NULL AUTO_INCREMENT,
	usuario VARCHAR(32) NOT NULL,
	clave VARCHAR(16) NOT NULL,
	PRIMARY KEY(id_sesion_admin)
);

-- añadiendo tabla qr
ALTER TABLE Bienes_Muebles.bienes_por_zona ADD codigo_qr VARCHAR(25) COMMIT 'Columna que servira para guardar el codigo QR, para busquedas';

/*Inyeccion de datos */

INSERT INTO Bienes_Muebles.supervisor_area_kino(nombre, apellido, cedula) 
VALUES('Pacho Andres', 'Rodriguez Buena', '19453254'),
	('Andrea Carolina', 'Montilva Mesa', '20453542');

INSERT INTO Bienes_Muebles.areas_trabajo_kino(nombre_area, codigo_zona, id_supervisor) 
VALUES ('Talento Humano', 'P5C6', 1),
	('Publicidad', 'P2C1', 2),
	('Gerencia Publica', 'P4C2', 1);
/* Bienes */
INSERT INTO Bienes_Muebles.bienes_por_zona(id_area, cantidad, num_cons, desc_item, valor, observacion) 
VALUES (1, 32, 3044, 'Mouse marca logitech', 10.5, 'En uso'),
	   (1, 44, 2124, 'Silla marca chair', 5.9, 'En uso'),
	   (1, 12, 3231, 'Mesa marca table', 7.0, 'En uso'),
	   (1, 4, 2369, 'Alfombra marca Luigi', 25.5, 'En desuso'),
	   (1, 16, 2534, 'Impresora marca tintaTruco', 50.5, 'En uso');

INSERT INTO Bienes_Muebles.bienes_por_zona(id_area, cantidad, num_cons, desc_item, valor, observacion) 
VALUES (2, 32, 4324, 'Mouse marca logitech', 10.5, 'En uso'),
	   (2, 44, 4341, 'Silla marca chair', 5.9, 'En uso'),
	   (2, 12, 4312, 'Mesa marca table', 7.0, 'En uso'),
	   (2, 4, 4223, 'Alfombra marca Luigi', 25.5, 'En desuso'),
	   (2, 16, 4124, 'Impresora marca tintaTruco', 50.5, 'En uso');

INSERT INTO Bienes_Muebles.bienes_por_zona(id_area, cantidad, num_cons, desc_item, valor, observacion) 
VALUES (3, 32, 1243, 'Mouse marca logitech', 10.5, 'En uso'),
	   (3, 44, 1222, 'Silla marca chair', 5.9, 'En uso'),
	   (3, 12, 1422, 'Mesa marca table', 7.0, 'En uso'),
	   (3, 4, 1112, 'Alfombra marca Luigi', 25.5, 'En desuso'),
	   (3, 16, 1000, 'Impresora marca tintaTruco', 50.5, 'En uso');
/* Personal */
INSERT INTO Bienes_Muebles.personal_laborando(nombre, apellido, cedula, fecha_nacimiento, id_area) 
VALUES ('Juan Arc', 'Federico Mesa', '24423245', '1999-02-21', 1),
		('Rodrigo A.', 'Piso Liso', '24411145', '1998-02-20', 1),
		('Samanta D.', 'Buena Mocha', '21999245', '2000-01-11', 1),
		('Susan M.', 'Boldin Gacela', '29213245', '2010-12-21', 2),
		('Rubert D.', 'Ancor Char', '19342245', '1999-02-01', 2),
		('Dimitre Maximof', 'Almendra Dittsh', '92555543', '1996-05-04', 3);
/* sesiones */
INSERT INTO Bienes_Muebles.supervisor_sesion(clave_sup, id_supervisor)
VALUES ('Tronco_Tactico', 1);

INSERT INTO Bienes_Muebles.administrador(usuario, clave) 
VALUES ('Juan Pibote', 'Tu_NaranjaX4');

