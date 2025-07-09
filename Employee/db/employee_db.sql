-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 08, 2025 at 01:57 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `employee_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', '21232f297a57a5a743894a0e4a801fc3');

-- --------------------------------------------------------

--
-- Table structure for table `employee_db`
--

CREATE TABLE `employee_db` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `position` varchar(100) NOT NULL,
  `role` enum('admin','employee') NOT NULL DEFAULT 'employee',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee_db`
--

INSERT INTO `employee_db` (`id`, `username`, `password`, `name`, `address`, `age`, `gender`, `position`, `role`, `created_at`) VALUES
(4, 'superadmin', '0270c14315e59915aeeef28af06e8cce3298de9cad6436bcb7cc3dc345fa14865faefb6f9bd286320ded5d2e0c163c4582f01ef0d440095b867146e4a59589e2', 'admin', 'superadmin', 19, 'Male', 'superadmin', 'admin', '2025-07-08 11:14:47'),
(6, 'belle', '0270c14315e59915aeeef28af06e8cce3298de9cad6436bcb7cc3dc345fa14865faefb6f9bd286320ded5d2e0c163c4582f01ef0d440095b867146e4a59589e2', 'sdad', 'dasdasd', 21, 'Male', 'sadsada', 'employee', '2025-07-08 11:54:34'),
(8, 'admin', 'c047c8274fe350bae00d2950ad3ca1b6c2b0e2aec6cfac00a66d982189b9312addf3a7b56978091e9403f6cb5ecb257abd7f37597a1d35e5d46eba18af79fe92', 'admin', 'superadmin', 19, 'Female', 'superadmin', 'admin', '2025-07-08 11:56:13');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `employee_db`
--
ALTER TABLE `employee_db`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employee_db`
--
ALTER TABLE `employee_db`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
