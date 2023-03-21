-- Prepares a MySQL Test Server for the project
-- Database TheHospitalHub_test_db
-- User hbnb_test with password thehospitalhub
-- Grants all privileges for hub_test on TheHospitalHub_test_db
-- Grants SELECT privileges for hub_test on performance schema

CREATE DATABASE IF NOT EXISTS TheHospitalHub_test_db;
CREATE USER IF NOT EXISTS 'TheHospitalHub_test'@'localhost' IDENTIFIED BY 'thehospitalhub';
GRANT ALL PRIVILEGES ON `TheHospitalHub_test_db`.* TO 'TheHospitalHub_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'TheHospitalHub_test'@'localhost';
FLUSH PRIVILEGES;
