-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2021-04-11 11:55:37
-- 服务器版本： 8.0.17
-- PHP 版本： 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `block_chain`
--

-- --------------------------------------------------------

--
-- 表的结构 `buyed`
--

CREATE TABLE `buyed` (
  `pid` int(10) NOT NULL,
  `address` varchar(30) NOT NULL,
  `contact` varchar(11) NOT NULL,
  `performer` varchar(30) NOT NULL,
  `optime` datetime NOT NULL,
  `discribe` text NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `buyed`
--

INSERT INTO `buyed` (`pid`, `address`, `contact`, `performer`, `optime`, `discribe`, `status`) VALUES
(123, '北京', '12345678910', '老杨', '2019-07-13 10:11:16', 'first', 2);

-- --------------------------------------------------------

--
-- 表的结构 `process`
--

CREATE TABLE `process` (
  `pid` int(10) NOT NULL,
  `address` varchar(30) NOT NULL,
  `contact` varchar(11) NOT NULL,
  `discribe` text NOT NULL,
  `performer` varchar(30) NOT NULL,
  `optime` datetime NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `process`
--

INSERT INTO `process` (`pid`, `address`, `contact`, `discribe`, `performer`, `optime`, `status`) VALUES
(123, '海淀', '12345678910', 'first', '老杨', '2019-07-13 01:52:39', 2);

-- --------------------------------------------------------

--
-- 表的结构 `sale`
--

CREATE TABLE `sale` (
  `pid` int(10) NOT NULL,
  `name` varchar(30) NOT NULL,
  `birthday` datetime NOT NULL,
  `address` varchar(50) NOT NULL,
  `performer` varchar(30) NOT NULL,
  `contact` varchar(11) NOT NULL,
  `info` text NOT NULL,
  `discribe` text NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `sale`
--

INSERT INTO `sale` (`pid`, `name`, `birthday`, `address`, `performer`, `contact`, `info`, `discribe`, `status`) VALUES
(123, '西红柿', '2019-07-13 01:23:57', '海淀', '老杨', '12345678910', '西红柿不好吃', 'first', 2);

-- --------------------------------------------------------

--
-- 表的结构 `transfer`
--

CREATE TABLE `transfer` (
  `pid` int(10) NOT NULL,
  `address` varchar(30) NOT NULL,
  `contact` varchar(11) NOT NULL,
  `performer` varchar(30) NOT NULL,
  `discribe` text NOT NULL,
  `optime` datetime NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `transfer`
--

INSERT INTO `transfer` (`pid`, `address`, `contact`, `performer`, `discribe`, `optime`, `status`) VALUES
(123, '海淀', '12345678910', '老杨', 'first', '2019-07-13 09:29:30', 2);

-- --------------------------------------------------------

--
-- 表的结构 `up_relation`
--

CREATE TABLE `up_relation` (
  `uid` int(10) NOT NULL,
  `step` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `up_relation`
--

INSERT INTO `up_relation` (`uid`, `step`, `pid`, `id`) VALUES
(12345, 1, 123, 14),
(12345, 2, 123, 15),
(12345, 3, 123, 16),
(12345, 4, 123, 17);

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `uid` int(10) NOT NULL,
  `password` varchar(12) NOT NULL,
  `phone_num` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `total_num` int(11) NOT NULL DEFAULT '0',
  `sale_num` int(11) NOT NULL DEFAULT '0',
  `tran1_num` int(11) NOT NULL DEFAULT '0',
  `process_num` int(11) NOT NULL DEFAULT '0',
  `tran2_num` int(11) NOT NULL DEFAULT '0',
  `buy_num` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`uid`, `password`, `phone_num`, `total_num`, `sale_num`, `tran1_num`, `process_num`, `tran2_num`, `buy_num`) VALUES
(15, '1234567890', '1524182@qq.com', 0, 0, 0, 0, 0, 0),
(1234, '12345678', '13345678912', 0, 0, 0, 0, 0, 0),
(12345, '12345678', '13345678916', 0, 0, 0, 0, 0, 0);

--
-- 转储表的索引
--

--
-- 表的索引 `buyed`
--
ALTER TABLE `buyed`
  ADD PRIMARY KEY (`pid`);

--
-- 表的索引 `process`
--
ALTER TABLE `process`
  ADD PRIMARY KEY (`pid`);

--
-- 表的索引 `sale`
--
ALTER TABLE `sale`
  ADD PRIMARY KEY (`pid`);

--
-- 表的索引 `transfer`
--
ALTER TABLE `transfer`
  ADD PRIMARY KEY (`pid`);

--
-- 表的索引 `up_relation`
--
ALTER TABLE `up_relation`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`,`phone_num`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `up_relation`
--
ALTER TABLE `up_relation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
