-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 27, 2022 at 04:52 PM
-- Server version: 10.6.11-MariaDB
-- PHP Version: 8.1.12
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;

-- --------------------------------------------------------
--
-- Table structure for table `admins`
--
CREATE TABLE `admins` (
    `id` int(11) NOT NULL,
    `user_id` varchar(50) NOT NULL,
    `folder_name` varchar(50) DEFAULT NULL,
    `storagesize` varchar(20) DEFAULT NULL,
    `auth` varchar(50) DEFAULT NULL,
    `permlevel` int(11) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
--
-- Dumping data for table `admins`
--
INSERT INTO `admins` (
        `id`,
        `user_id`,
        `folder_name`,
        `storagesize`,
        `auth`,
        `permlevel`
    )
VALUES (
        1,
        'YOUR_DISCORD_ID',
        'YOUR_DISCORD_ID',
        '100',
        '8wjZWrnDLs_9Rg',
        1
    );
-- --------------------------------------------------------
--
-- Table structure for table `alembic_version`
--
CREATE TABLE `alembic_version` (`version_num` varchar(32) NOT NULL) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
--
-- Dumping data for table `alembic_version`
--
INSERT INTO `alembic_version` (`version_num`)
VALUES ('87d705b94db8');
-- --------------------------------------------------------
--
-- Table structure for table `settings`
--
CREATE TABLE `settings` (
    `id` int(11) NOT NULL,
    `name` varchar(25) DEFAULT NULL,
    `description` varchar(500) DEFAULT NULL,
    `webhook` varchar(200) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;
--
-- Dumping data for table `settings`
--
INSERT INTO `settings` (
        `id`,
        `name`,
        `description`,
        `webhook`
    )
VALUES (
        1,
        'Image Uploader',
        'A simple and easy to use ShareX server made by icedoesjs on Github',
        NULL
    );
--
-- Indexes for dumped tables
--
--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
ADD PRIMARY KEY (`id`);
--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
ADD PRIMARY KEY (`version_num`);
--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
ADD PRIMARY KEY (`id`);
--
-- AUTO_INCREMENT for dumped tables
--
--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 2;
--
-- AUTO_INCREMENT for table `settings`
--
ALTER TABLE `settings`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
    AUTO_INCREMENT = 2;
COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;
