-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 2017-11-20 04:50:37
-- 服务器版本： 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `suriweb`
--

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户的ID',
  `username` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户名',
  `password` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '密码',
  `mail` varchar(30) DEFAULT NULL COMMENT '邮箱',
  `info` text COMMENT '个人简介',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COMMENT='用户名登录和注册' AUTO_INCREMENT=12 ;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `mail`, `info`) VALUES
(1, 'root', 'root', NULL, NULL),
(2, 'wuyy3', 'wuyy', NULL, NULL),
(3, 'wuyy3', 'wuyy', NULL, NULL),
(4, 'wuyy78', 'wuyy78', NULL, NULL),
(5, 'wuyy78', 'wuyy78', NULL, NULL),
(6, 'wuyy78', 'wuyy78', 'wuyy@126.com', '清华大学'),
(7, 'hello', 'de', 'adaas', 'ed'),
(8, 'gr', 'gr', 'sgs', 'csd'),
(9, 'wuyy758', 'wuyy758', 'wuyy@126.com', '清华大学'),
(10, 'das', 'ds', 'ds', 'ds'),
(11, 'ds', 'ds', 'ds', '哈哈');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
