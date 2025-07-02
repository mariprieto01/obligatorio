USE obligatorio;

INSERT INTO Login (correo, contraseña, es_administrador) VALUES
    ('admin@marloy.com', '91f5167c34c400758115c2a6826ec2e3', TRUE),
    ('usuario@marloy.com', 'f8032d5cae3de20fcec887f395ec9a6a', FALSE);

INSERT INTO Proveedores (nombre, contacto) VALUES
    ('Distribuidora Aroma', '099123456'),
    ('Café del Sur', '098765432'),
    ('Insumos del Café', '091234567');

INSERT INTO Clientes (nombre, direccion, telefono, correo) VALUES
    ('Oficinas Centra SRL', 'Av. Libertador 1234', '2901 2345', 'contacto@centra.com.uy'),
    ('Hospital Buena Salud', 'Bvar. Artigas 567', '2487 4567', 'compras@buenasalud.org'),
    ('Estudio Contable FinEs', 'Colonia 987', '099876543', 'fines@estudio.com');

INSERT INTO Insumos (descripcion, tipo, precio_unitario, id_proveedor) VALUES
    ('Café en grano premium', 'Café', 480.00, 1),
    ('Leche en polvo entera', 'Lácteo', 310.50, 3),
    ('Canela molida', 'Condimento', 150.00, 2),
    ('Chocolate en polvo', 'Complemento', 275.00, 3),
    ('Filtros de papel', 'Accesorios', 120.00, 1),
    ('Azúcar refinada', 'Complemento', 95.00, 2);

INSERT INTO Maquinas (modelo, id_cliente, ubicacion_cliente, costo_alquiler_mensual) VALUES
    ('MX-2000', 1, 'Recepción', 1500.00),
    ('CAF-500', 1, 'Sala de reuniones', 1800.00),
    ('BaristaPro', 2, 'Hall principal', 2000.00),
    ('EcoCafeMini', 3, 'Oficina central', 1300.00);

INSERT INTO Tecnicos (ci, nombre, apellido, telefono) VALUES
    (45678901, 'Lucía', 'González', '092345678'),
    (48765432, 'Martín', 'Pereira', '091112233'),
    (49001234, 'Sofía', 'Rodríguez', '098998877');

INSERT INTO Mantenimientos (id_maquina, ci_tecnico, tipo, fecha, observaciones) VALUES
    (1, 45678901, 'Preventivo', '2025-06-01 10:30:00', 'Cambio de filtro y limpieza general'),
    (3, 48765432, 'Asistencia', '2025-06-10 14:00:00', 'Error en dispensador de leche'),
    (2, 49001234, 'Preventivo', '2025-06-15 09:00:00', 'Revisión general sin novedades'),
    (4, 45678901, 'Asistencia', '2025-06-20 11:15:00', 'Fugas de agua en la base');

INSERT INTO Registro_consumo (id_maquina, id_insumo, fecha, cantidad_usada) VALUES
    (1, 1, '2025-07-05', 20),
    (1, 2, '2025-07-05', 10),
    (2, 1, '2025-07-05', 15),
    (2, 6, '2025-07-06', 8),
    (3, 4, '2025-07-07', 12),
    (3, 2, '2025-07-07', 6),
    (4, 3, '2025-07-08', 5);