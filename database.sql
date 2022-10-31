create Table todos(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    status boolean,
    time timestamp
);