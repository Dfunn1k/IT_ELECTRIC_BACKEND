--
-- Create model Motor
--
CREATE TABLE `Baker_motor` (`motor_key` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `model` varchar(100) NOT NULL);
--
-- Create model Usuario
--
CREATE TABLE `Baker_usuario` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` integer NOT NULL UNIQUE);
--
-- Create model Test
--
CREATE TABLE `Baker_test` (`test_key` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `motor_nro_id` integer NOT NULL);
--
-- Add field usuario to motor
--
ALTER TABLE `Baker_motor` ADD COLUMN `usuario_id` bigint NOT NULL , ADD CONSTRAINT `Baker_motor_usuario_id_6c2489ff_fk_Baker_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `Baker_usuario`(`id`);
--
-- Create model Medicion
--
CREATE TABLE `Baker_medicion` (`medicion_key` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `time` datetime(6) NOT NULL, `mag_v1` double precision NOT NULL, `mag_v2` double precision NOT NULL, `mag_v3` double precision NOT NULL, `ang_v1` double precision NOT NULL, `ang_v2` double precision NOT NULL, `ang_v3` double precision NOT NULL, `v2_freq` double precision NOT NULL, `v3_freq` double precision NOT NULL, `mag_i1` double precision NOT NULL, `mag_i2` double precision NOT NULL, `mag_i3` double precision NOT NULL, `ang_i1` double precision NOT NULL, `ang_i2` double precision NOT NULL, `ang_i3` double precision NOT NULL, `i1_freq` double precision NOT NULL, `i2_freq` double precision NOT NULL, `i3_freq` double precision NOT NULL, `test_key_id` integer NOT NULL);
ALTER TABLE `Baker_usuario` ADD CONSTRAINT `Baker_usuario_user_id_84c75944_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `Baker_test` ADD CONSTRAINT `Baker_test_motor_nro_id_33363dea_fk_Baker_motor_motor_key` FOREIGN KEY (`motor_nro_id`) REFERENCES `Baker_motor` (`motor_key`);
ALTER TABLE `Baker_medicion` ADD CONSTRAINT `Baker_medicion_test_key_id_c7c90978_fk_Baker_test_test_key` FOREIGN KEY (`test_key_id`) REFERENCES `Baker_test` (`test_key`);
