CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';

CREATE DATABASE IF NOT EXISTS messages;

GRANT ALL PRIVILEGES ON ipmd TO 'admin'@'localhost';

USE messages;

CREATE TABLE IF NOT EXISTS messages (
  clid INT NOT NULL,
  mess TEXT NOT NULL,
  sid TEXT NOT NULL,
  PRIMARY KEY(clid)
);

INSERT INTO messages (clid, mess, sid) VALUES
(1, 'Hello world from messages table!', 'abc'),
(2, 'Test', 'def'),
(3, 'Yeray2 is the best team from ipmd', 'abc');