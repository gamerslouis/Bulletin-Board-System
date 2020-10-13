create table user(
    id integer primary key AUTOINCREMENT,
    username text not null UNIQUE,
    email text,
    password text not null
);

create table board(
    id integer primary key AUTOINCREMENT,
    name text not null,
    moderator_id integer
);

create table post(
    id integer primary key AUTOINCREMENT,
    bid integer,
    title text not null,
    author_id integer,
    create_date datetime default (
        strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')
    ),
    content text not null
);

create table comment(
    id integer primary key AUTOINCREMENT,
    post_id integer,
    author_id integer,
    content text
);