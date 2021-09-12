
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS learners;
CREATE TABLE learners (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    name VARCHAR (32), category VARCHAR (32));

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    name VARCHAR (32), category VARCHAR (32));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
