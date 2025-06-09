mysql://root:VZypsbsOguzilgSYuVqZkeLJxsJYCJXN@crossover.proxy.rlwy.net:38518/railway
--root= es el usuario
--VZypsbsOguzilgSYuVqZkeLJxsJYCJXN = es el password
--crossover.proxy.rlwy.net = es el host
--railwayv = es el nombre de la base de datos

CREATE DATABASE gestion_formacion CHARACTER SET utf8 COLLATE utf8_general_ci;
USE gestion_formacion;

CREATE TABLE regional(
    cod_regional INT UNSIGNED PRIMARY KEY,
    nombre VARCHAR(80)
);

CREATE TABLE centro_formacion(
    cod_centro INT UNSIGNED PRIMARY KEY,
    nombre_centro VARCHAR(80),
    cod_regional INT UNSIGNED,
    FOREIGN KEY (cod_regional) REFERENCES regional(cod_regional)
);

ALTER TABLE programa_formacion MODIFY COLUMN nombre VARCHAR(130);
CREATE TABLE programa_formacion(
    cod_programa INT UNSIGNED,
    la_version TINYINT UNSIGNED,
    nombre VARCHAR(30),
    horas_lectivas INT,
    horas_productivas INT,
    PRIMARY KEY (cod_programa, la_version)
);

CREATE TABLE competencia(
    cod_competencia INT UNSIGNED PRIMARY KEY,
    nombre VARCHAR(60),
    horas INT UNSIGNED
);

CREATE TABLE resultado_aprendizaje(
    cod_resultado INT UNSIGNED PRIMARY KEY,
    nombre  VARCHAR(30),
    cod_competencia INT UNSIGNED,
    FOREIGN KEY (cod_competencia) REFERENCES competencia(cod_competencia)
);

CREATE TABLE programa_competencia(
    cod_prog_competencia INT UNSIGNED PRIMARY KEY,
    cod_programa INT UNSIGNED,
    la_version TINYINT UNSIGNED,
    cod_competencia INT UNSIGNED,
    FOREIGN KEY (cod_programa, la_version) REFERENCES programa_formacion(cod_programa, la_version),
    FOREIGN KEY (cod_competencia) REFERENCES competencia(cod_competencia)
);

AlTER TABLE grupo MODIFY COLUMN estado_grupo VARCHAR(30)
CREATE TABLE grupo(
    cod_ficha INT UNSIGNED,
    cod_centro INT UNSIGNED,
    cod_programa INT UNSIGNED,
    la_version TINYINT UNSIGNED,
    nombre_nivel VARCHAR(40),
    jornada VARCHAR(15),
    fecha_inicio DATE,
    fecha_fin DATE,
    etapa VARCHAR (20),
    modalidad VARCHAR(30),
    responsable VARCHAR(60),
    nombre_empresa VARCHAR(40),
    nombre_municipio VARCHAR(30),
    nombre_programa_especial VARCHAR(60),
    hora_inicio TIME,
    hora_fin TIME,
    aula_actual CHAR(20),
    PRIMARY KEY (cod_ficha),
    FOREIGN KEY(cod_centro) REFERENCES centro_formacion(cod_centro),
    FOREIGN KEY (cod_programa, la_version) REFERENCES programa_formacion(cod_programa, la_version)
);

CREATE TABLE datos_grupo(
    cod_ficha INT UNSIGNED,
    num_aprendices_masculinos  TINYINT UNSIGNED,
    num_aprendices_femenino  TINYINT UNSIGNED,
    num_aprendices_no_binario  TINYINT UNSIGNED,
    num_total_aprendices  TINYINT UNSIGNED,
    num_total_aprendices_activos  TINYINT UNSIGNED,
    cupo_total  TINYINT UNSIGNED,
    en_transito  TINYINT UNSIGNED,
    induccion  TINYINT UNSIGNED,
    formacion  TINYINT UNSIGNED,
    condicionado  TINYINT UNSIGNED,
    aplazado  TINYINT UNSIGNED,
    retiro_voluntuario  TINYINT UNSIGNED,
    cancelado  TINYINT UNSIGNED,
    cancelamiento_vit_comp  TINYINT UNSIGNED,
    desercion_vit_comp  TINYINT UNSIGNED,
    por_certificar  TINYINT UNSIGNED,
    certificados  TINYINT UNSIGNED,
    traslados  TINYINT UNSIGNED,
    otro  TINYINT UNSIGNED,
    FOREIGN KEY(cod_ficha) REFERENCES grupo(cod_ficha),
    PRIMARY KEY(cod_ficha)
);


CREATE TABLE rol(
    id_rol INT UNSIGNED PRIMARY KEY,
    nombre VARCHAR(30)
);

CREATE TABLE usuario(
    id_usuario INT UNSIGNED PRIMARY KEY,
    nombre_completo VARCHAR(80),
    identificacion BIGINT UNSIGNED,
    id_rol INT UNSIGNED,
    correo VARCHAR(100) UNIQUE,
    pass_hash VARCHAR(100),
    tipo_contrato VARCHAR(50),
    telefono VARCHAR(15),
    estado BOOLEAN,
    FOREIGN KEY(id_rol) REFERENCES rol(id_rol)
);


CREATE TABLE programacion(
    id_programacion INT UNSIGNED AUTO_INCREMENT,
    id_instructor INT UNSIGNED,
    cod_ficha INT UNSIGNED,
    fecha_programada DATE,
    horas_programadas INT,
    hora_inicio TIME,
    hora_fin TIME,
    cod_competencia INT UNSIGNED,
    cod_resultado INT UNSIGNED,
    id_user INT UNSIGNED,
    PRIMARY KEY(id_programacion),
    FOREIGN KEY(id_instructor) REFERENCES usuario(id_usuario),
    FOREIGN KEY(cod_ficha) REFERENCES grupo(cod_ficha),
    FOREIGN KEY(cod_competencia) REFERENCES competencia(cod_competencia),
    FOREIGN KEY(cod_resultado) REFERENCES resultado_aprendizaje(cod_resultado),
    FOREIGN KEY(id_user) REFERENCES usuario(id_usuario)
);

CREATE TABLE metas(
    id_meta INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    anio YEAR,
    concepto VARCHAR(100),
    valor INT UNSIGNED
);

CREATE TABLE festivos(
    festivo DATE PRIMARY KEY
);