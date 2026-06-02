CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE operations (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    sum NUMERIC(12, 2) NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id),
    type_operation VARCHAR NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id)
);