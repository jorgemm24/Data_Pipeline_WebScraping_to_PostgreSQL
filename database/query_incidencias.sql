create table test1 (
id int,
name varchar(20)
)

-- insert into test1 values(1,'jorge')
-- delete from public.test1

select * from public.test1


-- drop table incidencias
-- truncate table incidencias
create table incidencias(
DNI varchar(10),
Gestor_COT varchar(100),
FechaRegistro timestamp,
CodIncidencia varchar(100), 
TPIncidencia varchar(100), 
Motivo varchar(100), 
Fecha date,
FechaInicio  timestamp,
FechaFin  timestamp,
DOID varchar(100), 
Registrado_Por  varchar(100), 
Modo varchar(1), 
--Tiempo_Incidencias_Formato varchar(20), -- time,
Tiempo_Incidencias_Formato  time,
Tiempo_Incidencias_Minutos decimal(8,2),
Observacion  varchar(1000)
)

select count(1) from public.incidencias
select * from public.incidencias