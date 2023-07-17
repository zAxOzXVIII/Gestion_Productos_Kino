-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-07-2023 a las 23:55:40
-- Versión del servidor: 10.1.38-MariaDB
-- Versión de PHP: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bienes_muebles`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `id_sesion_admin` int(3) NOT NULL,
  `usuario` varchar(32) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `clave` varchar(16) COLLATE utf8mb4_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id_sesion_admin`, `usuario`, `clave`) VALUES
(1, 'Juan Pibote', '123');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas_trabajo_kino`
--

CREATE TABLE `areas_trabajo_kino` (
  `id_area` int(4) NOT NULL,
  `nombre_area` varchar(42) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `codigo_zona` varchar(42) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `id_supervisor` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `areas_trabajo_kino`
--

INSERT INTO `areas_trabajo_kino` (`id_area`, `nombre_area`, `codigo_zona`, `id_supervisor`) VALUES
(1, 'Talento Humano', 'P5C6', 1),
(2, 'Publicidad', 'P2C1', 2),
(3, 'Gerencia Publica', 'P4C2', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bienes_por_zona`
--

CREATE TABLE `bienes_por_zona` (
  `id_bienes` int(4) NOT NULL,
  `id_area` int(4) NOT NULL,
  `cantidad` int(4) NOT NULL,
  `num_cons` int(6) NOT NULL,
  `desc_item` varchar(64) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `valor` float NOT NULL,
  `observacion` varchar(42) COLLATE utf8mb4_spanish2_ci DEFAULT NULL,
  `codigo_qr` varchar(25) COLLATE utf8mb4_spanish2_ci NOT NULL COMMENT 'Columna que servira para guardar el codigo QR, para busquedas'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `bienes_por_zona`
--

INSERT INTO `bienes_por_zona` (`id_bienes`, `id_area`, `cantidad`, `num_cons`, `desc_item`, `valor`, `observacion`, `codigo_qr`) VALUES
(1, 1, 32, 3044, 'Mouse marca logitech', 10.5, 'En uso', ''),
(2, 1, 44, 2124, 'Silla marca chair', 5.9, 'En uso', ''),
(3, 1, 12, 3231, 'Mesa marca table', 7, 'En uso', ''),
(4, 1, 4, 2369, 'Alfombra marca Luigi', 25.5, 'En desuso', ''),
(5, 1, 16, 2534, 'Impresora marca tintaTruco', 50.5, 'En uso', ''),
(6, 2, 32, 4324, 'Mouse marca logitech', 10.5, 'En uso', ''),
(7, 2, 44, 4341, 'Silla marca chair', 5.9, 'En uso', ''),
(8, 2, 12, 4312, 'Mesa marca table', 7, 'En uso', ''),
(9, 2, 4, 4223, 'Alfombra marca Luigi', 25.5, 'En desuso', ''),
(10, 2, 16, 4124, 'Impresora marca tintaTruco', 50.5, 'En uso', ''),
(11, 3, 32, 1243, 'Mouse marca logitech', 10.5, 'En uso', 'ID_B11NM_C1243C32V10.5'),
(12, 3, 44, 1222, 'Silla marca chair', 5.9, 'En uso', 'ID_B12NM_C1222C44V5.9'),
(13, 3, 12, 1422, 'Mesa marca table', 7, 'En uso', 'ID_B13NM_C1422C12V7.0'),
(14, 3, 4, 1112, 'Alfombra marca Luigi', 25.5, 'En desuso', ''),
(15, 3, 16, 1000, 'Impresora marca tintaTruco', 50.5, 'En uso', ''),
(16, 1, 40, 3033, 'Zapato Tactico', 11, 'En uso', 'ID_B16NM_C3033C40V11.0'),
(17, 1, 45, 3042, 'Luna de caramelo', 12.5, 'En uso', 'ID_B17NM_C3042C45V12.5'),
(18, 1, 34, 3332, 'Silla Gamer', 20.5, 'En uso', ''),
(19, 1, 43, 4443, 'Silla Gamer', 20.5, 'En uso', ''),
(20, 1, 32, 4443, 'Gato rip', 20, 'en desuso', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `movimientos_bienes_muebles`
--

CREATE TABLE `movimientos_bienes_muebles` (
  `id_movimiento` int(4) NOT NULL,
  `id_area` int(4) NOT NULL,
  `concepto_movimiento` varchar(48) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `cantidad` int(4) NOT NULL,
  `id_bienes` int(4) NOT NULL,
  `descripcion_movimiento` varchar(128) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `incorporaciones` float DEFAULT NULL,
  `desincorporaciones` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal_laborando`
--

CREATE TABLE `personal_laborando` (
  `id_persona` int(4) NOT NULL,
  `nombre` varchar(42) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `apellido` varchar(42) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `cedula` varchar(9) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `id_area` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `personal_laborando`
--

INSERT INTO `personal_laborando` (`id_persona`, `nombre`, `apellido`, `cedula`, `fecha_nacimiento`, `id_area`) VALUES
(1, 'Juan Arc', 'Federico Mesa', '24423245', '1999-02-21', 1),
(2, 'Rodrigo A.', 'Piso Liso', '24411145', '1998-02-20', 1),
(4, 'Susan M.', 'Boldin Gacela', '29213245', '2010-12-21', 2),
(5, 'Rubert D.', 'Ancor Char', '19342245', '1999-02-01', 2),
(6, 'Dimitre Maximof', 'Almendra Dittsh', '92555543', '1996-05-04', 3),
(8, 'Juan', 'Miguelangel', '293421542', '2000-07-19', 3),
(10, 'Rodrigo', 'Suarez', '12455221', '2020-07-15', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supervisor_area_kino`
--

CREATE TABLE `supervisor_area_kino` (
  `id_supervisor` int(4) NOT NULL,
  `nombre` varchar(42) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `apellido` varchar(32) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `cedula` varchar(9) COLLATE utf8mb4_spanish2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `supervisor_area_kino`
--

INSERT INTO `supervisor_area_kino` (`id_supervisor`, `nombre`, `apellido`, `cedula`) VALUES
(1, 'Pacho Andres', 'Rodriguez Buena', '19453254'),
(2, 'Andrea Carolina', 'Montilva Mesa', '20453542'),
(7, 'Perro Laser', 'Moto Laser', '33251'),
(8, 'El Xocas', 'Is There', '666666');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supervisor_sesion`
--

CREATE TABLE `supervisor_sesion` (
  `id_sesion` int(4) NOT NULL,
  `clave_sup` varchar(16) COLLATE utf8mb4_spanish2_ci NOT NULL,
  `id_supervisor` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `supervisor_sesion`
--

INSERT INTO `supervisor_sesion` (`id_sesion`, `clave_sup`, `id_supervisor`) VALUES
(1, '123', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id_sesion_admin`);

--
-- Indices de la tabla `areas_trabajo_kino`
--
ALTER TABLE `areas_trabajo_kino`
  ADD PRIMARY KEY (`id_area`),
  ADD KEY `id_supervisor` (`id_supervisor`);

--
-- Indices de la tabla `bienes_por_zona`
--
ALTER TABLE `bienes_por_zona`
  ADD PRIMARY KEY (`id_bienes`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `movimientos_bienes_muebles`
--
ALTER TABLE `movimientos_bienes_muebles`
  ADD PRIMARY KEY (`id_movimiento`),
  ADD KEY `id_area` (`id_area`),
  ADD KEY `id_bienes` (`id_bienes`);

--
-- Indices de la tabla `personal_laborando`
--
ALTER TABLE `personal_laborando`
  ADD PRIMARY KEY (`id_persona`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `supervisor_area_kino`
--
ALTER TABLE `supervisor_area_kino`
  ADD PRIMARY KEY (`id_supervisor`);

--
-- Indices de la tabla `supervisor_sesion`
--
ALTER TABLE `supervisor_sesion`
  ADD PRIMARY KEY (`id_sesion`),
  ADD KEY `id_supervisor` (`id_supervisor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id_sesion_admin` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `areas_trabajo_kino`
--
ALTER TABLE `areas_trabajo_kino`
  MODIFY `id_area` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `bienes_por_zona`
--
ALTER TABLE `bienes_por_zona`
  MODIFY `id_bienes` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `movimientos_bienes_muebles`
--
ALTER TABLE `movimientos_bienes_muebles`
  MODIFY `id_movimiento` int(4) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `personal_laborando`
--
ALTER TABLE `personal_laborando`
  MODIFY `id_persona` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `supervisor_area_kino`
--
ALTER TABLE `supervisor_area_kino`
  MODIFY `id_supervisor` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `supervisor_sesion`
--
ALTER TABLE `supervisor_sesion`
  MODIFY `id_sesion` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `areas_trabajo_kino`
--
ALTER TABLE `areas_trabajo_kino`
  ADD CONSTRAINT `areas_trabajo_kino_ibfk_1` FOREIGN KEY (`id_supervisor`) REFERENCES `supervisor_area_kino` (`id_supervisor`);

--
-- Filtros para la tabla `bienes_por_zona`
--
ALTER TABLE `bienes_por_zona`
  ADD CONSTRAINT `bienes_por_zona_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `areas_trabajo_kino` (`id_area`);

--
-- Filtros para la tabla `movimientos_bienes_muebles`
--
ALTER TABLE `movimientos_bienes_muebles`
  ADD CONSTRAINT `movimientos_bienes_muebles_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `areas_trabajo_kino` (`id_area`),
  ADD CONSTRAINT `movimientos_bienes_muebles_ibfk_2` FOREIGN KEY (`id_bienes`) REFERENCES `bienes_por_zona` (`id_bienes`);

--
-- Filtros para la tabla `personal_laborando`
--
ALTER TABLE `personal_laborando`
  ADD CONSTRAINT `personal_laborando_ibfk_1` FOREIGN KEY (`id_area`) REFERENCES `areas_trabajo_kino` (`id_area`);

--
-- Filtros para la tabla `supervisor_sesion`
--
ALTER TABLE `supervisor_sesion`
  ADD CONSTRAINT `supervisor_sesion_ibfk_1` FOREIGN KEY (`id_supervisor`) REFERENCES `supervisor_area_kino` (`id_supervisor`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
