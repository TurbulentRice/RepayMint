CREATE DATABASE repaymint;
USE repaymint;
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE loans (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    start_balance DECIMAL(10, 2) NOT NULL,
    interest_rate DECIMAL(5, 4) NOT NULL,
    payment_amount DECIMAL(10, 2) NOT NULL,
    title VARCHAR(100) NOT NULL,
    term INT NOT NULL
);