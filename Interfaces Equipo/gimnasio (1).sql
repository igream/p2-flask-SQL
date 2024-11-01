-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 01, 2024 at 02:51 AM
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
-- Table structure for table `clases`
--

CREATE TABLE `clases` (
  `ID_Clase` int(11) NOT NULL,
  `Nombre_Clase` varchar(50) NOT NULL,
  `Descripcion` text DEFAULT NULL,
  `Instructor` varchar(50) DEFAULT NULL,
  `Hora` time DEFAULT NULL,
  `Capacidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clases`
--

INSERT INTO `clases` (`ID_Clase`, `Nombre_Clase`, `Descripcion`, `Instructor`, `Hora`, `Capacidad`) VALUES
(1, 'Clase Aerobicas', 'Te mueves mucho', 'Venitocamelas', '16:46:00', 20),
(4, 'iujgjkhsdf', 'safdsfsd', 'Venitocamelas', '21:54:00', 324);

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
  `Direccion` varchar(150) DEFAULT NULL,
  `Fecha_Registro` date NOT NULL DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`ID_Cliente`, `Nombre`, `Apellido`, `Fecha_Nacimiento`, `Telefono`, `Email`, `Direccion`, `Fecha_Registro`) VALUES
(1, 'Fernandos', 'Azuara Ibarra', '2005-03-06', '7122411716', 'ferazuiba@gmail.com', 'San Felipe del Progreso', '2024-10-31'),
(7, 'dsdffa', 'dsfad', '2024-10-08', '17412312', 'sada@gmail.com', 'San Felipe del Progreso', '2024-10-31');

-- --------------------------------------------------------

--
-- Table structure for table `membresias`
--

CREATE TABLE `membresias` (
  `ID_Membresia` int(11) NOT NULL,
  `Tipo` varchar(50) NOT NULL,
  `Costo` decimal(10,2) NOT NULL,
  `Duracion` int(11) NOT NULL,
  `Descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `membresias`
--

INSERT INTO `membresias` (`ID_Membresia`, `Tipo`, `Costo`, `Duracion`, `Descripcion`) VALUES
(1, 'Básica', 400.00, 30, 'Ten acceso a...etc'),
(2, 'Oro', 800.00, 60, 'Pues oro jijijija'),
(4, 'Diamante', 1200.00, 30, 'Todo pa ti');

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
  `Metodo_Pago` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pagos`
--

INSERT INTO `pagos` (`ID_Pago`, `ID_Cliente`, `ID_Membresia`, `Fecha_Pago`, `Monto`, `Metodo_Pago`) VALUES
(3, 1, 1, '2024-10-31', 800.00, 'Tarjeta de Debito');

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
(2, 'Omar Aldrei', 'Entrenador', 5000.00, 12, 'Matutino'),
(3, 'asd', 'Conserje', 14123.00, 12, 'Vespertino');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clases`
--
ALTER TABLE `clases`
  ADD PRIMARY KEY (`ID_Clase`);

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`ID_Cliente`);

--
-- Indexes for table `membresias`
--
ALTER TABLE `membresias`
  ADD PRIMARY KEY (`ID_Membresia`);

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
-- AUTO_INCREMENT for table `clases`
--
ALTER TABLE `clases`
  MODIFY `ID_Clase` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `ID_Cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `membresias`
--
ALTER TABLE `membresias`
  MODIFY `ID_Membresia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `pagos`
--
ALTER TABLE `pagos`
  MODIFY `ID_Pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `personal`
--
ALTER TABLE `personal`
  MODIFY `ID_Personal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

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
