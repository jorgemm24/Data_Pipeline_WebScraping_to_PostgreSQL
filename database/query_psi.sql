--   drop table psi;

create table psi (
Ticket varchar(250),
TipoAveria varchar(250),
Atencion varchar(250),
Quiebre varchar(250),
CodAveria varchar(250),
codcli  varchar(250),
ClienteNombre  varchar(250),
ClienteCelular  varchar(250),
ClienteTelefono  varchar(250),
ClienteDNI  varchar(250),
EmbajadorNombre  varchar(250),
EmbajadorCelular  varchar(250),
EmbajadorCorreo  varchar(250),
EmbajadorDNI  varchar(250),
ComentarioTicket varchar(1000),
asignado varchar(250),
FechaRegistro   timestamp,
motivo varchar(250),
submotivo varchar(250),
estado varchar(250),
ObservacionUltMov  varchar(250),
FechaUltMov timestamp,
UsuarioMov  varchar(250),
login  varchar(250),
Producto  varchar(250),
Accion  varchar(250),
EstadoLegado  varchar(250),
FechaRegistroLegado timestamp,
FechaLiquidacion timestamp,
CodigoLiquidacion varchar(250),
DetalleLiquidacion  varchar(250),
Area  varchar(250),
Contrata  varchar(250),
Zonal  varchar(250),
evento_masiva  varchar(250),
CodMov  varchar(250),
fh_reg104 varchar(20),   --timestamp,   datos con mucha basura
fh_reg1l  varchar(20),   --timestamp,   datos con mucha basura
fh_reg2l  varchar(20),   --timestamp,   datos con mucha basura
cod_multigestion  varchar(250),
llamador  varchar(250),
titular  varchar(250),
direccion varchar(500),
distrito varchar(250),
urbanizacion varchar(250),
telf_gestion  varchar(250),
telf_entrante  varchar(250),
operador  varchar(250),
motivo_call  varchar(250),
grupo  varchar(250),
fecha_rellamada timestamp,
responsable  varchar(250),
GrupoResponsable  varchar(250),
incidencia  varchar(250),
observacion_indicencia  varchar(250),
FechaIniGestion  timestamp,
FechaAsignacionUsuario  timestamp,
SubNivel  varchar(250),
Quiebre_origen  varchar(250),
tipo_atencion_origen  varchar(250),
peticion  varchar(250),
requerimiento  varchar(250),
Canal  varchar(250)
)

--   drop table psi;
-- truncate table psi

select count(1) from psi;
select * from psi;

select distinct fechainigestion, fechaasignacionusuario from psi