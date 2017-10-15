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
  `status` int(1) DEFAULT NULL,
  `ischeck` int(1) DEFAULT NULL,
  `project_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of mock_config
-- ----------------------------
INSERT INTO `mock_config` VALUES (338, '实名认证', '{\n	\"transType\":\"300002\",\n}', 'post', '/auth/bankCardVerified', '11', '{\n    \"success\": false,\n    \"errcode\": \"99999998\",\n    \"errmessage\": \"此身份信息已经实名认证\",\n    \"data\": null\n}', '2017-9-18 13:16:17', 0, 0, '支付核心');
