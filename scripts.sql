create table cities(
    city_id serial primary key,
    city_name varchar(128) not null
);

create table prod_groups(
    group_id serial primary key,
    group_name varchar(128) not null
);

create table cars(
    car_id serial primary key,
    prod_group_id integer references prod_groups(group_id) not null,
    car_name varchar(128) not null,
    car_year integer not null
);

create table users(
    user_id serial primary key,
    tg_user_id integer not null,
    tg_username varchar(128) not null,
    first_name varchar(128) not null,
    birth_date date not null,
    phone_number varchar(12) not null,
    user_email varchar(128) not null,
    user_password varchar(256) not null,
    city_id integer references cities(city_id),
    car_id integer references cars(car_id),
    card_id integer,
    is_vip varchar(1) default 'N'
);