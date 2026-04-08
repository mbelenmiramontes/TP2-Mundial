create database if not exists database_tpbackend;
use database_tpbackend;

-- tabla de usuarios
create table usuarios (
    id int auto_increment primary key,
    nombre varchar(100) not null,
    email varchar(100) not null unique
);

-- tabla partidos
create table partidos (
    id int auto_increment,
    equipo_local varchar(100) not null,
    equipo_visitante varchar(100) not null,
    fecha datetime not null,
    fase enum('grupos', 'dieciseisavos', 'octavos', 'cuartos', 'semis', 'final') not null
);

-- tabla de resultados
create table resultados (
    id_partido int primary key,
    goles_local int not null,
    goles_visitante int not null,
    foreign key (id_partido) references partidos(id) on delete cascade
    );

-- Foreign key - Numero que "pertenece" a otra tabla
-- References - Saca la información de partidos(id)
-- Delete cascade - Si se borra un partido de la tabla partidos , borra los resultados de ese partido

# tabla de ranking
create table ranking (
    id int auto_increment primary key,
    id_usuario int not null,
    id_partido int not null,
    goles_local int not null,
    goles_visitante int not null,
    unique(id_usuario, id_partido), -- Evita que un usuario prediga dos veces el mismo partido
    foreign key (id_usuario) references usuarios(id) on delete cascade,
    foreign key (id_partido) references partidos(id) on delete cascade
)

-- Foreign key - Numero que "pertenece" a otra tabla
-- References - Saca la información de la tabla usuarios(id)/partidos(id)
-- Delete cascade - Si se borra un usuario/partido, borra los resultados de predicción