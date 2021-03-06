-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: 2017-12-06 08:19:00
-- 服务器版本： 5.7.19
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `suriweb`
--

-- --------------------------------------------------------

--
-- 表的结构 `task`
--

DROP TABLE IF EXISTS `task`;
CREATE TABLE IF NOT EXISTS `task` (
  `id` int(100) NOT NULL AUTO_INCREMENT COMMENT 'task的id',
  `userId` int(100) DEFAULT NULL COMMENT '用户ID',
  `isCompleted` tinyint(4) DEFAULT NULL COMMENT '任务完成状态',
  `beginTime` int(100) DEFAULT NULL COMMENT '任务开始时间',
  `endTime` int(100) DEFAULT NULL COMMENT '任务结束时间',
  `resultPath` varchar(200) DEFAULT NULL COMMENT '存储结果的路径 /result/username/',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `task`
--

INSERT INTO `task` (`id`, `userId`, `isCompleted`, `beginTime`, `endTime`, `resultPath`) VALUES
(1, 1, 0, 1243, 14135351, NULL),
(4, 8, 0, 1512546725, 0, 'C:\\Users\\winsen\\Desktop\\SuriWeb\\app\\result\\winsen\\'),
(7, 8, 0, 1512546832, 0, 'C:\\Users\\winsen\\Desktop\\SuriWeb\\app\\result\\winsen\\'),
(6, 8, 0, 1512546819, 0, 'C:\\Users\\winsen\\Desktop\\SuriWeb\\app\\result\\winsen\\'),
(8, 8, 0, 1512547225, 0, 'C:\\Users\\winsen\\Desktop\\SuriWeb\\app\\result\\winsen\\'),
(9, 8, 0, 1512547258, 0, 'C:\\Users\\winsen\\Desktop\\SuriWeb\\app\\result\\winsen\\'),
(10, 1, 0, 1512547338, 0, 'C:\\Users\\winsen\\Desktop\\SuriWeb\\app\\result\\root\\');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户的ID',
  `username` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '用户名',
  `password` varchar(50) CHARACTER SET utf8 DEFAULT NULL COMMENT '密码',
  `mail` varchar(30) DEFAULT NULL COMMENT '邮箱',
  `info` text COMMENT '个人简介',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COMMENT='用户名登录和注册';

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `mail`, `info`) VALUES
(1, 'root', 'root', NULL, NULL),
(2, 'wuyy78', 'wuyy78', 'wuyy@126.com', '清华大学'),
(3, 'wuyy758', 'wuyy758', 'wuyy@126.com', '清华大学'),
(4, 'liuzf13', 'test', 'liuzf13@163.com', 'register test'),
(5, 'liuzf2', 'test', 'liuzf13@163.com', 'register test2'),
(6, 'liuzf3', 'test', 'liuzf13@163.com', 'test for mial address'),
(7, 'liuzf5', 'test', 'liuzf13@mails.tsinghua.edu.cn', 'test for register'),
(8, 'winsen', 'winsen', 'winsen@123.com', 'winsen\r\n');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
