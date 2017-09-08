CREATE DATABASE `admin_backend` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;


CREATE TABLE IF NOT EXISTS `apikey` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`owner` VARCHAR(128) NOT NULL,
    `key` VARCHAR(256) NOT NULL,
	`status` SMALLINT(4) NOT NULL,
	`created_at` DATETIME,
	`updated_at` DATETIME,
	PRIMARY KEY (`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 用户表
# 使用Django自带auth_user表