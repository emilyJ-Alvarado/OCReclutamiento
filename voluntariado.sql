create database voluntariado;

use voluntariado;

show tables;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL UNIQUE,
  	`password` varchar(255) NOT NULL,
  	`dni` varchar(10) NOT NULL UNIQUE, 
  	`nombre` varchar(100) NOT NULL,    
  	`apellido` varchar(100) NOT NULL,
	`edad` int(11) NOT NULL,
  	`sexo` varchar(20) NOT NULL,   
	`pre_test` float(11) NOT NULL,
	`post_test` float(11) NOT NULL, 
	`aceptacion_terminos` int(11) NOT NULL, 
	`tipo_usuario` int(11) NOT NULL,
	`date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,    
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

describe accounts;

select * from accounts;

INSERT INTO `accounts` (`id`, `username`, `password`, `dni`,`nombre`,`apellido`,`edad`,`sexo`, `pre_test`, `post_test`,`aceptacion_terminos`,`tipo_usuario`) VALUES (1, 'nohely', '123', 'ABC001','Nohely','Peña',26,'Femenino', -1, -1, 0, 0);
INSERT INTO `accounts` (`username`, `password`, `dni`,`nombre`,`apellido`,`edad`,`sexo`, `pre_test`, `post_test`,`aceptacion_terminos`,`tipo_usuario`) VALUES ( 'mitchell', '123', 'ABC002','Mitchell','Blancas',34,'Masculino', -1, -1, 0, 0);
INSERT INTO `accounts` (`username`, `password`, `dni`,`nombre`,`apellido`,`edad`,`sexo`, `pre_test`, `post_test`,`aceptacion_terminos`,`tipo_usuario`) VALUES ( 'bris', 'xyz',     'DOC001','Briseyda','Peña',   25,'Femenino', -1, -1, 0, 1);

UPDATE accounts SET post_test = -1 WHERE id = 1;
UPDATE accounts SET aceptacion_terminos = 0 WHERE id = 1;

