CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    image_file TEXT,
    image_file_name TEXT,
    title TEXT,
    message TEXT,
    user_id INTEGER REFERENCES users,
    board_name TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    image_file TEXT,
    image_file_name TEXT,
    title TEXT,
    message TEXT,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    sent_at TIMESTAMP
);