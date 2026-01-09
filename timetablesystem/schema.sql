CREATE DATABASE timetable_db;
USE timetable_db;

CREATE TABLE faculty (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  department VARCHAR(100)
);

CREATE TABLE timetable (
  id INT AUTO_INCREMENT PRIMARY KEY,
  day VARCHAR(20),
  period INT,
  subject VARCHAR(100),
  faculty VARCHAR(100),
  room VARCHAR(50)
);