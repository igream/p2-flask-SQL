-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 04, 2024 at 07:41 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gimnasio`
--

-- --------------------------------------------------------

--
-- Table structure for table `administradores`
--

CREATE TABLE `administradores` (
  `ID_Admin` int(11) NOT NULL,
  `User` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `administradores`
--

INSERT INTO `administradores` (`ID_Admin`, `User`, `Password`) VALUES
(4, 'admin', 'scrypt:32768:8:1$z5CvXfGw7gFOTErd$66aa36e5bcbc1e05dae96a9cca5c23f8f47148e0a6e8d4eb8d976993746d6c4d4cc208ae0343bbd666f0510e5b0371417f20ddc898ffab95aac3c32afbed313c'),
(5, 'admin1', 'scrypt:32768:8:1$q93DCDEwXXElY5eb$c29828c4243f2a3c05dd0cd37fab1a7fb03edd1b6d97e0d9495746b73d25cfb4b8b2ef7a53e351b25211a06ce56210597eaf0d9774444af66846ac2ed0a327d9'),
(6, 'ProfeTeja', 'scrypt:32768:8:1$qTzLMurcFkfV73zg$bba70dcdeeac84b8b7c1f33313893df87c85bd8d39b37b7bd5891deda802d76456330dd66f843954599d2b906abd91aebda5da61ee746a83f9f745406e233bb9'),
(7, 'FernandoAdmin', 'scrypt:32768:8:1$jNESgLGq5ybxWUgM$7f304ba5a8062697185703fdc3d784bc6893cc041e5e9e2f048662c22543a690d72f8b00c4ee503d4174f00c34b0157eb364ed06ca76319329d96645fb0ed830');

-- --------------------------------------------------------

--
-- Table structure for table `clases`
--

CREATE TABLE `clases` (
  `ID_Clase` int(11) NOT NULL,
  `Nombre_Clase` varchar(50) NOT NULL,
  `Descripcion` text DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Capacidad` int(11) NOT NULL,
  `Imagen` varchar(255) DEFAULT NULL,
  `ID_Personal` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clases`
--

INSERT INTO `clases` (`ID_Clase`, `Nombre_Clase`, `Descripcion`, `Hora`, `Capacidad`, `Imagen`, `ID_Personal`) VALUES
(7, 'Ejercicio Aerobico', 'El ejercicio aeróbrazón y promueve niveles de colesterol saludables. Entre los aeróbicos de bajo impacto están el caminar y nadar. Correr, jugar tenis y bailar son aeróbicos de alto impacto.', '22:00:00', 3, 'uploads/aerobico.jpg', 4),
(8, 'Entrenamiento de Fuerza', 'Es una rutina deportiva que busca fortalecer los músculos del cuerpo. Para ello, se utilizan distintos métodos de resistencia, como pesas, máquinas, bandas elásticas o el propio peso del cuerpo.', '23:00:00', 10, 'uploads/fuerza.jpg', 11),
(9, 'Entrenamiento de Atrofia Muscular', 'El entrenamiento físico puede ayudar a tratar la atrofia muscular, que es la disminución de la masa muscular y el desgaste de los tejidos musculares.', '22:14:00', 5, 'uploads/atrofia.jpg', 7),
(12, 'Militar', 'Entrenamiento Militar', '01:46:00', 20, 'uploads/rambo.jpg', 6),
(13, 'Zumba', 'Danza de zumba', '15:08:00', 5, 'uploads/clase1.jpg', 6);

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `ID_Cliente` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  `Telefono` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `Direccion` varchar(150) DEFAULT NULL,
  `Fecha_Registro` date NOT NULL DEFAULT curdate(),
  `Imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`ID_Cliente`, `Nombre`, `Apellido`, `Fecha_Nacimiento`, `Telefono`, `Email`, `password`, `Direccion`, `Fecha_Registro`, `Imagen`) VALUES
(17, 'Fernando', 'Azuara Ibarra', '2005-03-06', '7122411716', 'ferazuiba@gmail.com', 'fer123', 'San Felipe del Progreso', '2024-11-24', 'clientes/fer.jpg'),
(18, 'Jiovani Asael', 'Tapia López', '2005-02-03', '919238912', 'Asael@gmail.com', 'asael123', 'Santiago Casandeje', '2024-11-24', 'clientes/asael.jpg'),
(19, 'Omar Aldrei', 'García López', '2005-02-09', '9812893123', 'omar@gmail.com', 'omar123', 'Atlacomulco', '2024-11-24', 'clientes/omar.jpg'),
(20, 'Jenifer', 'Ramírez Ibarra', '2005-02-02', '901203921', 'jeni@gmail.com', 'jeni123', 'Atlacomulco', '2024-11-24', 'clientes/jeni.jpg'),
(21, 'Oswaldo', 'Plata Navarrete', '2005-09-09', '912893212', 'oswaldo@gmail.com', 'oswaldo123', 'Atlacomulco', '2024-11-24', 'clientes/oswaldo.jpg'),
(22, 'Ricardo', 'Anaya', '2024-11-06', '97983217983', 'ricardo@gmail.com', 'ricardo123', 'El Cielo', '2024-11-24', 'clientes/ricardo.jpg'),
(23, 'Rambo', 'Rambosio', '2002-01-01', '17412312', 'rambo@gmail.com', 'rambo123', 'Ucrania', '2024-11-24', 'clientes/rambo.jpg'),
(24, 'Gigachad', 'Apellido', '2024-10-30', '1231', 'giga@gmail.com', 'giga123', 'Cielo', '2024-11-25', 'clientes/yo.jpg'),
(26, 'prueba2', 'apellido2', '2024-11-07', '17412312', 'prueba2@gmail.com', 'prueba2123', 'Narnia', '2024-11-25', 'clientes/Sin_titulo.png'),
(29, 'Nuevo Usuario', 'Apellido Usuario', '1920-03-03', '9918298312', 'NewUser@gmail.com', 'usuario123', 'Palmillas', '2024-11-26', 'clientes/3577429.png');

-- --------------------------------------------------------

--
-- Table structure for table `inscripciones`
--

CREATE TABLE `inscripciones` (
  `ID_Inscripcion` int(11) NOT NULL,
  `ID_Clase` int(11) NOT NULL,
  `ID_Cliente` int(11) NOT NULL,
  `Fecha_Inscripcion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inscripciones`
--

INSERT INTO `inscripciones` (`ID_Inscripcion`, `ID_Clase`, `ID_Cliente`, `Fecha_Inscripcion`) VALUES
(4, 7, 17, '2024-12-03 00:16:50'),
(5, 7, 20, '2024-12-03 00:19:57'),
(6, 7, 19, '2024-12-03 00:20:34');

-- --------------------------------------------------------

--
-- Table structure for table `membresias`
--

CREATE TABLE `membresias` (
  `ID_Membresia` int(11) NOT NULL,
  `Tipo` varchar(50) NOT NULL,
  `Costo` decimal(10,2) NOT NULL,
  `Duracion` int(11) NOT NULL,
  `Descripcion` text DEFAULT NULL,
  `Imagen` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `membresias`
--

INSERT INTO `membresias` (`ID_Membresia`, `Tipo`, `Costo`, `Duracion`, `Descripcion`, `Imagen`) VALUES
(1, 'Carbones', 400.00, 40, 'Acceso a las instalaciones tiempo completo', 'uploads/carbon.jpg'),
(2, 'Hierro', 800.00, 30, 'Carbon + Entrenamientos con proteina incluida', 'uploads/hierro.jpg'),
(4, 'Oros', 12020.00, 30, 'Hierro + Instructor personal', 'uploads/oro.jpg'),
(6, 'Diamante', 1600.00, 30, 'Oro + Nutriologo Incluido', 'uploads/diamante.jpg'),
(7, 'Super Carbón', 2000.00, 180, 'Semestre de beneficios carbón', 'uploads/bloquecarbon.jpg'),
(8, 'Super Hierro', 4000.00, 180, 'Semestre de beneficios Hierro', 'uploads/bloquehierro.jpg'),
(10, 'Super Diamante', 8000.00, 180, 'Semestre de beneficios diamante', 'uploads/bloquediamante.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `membresias_clases`
--

CREATE TABLE `membresias_clases` (
  `ID_Membresia` int(11) NOT NULL,
  `ID_Clase` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `membresias_clases`
--

INSERT INTO `membresias_clases` (`ID_Membresia`, `ID_Clase`) VALUES
(1, 12),
(1, 13),
(2, 9),
(2, 12),
(6, 9),
(8, 7);

-- --------------------------------------------------------

--
-- Table structure for table `pagos`
--

CREATE TABLE `pagos` (
  `ID_Pago` int(11) NOT NULL,
  `ID_Cliente` int(11) DEFAULT NULL,
  `ID_Membresia` int(11) DEFAULT NULL,
  `Fecha_Pago` date NOT NULL DEFAULT curdate(),
  `Monto` decimal(10,2) NOT NULL,
  `Metodo_Pago` varchar(50) DEFAULT NULL,
  `Estado` enum('Pendiente','Pagado','Vencido') NOT NULL DEFAULT 'Pendiente',
  `Referencia` varchar(100) NOT NULL,
  `Estado_Membresia` enum('Inactivo','Activo','Validado') NOT NULL DEFAULT 'Inactivo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pagos`
--

INSERT INTO `pagos` (`ID_Pago`, `ID_Cliente`, `ID_Membresia`, `Fecha_Pago`, `Monto`, `Metodo_Pago`, `Estado`, `Referencia`, `Estado_Membresia`) VALUES
(14, 18, 1, '2024-11-25', 400.00, 'Efectivo', 'Pagado', 'e70316f5c1', 'Validado'),
(24, 17, 8, '2024-11-25', 4000.00, 'Tarjeta de Debito', 'Pagado', '7232f49335', 'Activo'),
(25, 19, 1, '2024-11-25', 400.00, 'Efectivo', 'Pagado', '80d3a39e26', 'Inactivo'),
(26, 19, 2, '2024-11-25', 800.00, 'Efectivo', 'Pagado', 'f9ce2cb2bd', 'Validado'),
(27, 17, 10, '2024-11-25', 8000.00, 'Efectivo', 'Pagado', '503fcd2eec', 'Validado'),
(29, 20, 1, '2024-11-26', 400.00, 'Efectivo', 'Vencido', '7be3db69c7', 'Inactivo'),
(30, 29, 2, '2024-11-26', 800.00, 'Tarjeta de Debito', 'Pagado', '5b82548291', 'Activo'),
(31, 29, 10, '2024-11-26', 8000.00, 'Efectivo', 'Pagado', '14946549a8', 'Validado'),
(32, 19, 8, '2024-12-02', 4000.00, 'Efectivo', 'Pagado', 'c81fcc946b', 'Activo'),
(33, 20, 8, '2024-12-02', 4000.00, 'Efectivo', 'Pagado', '276d4363d6', 'Activo'),
(34, 21, 8, '2024-12-02', 4000.00, 'Efectivo', 'Pagado', '75fedc9e42', 'Activo'),
(35, 17, 8, '2024-12-04', 4000.00, 'Efectivo', 'Pagado', '046f9252f4', 'Inactivo');

-- --------------------------------------------------------

--
-- Table structure for table `personal`
--

CREATE TABLE `personal` (
  `ID_Personal` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Puesto` varchar(50) NOT NULL,
  `Salario` decimal(10,2) NOT NULL,
  `Antiguedad` int(11) DEFAULT NULL,
  `Turno` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `personal`
--

INSERT INTO `personal` (`ID_Personal`, `Nombre`, `Puesto`, `Salario`, `Antiguedad`, `Turno`) VALUES
(2, 'Calamardo Tentaculos', 'Cajero', 5000.00, 12, 'Matutino'),
(3, 'Levi Hackerman', 'Conserje', 14123.00, 15, 'Vespertino'),
(4, 'Baki Hanma', 'Entrenador', 10000.00, 3, 'Matutino'),
(5, 'Alma Marcela Gozo', 'Entrenador', 15000.00, 2, 'Matutino'),
(6, 'Samuel del Luque', 'Entrenador', 13000.00, 24, 'Vespertino'),
(7, 'Alan Brito', 'Entrenador', 10000.00, 12, 'Vespertino'),
(8, 'Octavio Paz', 'Mantenimiento', 5000.00, 12, 'Matutino'),
(9, 'Nombre Entrenador', 'Entrenador', 2000.00, 29, 'Matutino'),
(10, 'Personal Mantenimiento', 'Mantenimiento', 2000.00, 23, 'Matutino'),
(11, 'Entrenador Nuevo', 'Entrenador', 9000.00, 20, 'Vespertino');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`ID_Admin`);

--
-- Indexes for table `clases`
--
ALTER TABLE `clases`
  ADD PRIMARY KEY (`ID_Clase`),
  ADD KEY `fk_personal` (`ID_Personal`);

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`ID_Cliente`);

--
-- Indexes for table `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD PRIMARY KEY (`ID_Inscripcion`),
  ADD KEY `ID_Clase` (`ID_Clase`),
  ADD KEY `ID_Cliente` (`ID_Cliente`);

--
-- Indexes for table `membresias`
--
ALTER TABLE `membresias`
  ADD PRIMARY KEY (`ID_Membresia`);

--
-- Indexes for table `membresias_clases`
--
ALTER TABLE `membresias_clases`
  ADD PRIMARY KEY (`ID_Membresia`,`ID_Clase`),
  ADD KEY `ID_Clase` (`ID_Clase`);

--
-- Indexes for table `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`ID_Pago`),
  ADD KEY `ID_Cliente` (`ID_Cliente`),
  ADD KEY `ID_Membresia` (`ID_Membresia`);

--
-- Indexes for table `personal`
--
ALTER TABLE `personal`
  ADD PRIMARY KEY (`ID_Personal`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `administradores`
--
ALTER TABLE `administradores`
  MODIFY `ID_Admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `clases`
--
ALTER TABLE `clases`
  MODIFY `ID_Clase` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `ID_Cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `inscripciones`
--
ALTER TABLE `inscripciones`
  MODIFY `ID_Inscripcion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `membresias`
--
ALTER TABLE `membresias`
  MODIFY `ID_Membresia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `pagos`
--
ALTER TABLE `pagos`
  MODIFY `ID_Pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `personal`
--
ALTER TABLE `personal`
  MODIFY `ID_Personal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `clases`
--
ALTER TABLE `clases`
  ADD CONSTRAINT `fk_personal` FOREIGN KEY (`ID_Personal`) REFERENCES `personal` (`ID_Personal`) ON DELETE SET NULL;

--
-- Constraints for table `inscripciones`
--
ALTER TABLE `inscripciones`
  ADD CONSTRAINT `inscripciones_ibfk_1` FOREIGN KEY (`ID_Clase`) REFERENCES `clases` (`ID_Clase`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `inscripciones_ibfk_2` FOREIGN KEY (`ID_Cliente`) REFERENCES `clientes` (`ID_Cliente`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `membresias_clases`
--
ALTER TABLE `membresias_clases`
  ADD CONSTRAINT `membresias_clases_ibfk_1` FOREIGN KEY (`ID_Membresia`) REFERENCES `membresias` (`ID_Membresia`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `membresias_clases_ibfk_2` FOREIGN KEY (`ID_Clase`) REFERENCES `clases` (`ID_Clase`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `clientes` (`ID_Cliente`),
  ADD CONSTRAINT `pagos_ibfk_2` FOREIGN KEY (`ID_Membresia`) REFERENCES `membresias` (`ID_Membresia`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
