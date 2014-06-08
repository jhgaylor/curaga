drop table if exists users;
create table users (
    id integer primary key autoincrement,
    name varchar(200) not null,
    password text not null
);

drop table if exists packages;
create table packages (
    id integer primary key autoincrement,
    name varchar(200) unique not null,
    user_id integer not null,
    foreign key (user_id) references users(id)
);

drop table if exists package_downloads;
create table package_downloads (
    package_id integer not null,
    ip varchar(50),
    foreign key (package_id) references packages(id)
);