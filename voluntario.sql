create database voluntario;
show databases;
use voluntario;

show tables;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL UNIQUE,
  	`correo` varchar(100) NOT NULL,        
  	`dni` varchar(10) NOT NULL UNIQUE, 
  	`nombre` varchar(100) NOT NULL,    
  	`apellido` varchar(100) NOT NULL,
	`edad` int(11) NOT NULL,
  	`sexo` varchar(20) NOT NULL,
  	`universidad` varchar(100) NOT NULL,
  	`carrera` varchar(100) NOT NULL,
  	`ciclo` int(11) NOT NULL,    
	`tipo_usuario` int(11) NOT NULL,
  	`cargo` varchar(50) NOT NULL,      
  	`password` varchar(255) NOT NULL,    
	`pre_test` float(11) NOT NULL,
	`post_test` float(11) NOT NULL, 
	`aceptacion_terminos` int(11) NOT NULL,
	`aceptado` int(11) NOT NULL,    
	`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,    
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

describe accounts;

select * from accounts;

INSERT INTO `accounts` (`id`,`username`,`correo`,`dni`,`nombre`,`apellido`,`edad`,`sexo`,`universidad`,`carrera`,`ciclo`, `tipo_usuario`,`cargo`,`password`,`pre_test`,`post_test`,`aceptacion_terminos`,`aceptado`,`date`) values (1,'nohe','nohely180818@gmail.com','71254104','Nohely','Peña',27,'Femenino','Universidad Privada Antenor Orrego','Contabilidad',7, 0,'Est','123',50,-1,0,0,now());

INSERT INTO `accounts` (`username`,`correo`,`dni`,`nombre`,`apellido`,`edad`,`sexo`,`universidad`,`carrera`,`ciclo`, `tipo_usuario`,`cargo`,`password`,`pre_test`,`post_test`,`aceptacion_terminos`,`aceptado`,`date`) values ('emily','emilyjhas@gmail.com','58465321','Emily','Alvarado',23,'Femenino','Universidad Católica Santo Toribio de Mogrovejo','Ingeniería de sistemas',10, 1,'Est','123',50,-1,0,0,now());


UPDATE accounts SET post_test = -1 WHERE id = 1;
UPDATE accounts SET aceptacion_terminos = 0 WHERE id = 1;
