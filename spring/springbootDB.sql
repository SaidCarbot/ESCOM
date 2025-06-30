drop database if exists proyecto;
create database proyecto;

use proyecto;

create table Tareas(
	idTarea int not null auto_increment, 
    nombreTarea varchar(50) not null,
    descripcionTarea text not null,
    completada boolean not null,
    primary key (idTarea)
);

select * from tareas;