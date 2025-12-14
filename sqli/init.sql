CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Target to find: password is 'A_Secret_Password_123'
INSERT INTO users (username, password) VALUES ('admin', SHA2('A_Secret_Password_123', 256));
INSERT INTO users (username, password) VALUES ('guest', SHA2('simple', 256));
