INSERT INTO Proveedores (nombre, contacto) VALUES 
('Suministros S.A.', '099123456'),
('Insumos del Sur', '092345678'),
('TecnoParts', '094567890'),
('IndustriaMax', '098112233'),
('Ferretería Pro', '091122334'),
('Provemaq', '093344556'),
('Distribuidora Central', '097788990');

INSERT INTO Insumos (descripcion, tipo, precio_unitario, id_proveedor) VALUES 
('Aceite hidráulico', 'Líquido', 250.00, 1),
('Filtro de aire', 'Repuesto', 150.50, 2),
('Tornillos M8', 'Fijación', 10.00, 3),
('Correa de transmisión', 'Repuesto', 320.00, 4),
('Grasa industrial', 'Lubricante', 180.00, 1),
('Limpiador dieléctrico', 'Limpieza', 95.00, 5),
('Sensor de presión', 'Electrónico', 560.00, 6);

INSERT INTO Clientes (nombre, direccion, telefono, correo) VALUES 
('Empresa Alfa', 'Av. 18 de Julio 1234', '099112233', 'alfa@empresa.com'),
('Taller Beta', 'Bvar. Artigas 5678', '091223344', 'beta@taller.com'),
('Constructora Gama', 'Cno. Carrasco 999', '092334455', 'gama@constru.com'),
('AgroTech', 'Ruta 8 Km 45', '094556677', 'contacto@agrotech.com'),
('Servicios Delta', 'Sarandí 345', '095667788', 'delta@servicios.com'),
('Metalúrgica Omega', 'Maldonado 789', '097778899', 'info@omega.com'),
('Soluciones XYZ', 'Av. Italia 1010', '093889900', 'xyz@soluciones.com');

INSERT INTO Maquinas (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual) VALUES
('MX-100', 1, 'Depósito principal', 1500),
('TX-200', 2, 'Taller central', 1200),
('GX-300', 3, 'Obra Carrasco', 1800),
('AX-400', 4, 'Campo norte', 1600),
('DX-500', 5, 'Base operativa', 1400),
('OX-600', 6, 'Galpón este', 1700),
('ZX-700', 7, 'Oficina técnica', 1550);

INSERT INTO Registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada) VALUES 
(1, 1, '2025-06-01', 5),
(2, 2, '2025-06-02', 3),
(3, 3, '2025-06-03', 50),
(4, 4, '2025-06-04', 2),
(5, 5, '2025-06-05', 4),
(6, 6, '2025-06-06', 1),
(7, 7, '2025-06-07', 2);

INSERT INTO Tecnicos (ci, nombre, apellido, telefono) VALUES 
(12345678, 'Luis', 'Pérez', '099111222'),
(23456789, 'Ana', 'García', '092222333'),
(34567890, 'Carlos', 'Rodríguez', '091333444'),
(45678901, 'Laura', 'Fernández', '094444555'),
(56789012, 'Diego', 'Martínez', '093555666'),
(67890123, 'Lucía', 'Gómez', '095666777'),
(78901234, 'Marcos', 'López', '097777888');

INSERT INTO Mantenimientos (id_maquina, ci_tecnico, tipo, fecha, observaciones) VALUES 
(1, 12345678, 'Preventivo', '2025-06-10 09:00:00', 'Todo correcto'),
(2, 23456789, 'Correctivo', '2025-06-11 14:00:00', 'Cambio de filtro'),
(3, 34567890, 'Preventivo', '2025-06-12 10:00:00', 'Lubricación'),
(4, 45678901, 'Correctivo', '2025-06-13 08:30:00', 'Ajuste de correa'),
(5, 56789012, 'Urgente', '2025-06-14 16:00:00', 'Falla eléctrica'),
(6, 67890123, 'Revisión', '2025-06-15 13:00:00', 'Chequeo general'),
(7, 78901234, 'Correctivo', '2025-06-16 11:00:00', 'Sensor dañado');