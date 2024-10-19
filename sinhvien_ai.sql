-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 15, 2024 at 02:43 AM
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
-- Database: `sinhvien_ai`
--

-- --------------------------------------------------------

--
-- Table structure for table `sinhvien`
--

CREATE TABLE `sinhvien` (
  `MaSinhVien` varchar(10) NOT NULL,
  `TenSinhVien` varchar(100) NOT NULL,
  `Lop` varchar(10) NOT NULL,
  `GioiTinh` enum('Nam','Nữ') NOT NULL,
  `Avatar` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sinhvien`
--

INSERT INTO `sinhvien` (`MaSinhVien`, `TenSinhVien`, `Lop`, `GioiTinh`, `Avatar`) VALUES
('2254810182', 'Trần Thanh Đạt', '22DHTT04', 'Nam', 'user.png'),
('2265898009', 'Hien Ho', '22DHTT07', 'Nam', 'user.png'),
('2234810122', 'Khang', '22DHVW22', 'Nam', 'user.png'),
('22123244', 'fasfdgg', 'dsadsafgsd', 'Nam', 'user.png'),
('dfdsfdsf', 'dsadsadd', 'safsafsad', 'Nam', 'user.png');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
