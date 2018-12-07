

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `wbs`;
CREATE TABLE `wbs` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) DEFAULT NULL,
  `weibos` text CHARACTER SET utf8mb4,
  `zhuanfa` text CHARACTER SET utf8mb4,
  `p_time` varchar(255) DEFAULT NULL,
  `num_zan` int(10) DEFAULT NULL,
  `num_forwarding` int(10) DEFAULT NULL,
  `num_comment` int(10) DEFAULT NULL,
  `ctt` text CHARACTER SET utf8mb4,
  `p_name` varchar(255) DEFAULT NULL,
  `ping_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=171286 DEFAULT CHARSET=utf8;
