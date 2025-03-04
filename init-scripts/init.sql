-- Crear el usuario 'admin99' con la contraseña 'Admin9999' en localhost
CREATE USER 'admin99'@'localhost' IDENTIFIED BY 'Admin9999';

-- Crear la base de datos 'messages' si no existe
CREATE DATABASE IF NOT EXISTS messages;

-- Otorgar todos los privilegios sobre la base de datos 'messages' al usuario 'admin99'
GRANT ALL PRIVILEGES ON messages.* TO 'admin99'@'localhost';

USE messages;

-- Crear la tabla 'messages' si no existe
CREATE TABLE IF NOT EXISTS messages (
  clid INT NOT NULL,  -- ID del mensaje
  mess TEXT NOT NULL, -- Contenido del mensaje
  sid TEXT NOT NULL,  -- ID del servidor
  PRIMARY KEY(clid)   -- Definir 'clid' como primary key
);

-- Insertar algunos datos de prueba en la tabla 'messages'
INSERT INTO messages (clid, mess, sid) VALUES
(1, 'Hello world!', 'abc'),
(2, 'Test2', 'def'),
(3, 'Last entry', 'xyz');
