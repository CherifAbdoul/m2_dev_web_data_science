SELECT * FROM customers.client;

create database customers_base;
use customers_base;

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
