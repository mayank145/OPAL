-- OPAL Database Setup Script
-- This script creates the database, user, and grants privileges

-- Create database
CREATE DATABASE IF NOT EXISTS opal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user with password
CREATE USER IF NOT EXISTS 'opal'@'localhost' IDENTIFIED BY 'opal_password';

-- Grant all privileges on opal database
GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

-- Show created user
SELECT user, host FROM mysql.user WHERE user = 'opal';

-- Show databases
SHOW DATABASES LIKE 'opal';

