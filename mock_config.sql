SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `mock_config`
-- ----------------------------
DROP TABLE IF EXISTS `mock_config`;
CREATE TABLE `mock_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `reqparams` varchar(500) DEFAULT NULL,
  `methods` varchar(50) DEFAULT NULL,
  `domain` varchar(50) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `resparams` varchar(500) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` int(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mock_config
-- ----------------------------
