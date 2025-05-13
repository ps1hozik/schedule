CREATE DATABASE schedule_db;
USE schedule_db;

CREATE TABLE subgroups (
    subgroup_name VARCHAR(22) NOT NULL,
    group_name VARCHAR(20) NOT NULL,
    course VARCHAR(1) NOT NULL,
    faculty_name VARCHAR(60) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    form VARCHAR(2) NOT NULL,
    PRIMARY KEY (subgroup_name, specialty)
);

CREATE TABLE pairs (
    week_day VARCHAR(11) NOT NULL,
    date DATE NOT NULL,
    number VARCHAR(1) NOT NULL,
    teacher VARCHAR(255),
    auditorium VARCHAR(255),
    name VARCHAR(300),
    subgroup_name VARCHAR(22) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    FOREIGN KEY (subgroup_name, specialty) REFERENCES subgroups (subgroup_name, specialty) ON DELETE CASCADE,
    UNIQUE (week_day, date, number, teacher, auditorium, name, subgroup_name, specialty)
);

CREATE TABLE exams_credits (
    week_day VARCHAR(11) NOT NULL,
    date DATE NOT NULL,
    teacher VARCHAR(255),
    auditorium VARCHAR(255),
    name VARCHAR(300),
    time VARCHAR(5),
    subgroup_name VARCHAR(22) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    FOREIGN KEY (subgroup_name, specialty) REFERENCES subgroups (subgroup_name, specialty) ON DELETE CASCADE,
    UNIQUE (week_day, date, name, subgroup_name, specialty)
);