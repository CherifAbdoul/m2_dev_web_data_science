create database customers_base;
use customers_base;

show create table customers;

CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` text COLLATE latin1_general_ci,
  `last_name` text COLLATE latin1_general_ci,
  `email` text COLLATE latin1_general_ci,
  `phone` text COLLATE latin1_general_ci,
  `address` text COLLATE latin1_general_ci,
  `gender` text COLLATE latin1_general_ci,
  `age` int DEFAULT NULL,
  `registered` datetime DEFAULT NULL,
  `orders` int DEFAULT NULL,
  `spent` double DEFAULT NULL,
  `job` text COLLATE latin1_general_ci,
  `hobbies` text COLLATE latin1_general_ci,
  `is_married` text COLLATE latin1_general_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1006 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;



drop table if exists california_housing;
create table if not exists california_housing(
id int auto_increment primary key,
med_inc double,
house_age double,
ave_rooms double,
ave_bed_rms double,
population double,
ave_occupation double,
latitude double,
longitude double,
price double,
price_predict double
);

drop table if exists reportings;
create table if not exists reportings(
id int auto_increment primary key,
type_bien varchar(50),
pieces varchar(10),
region varchar(50),
nb_vente int,
ca_vente double,
semaine varchar(10),
mois date
);
