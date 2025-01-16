
/* 
se déplacer dans la base mysql
cd /usr/local/mysql/bin
./mysql -uroot -p

*/

/*afficher la liste des bases de données */
show databases;

/*selection une base de données */
use customers;

/* Afficher la liste des tables */
show tables;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    address VARCHAR(255),
    gender VARCHAR(255),
    age INT,
    registered date,
    orders INT,
    spent float,
    job VARCHAR(255),
    hobbies VARCHAR(255),
    is_married boolean
);


