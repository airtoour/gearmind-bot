-- Таблица городов России, где может быть зарегистрирован пользователь для доставки
create table cities(
    city_id serial primary key,
    city_name      varchar(128) not null
);

create table cars_brand(
    id         serial primary key,
    brand_name varchar(256) not null
);

create table cars_model(
    id         serial primary key,
    brand_id   integer references cars_brand(id),
    model_name varchar(256) not null
);

create table cars_gens(
    id       serial primary key,
    model_id integer references cars_model(id) not null,
    gen_name varchar(256) not null
);

-- Таблица с Пользователями, связана с Телеграм данными
create table users(
    user_id       serial primary key,
    tg_user_id    integer,
    tg_username   varchar(128),
    first_name    varchar(128) not null,
    birth_date    date not null,
    phone_number  varchar(12) not null,
    user_email    varchar(128) not null,
    user_password varchar(256) not null,
    city_id       integer references cities(city_id)
);

-- Таблица с машинами, ДОЛЖНА РАСШИРИТЬСЯ
create table cars(
    car_id   serial primary key,
    brand_id integer references cars_brand(id) not null,
    model_id integer references cars_model(id) not null,
    gen_id   integer references cars_gens(id) not null,
    user_id  integer references users(user_id) not null
);