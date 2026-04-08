CREATE DATABASE airflow_db;
CREATE TABLE IF NOT EXISTS users (
    user_id      VARCHAR(50) PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    address      TEXT,
    city         VARCHAR(50),
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    product_id   VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(50) NOT NULL,
    brand        VARCHAR(50),
    price        NUMERIC(15, 2) NOT NULL,
    stock        INT NOT NULL DEFAULT 0,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    created_date TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    order_id       VARCHAR(50) PRIMARY KEY,
    user_id        VARCHAR(50) NOT NULL REFERENCES users(user_id),
    product_id     VARCHAR(50) NOT NULL REFERENCES products(product_id),
    quantity       INT NOT NULL,
    amount         NUMERIC(15, 2) NOT NULL,
    country        VARCHAR(10) NOT NULL,
    city           VARCHAR(50),
    payment_method VARCHAR(30),
    device         VARCHAR(20),
    created_date   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_date   TIMESTAMP,
    status         VARCHAR(10) NOT NULL CHECK (status IN ('genuine', 'frauds'))
);