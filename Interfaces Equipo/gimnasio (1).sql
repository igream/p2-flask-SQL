-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 26, 2024 at 07:03 AM
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
(6, 'ProfeTeja', 'scrypt:32768:8:1$qTzLMurcFkfV73zg$bba70dcdeeac84b8b7c1f33313893df87c85bd8d39b37b7bd5891deda802d76456330dd66f843954599d2b906abd91aebda5da61ee746a83f9f745406e233bb9');

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
(7, 'Ejercicio Aerobico', 'El ejercicio aeróbrazón y promueve niveles de colesterol saludables. Entre los aeróbicos de bajo impacto están el caminar y nadar. Correr, jugar tenis y bailar son aeróbicos de alto impacto.', '22:00:00', 20, 'uploads/aerobico.jpg', 4),
(8, 'Entrenamiento de Fuerza', 'Es una rutina deportiva que busca fortalecer los músculos del cuerpo. Para ello, se utilizan distintos métodos de resistencia, como pesas, máquinas, bandas elásticas o el propio peso del cuerpo.', '23:00:00', 10, 'uploads/fuerza.jpg', NULL),
(9, 'Entrenamiento de Atrofia Muscular', 'El entrenamiento físico puede ayudar a tratar la atrofia muscular, que es la disminución de la masa muscular y el desgaste de los tejidos musculares.', '22:14:00', 5, 'uploads/atrofia.jpg', 7),
(12, 'asdsa', 'asdsadasdsads', '11:46:00', 4, 'uploads/rambo.jpg', 5);

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
(17, 'Fernando', 'Azuara Ibarra', '2005-03-06', '7122411716', 'ferazuiba@gmail.com', 'scrypt:32768:8:1$6DtBJ1VK3tmPPVp4$f6dba501e1d45843e5509ea6ada53eee559263985f7829bf2291fc5c8a6f6f0e496ee1a1930df047e4cdddf932177ceb9defd82ba17e47377437f78d976b0b18', 'San Felipe del Progreso', '2024-11-24', 'clientes/fer.jpg'),
(18, 'Jiovani Asael', 'Tapia López', '2005-02-03', '919238912', 'Asael@gmail.com', 'scrypt:32768:8:1$OiaOMGY3SQRt2yB4$3448ae89f7d6b21cc6fd158eaf643e943a201146ba792671d018cdec49a1b3b62aa5129bb9315c3a3d7328effe1cc275f757271839f656247adf36894be18c86', 'Santiago Casandeje', '2024-11-24', 'clientes/asael.jpg'),
(19, 'Omar Aldrei', 'García López', '2005-02-09', '9812893123', 'omar@gmail.com', 'scrypt:32768:8:1$oQtodj3utDlThk6J$abaaf9e2956b043f24a9e57445b8410f9d236412fb26bdba8158920f5b01a2a8ac9ca0ae73476dcf9702f57fbafbe176d2307452af1a3c3028415041db8d0cb2', 'Atlacomulco', '2024-11-24', 'clientes/omar.jpg'),
(20, 'Jenifer', 'Ramírez Ibarra', '2005-02-02', '901203921', 'jeni@gmail.com', 'scrypt:32768:8:1$V6rA3XbVei21JlV4$9d13aaac492358dc433199a122804ef021739ddb5c1834a12ba439ecd49186719d7e0bb78c6374baa8d1d3d0cb1c3ae9ad1fe0cd8ccfb1d70b58bef967eda705', 'Atlacomulco', '2024-11-24', 'clientes/jeni.jpg'),
(21, 'Oswaldo', 'Plata Navarrete', '2005-09-09', '912893212', 'oswaldo@gmail.com', 'scrypt:32768:8:1$rV6hd5wKCfzavSWN$71987c274559efc8e424ce49542158cbdc81137e1c29e1e4879e1303931758ed8007212148554de6bf243a798a361f7b240a82670f3ce007c3a1c20956282aff', 'Atlacomulco', '2024-11-24', 'clientes/oswaldo.jpg'),
(22, 'Ricardo', 'Anaya', '2024-11-06', '97983217983', 'ricardo@gmail.com', 'scrypt:32768:8:1$UIxakQIflXaUnvQd$4c9f5ef316cd8c9f16826e13b1497398fc54150dfcbcbe7f2f0bb0ae09e8182c9eed3bb151de3d0cf795e4107075251405f8fac6e9f5f4ef7f80184b6e36cc9f', 'El Cielo', '2024-11-24', 'clientes/ricardo.jpg'),
(23, 'Rambo', 'Rambosio', '2002-01-01', '17412312', 'rambo@gmail.com', 'scrypt:32768:8:1$Qq3yIz3drWtUSd7I$c3bd0acd8f576a838eff156bb6b3c01955407663ae6398c7492396d7b8af3ae66838943ac3445d189ce954eb75d86ada8fb619651a655b89ee8bba37f3fb3688', 'Ucrania', '2024-11-24', 'clientes/rambo.jpg'),
(24, 'Gigachad', 'Apellido', '2024-10-30', '1231', 'giga@gmail.com', 'scrypt:32768:8:1$IXwrS8JaKDPoKB7R$8db1f171c2d76cf0ed290b2ac7948ac59cb7d892cf39b7c4362d4bb5b0db8440a8b0c12cab11a35b6794a71b527154aee23b95ededc198a3bd2d52f4872f27c9', 'Cielo', '2024-11-25', 'clientes/yo.jpg'),
(25, 'prueba', 'apellido2', '2024-11-15', '17412312', 'prueba@gmail.com', 'scrypt:32768:8:1$49OlcmqMekNVGljp$928265e41a74a0170cb86c0450bad272c2099b75ec09b40320d7189fb7802fb50a0e1fbbfbddfe355298abe14bde01b0d6cb0a1a09cc96a3e08fc97c19ca7727', 'aqui', '2024-11-25', 'clientes/eeeaa72c3bd4af6bdeafda555c80da0a.jpg'),
(26, 'prueba2', 'apellido2', '2024-11-07', '17412312', 'prueba2@gmail.com', 'scrypt:32768:8:1$sHtLjktqBqqm5ljI$711d90d69276a86ddfbf0cc0750029fd82cbb326baf81b7eaba902d57e7450f71ae06d1e4284f181441be995ffed080a32d2fd0d34465900488cc47378519337', 'Narnia', '2024-11-25', 'clientes/Sin_titulo.png');

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
(1, 'Carbón', 400.00, 31, 'Acceso a laas', 'uploads/carbon.jpg'),
(2, 'Hierro', 800.00, 30, 'Carbon + Entrenamientos con proteina incluida', 'uploads/hierro.jpg'),
(4, 'Oros', 12020.00, 30, 'Hierro + Instructor personal', 'uploads/oro.jpg'),
(6, 'Diamante', 1600.00, 30, 'Oro + Nutriologo Incluido', 'uploads/diamante.jpg'),
(7, 'Super Carbón', 2000.00, 180, 'Semestre de beneficios carbón', 'uploads/bloquecarbon.jpg'),
(8, 'Super Hierro', 4000.00, 180, 'Semestre de beneficios Hierro', 'uploads/bloquehierro.jpg'),
(9, 'Super Oro', 6000.00, 180, 'Semestre de beneficios oro', 'uploads/bloqueoro.jpg'),
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
(1, 9),
(6, 9),
(8, 7),
(9, 9);

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
(24, 17, 8, '2024-11-25', 4000.00, 'Tarjeta de Debito', 'Pendiente', '7232f49335', 'Activo'),
(25, 19, 1, '2024-11-25', 400.00, 'Efectivo', 'Pendiente', '80d3a39e26', 'Activo'),
(26, 19, 2, '2024-11-25', 800.00, 'Efectivo', 'Pendiente', 'f9ce2cb2bd', 'Inactivo'),
(27, 17, 10, '2024-11-25', 8000.00, 'Efectivo', 'Pendiente', '503fcd2eec', 'Inactivo'),
(28, 17, 1, '2024-11-25', 400.00, 'Efectivo', 'Pendiente', '2fc47fc8f3', 'Inactivo');

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
(8, 'Octavio Paz', 'Mantenimiento', 5000.00, 12, 'Matutino');

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
  MODIFY `ID_Admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `clases`
--
ALTER TABLE `clases`
  MODIFY `ID_Clase` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `ID_Cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `membresias`
--
ALTER TABLE `membresias`
  MODIFY `ID_Membresia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `pagos`
--
ALTER TABLE `pagos`
  MODIFY `ID_Pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `personal`
--
ALTER TABLE `personal`
  MODIFY `ID_Personal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `clases`
--
ALTER TABLE `clases`
  ADD CONSTRAINT `fk_personal` FOREIGN KEY (`ID_Personal`) REFERENCES `personal` (`ID_Personal`) ON DELETE SET NULL;

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
