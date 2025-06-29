USE obligatorio;

CREATE TABLE Login (
    correo VARCHAR(50) PRIMARY KEY,
    contraseña VARCHAR(255) NOT NULL,
    es_administrador BOOLEAN NOT NULL
);

CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    contacto VARCHAR(20) NOT NULL
);

CREATE TABLE Insumos (
    id_insumo INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);

CREATE TABLE Clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(50) NOT NULL
);

CREATE TABLE Maquinas (
    id_maquina INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(20) NOT NULL,
    id_cliente INT NOT NULL,
    ubicacion_cliente VARCHAR(50) NOT NULL,
    costo_alquiler_mensual DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    CONSTRAINT cliente_ubicaciones UNIQUE (id_cliente, ubicacion_cliente) -- Para que un cliente no tenga dos máquinas en la misma ubicación
);

CREATE TABLE Registro_consumo (
    id_consumo INT AUTO_INCREMENT PRIMARY KEY,
    id_maquina INT NOT NULL,
    id_insumo INT NOT NULL,
    fecha DATE NOT NULL,
    cantidad_usada INT NOT NULL,
    FOREIGN KEY (id_maquina) REFERENCES Maquinas(id_maquina),
    FOREIGN KEY (id_insumo) REFERENCES Insumos(id_insumo)
);

CREATE TABLE Tecnicos (
    ci INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

CREATE TABLE Mantenimientos (
    id_mantenimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_maquina INT NOT NULL,
    ci_tecnico INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    fecha DATETIME NOT NULL,
    observaciones VARCHAR(50),
    FOREIGN KEY (id_maquina) REFERENCES Maquinas(id_maquina),
    FOREIGN KEY (ci_tecnico) REFERENCES Tecnicos(ci)
);