CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'administrador';
CREATE USER 'user'@'localhost' IDENTIFIED BY 'usuario';

GRANT ALL PRIVILEGES ON obligatorio.* TO 'admin_user'@'localhost';
GRANT SELECT, INSERT ON obligatorio.* TO 'user'@'localhost'; # Solo puede leer y agregar datos

FLUSH PRIVILEGES; # Aplica los cambios inmediatamente