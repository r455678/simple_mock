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
  `project_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mock_config
-- ----------------------------
INSERT INTO `mock_config` VALUES ('1', '请求登陆11', 'var1=1&var2=2&var3=3', 'post', '/login/manageLogin2', 'var1=1&var2=2&var3=3', '{\"status\":\"fail\",\"msg\":\"111用户名或密码错误,密码输错超过5次将被锁定哦！已输错1次\",\"data\":\"\",\"externData\":null}', '2017-08-10 17:54:05', '0', '营销平台');
