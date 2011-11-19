


CREATE DATABASE IF NOT EXISTS picturme CHARACTER SET utf8;
use mysql;

INSERT INTO user (Host,User,Password) VALUES('107.22.190.247','django',PASSWORD('n2EdygGba'));
SET PASSWORD FOR 'django'@'107.22.190.247' = PASSWORD('n2EdygGba');

flush privileges; 
grant all privileges on picturme.* to django@107.22.190.247;
flush privileges;


