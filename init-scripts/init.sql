CREATE USER 'admin99'@'localhost' IDENTIFIED BY 'Admin9999';

CREATE DATABASE IF NOT EXISTS messages;

GRANT ALL PRIVILEGES ON messages TO 'admin99'@'localhost';

USE messages;

CREATE TABLE IF NOT EXISTS messages (
  clid INT NOT NULL,
  mess TEXT NOT NULL,
  sid TEXT NOT NULL,
  PRIMARY KEY(clid)
);

INSERT INTO messages (clid, mess, sid) VALUES
(1, 'Hello world!', 'abc'),
(2, 'Test2', 'def'),
(3, 'Last entry', 'xyz');