-- Prepares a MySQL Development Server for the project
-- Database TheHospitalHub_dev_db
-- User hbnb_dev with password thehospitalhub
-- Grants all privileges for hub_dev on TheHospitalHub_dev_db
-- Grants SELECT privileges for TheHospitalHub_dev on performance schema

CREATE DATABASE IF NOT EXISTS TheHospitalHub_dev_db;
CREATE USER IF NOT EXISTS 'TheHospitalHub_dev'@'localhost' IDENTIFIED BY 'thehospitalhub';
GRANT ALL PRIVILEGES ON `hub_dev_db`.* TO 'TheHospitalHub_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'TheHospitalHub_dev'@'localhost';
FLUSH PRIVILEGES;
