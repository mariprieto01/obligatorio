USE obligatorio;

-- Trigger para evitar que un técnico tenga dos mantenimientos en la misma hora
CREATE TRIGGER evitar_mantenimientos_en_misma_hora
BEFORE INSERT ON Mantenimientos
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM Mantenimientos
            WHERE ci_tecnico = NEW.ci_tecnico
            AND NEW.fecha BETWEEN DATE_SUB(fecha, INTERVAL 59 MINUTE) AND DATE_ADD(fecha, INTERVAL 59 MINUTE)
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El técnico ya tiene un mantenimiento en ese rango horario.';
    END IF;
END;

