-- Таблица городов России, где может быть зарегистрирован пользователь для доставки
create table cities(
    city_id serial primary key,
    city_name      varchar(128) not null
);

-- Таблица марок машин
create table prod_groups(
    group_id   serial primary key,
    group_name varchar(128) not null
);

-- Таблица с машинами, ДОЛЖНА РАСШИРИТЬСЯ
create table cars(
    car_id serial primary key,
    prod_group_id integer references prod_groups(group_id) not null,
    car_name      varchar(128) not null,
    car_year      integer not null
    -----------------------------------------------
);

-- Таблица с компонентами, ОСНОВНАЯ ДЛЯ ЗАКАЗА
create table details(
    detail_id            serial primary key,
    detail_name          varchar(128) not null,
    article_number       varchar(20) not null,
    date_of_last_receipt date default current_date,
    -----------------------------------------------
);

-- Таблица с Пользователями, связана с Телеграм данными
create table users(
    user_id serial primary key,
    tg_user_id     integer,
    tg_username    varchar(128),
    first_name     varchar(128) not null,
    birth_date     date not null,
    phone_number   varchar(12) not null,
    user_email     varchar(128) not null,
    user_password  varchar(256) not null,
    city_id        integer references cities(city_id),
    car_id         integer references cars(car_id),
    card_id        integer,
    is_vip         varchar(1) default 'N'
);

-- Таблица с Заказами
create table orders(
    order_id serial primary key,
    user_id  integer references users(user_id) not null,
    ----------------------------------------------------
);