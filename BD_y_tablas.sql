DROP DATABASE IF EXISTS obligatorio;
CREATE DATABASE obligatorio;
USE obligatorio;

CREATE TABLE Login (
    correo VARCHAR(50),
    contraseña VARCHAR(50),
    es_administrador BOOLEAN
);

CREATE TABLE Proveedores (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    contacto INT(9)
);

CREATE TABLE Insumos (
    id INT PRIMARY KEY,
    descripcion VARCHAR(50),
    tipo VARCHAR(50),
    precio_unitario DECIMAL(10,2),
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id)
);

CREATE TABLE Clientes (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    direccion VARCHAR(50),
    telefono INT(9),
    correo VARCHAR(50)
);

CREATE TABLE Maquinas (
    id INT PRIMARY KEY,
    modelo VARCHAR(20),
    id_cliente INT,
    ubicacion_cliente VARCHAR(50),
    costo_alquiler_mensual DECIMAL(10,2),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id)
);

CREATE TABLE Registro_consumo (
    id INT PRIMARY KEY,
    id_maquina INT,
    id_insumo INT,
    fecha DATE,
    cantidad_usada INT,
    FOREIGN KEY (id_maquina) REFERENCES Maquinas(id),
    FOREIGN KEY (id_insumo) REFERENCES Insumos(id)
);

CREATE TABLE Tecnicos (
    ci INT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    telefono INT(9)
);

CREATE TABLE Mantenimientos (
    id INT PRIMARY KEY,
    id_maquina INT,
    ci_tecnico INT,
    tipo VARCHAR(50),
    fecha DATE,
    observaciones VARCHAR(50),
    FOREIGN KEY (id_maquina) REFERENCES Maquinas(id),
    FOREIGN KEY (ci_tecnico) REFERENCES Tecnicos(ci)
);
