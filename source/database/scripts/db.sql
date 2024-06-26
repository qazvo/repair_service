CREATE TABLE types_devices (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255)
);

CREATE TABLE statuses(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(40)
);

CREATE TABLE devices (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER REFERENCES types_devices(id) ON DELETE CASCADE ON UPDATE CASCADE,
    model VARCHAR(255),
    serial_number VARCHAR(255)
);

CREATE TABLE customers (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    FIO VARCHAR(255),
    address VARCHAR(255),
    number_phone VARCHAR(20),
    email VARCHAR(255),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE posts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255)
);

CREATE TABLE employees (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    FIO VARCHAR(255),
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE appeals (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE,
    device_id INTEGER REFERENCES devices(id) ON DELETE CASCADE ON UPDATE CASCADE,
    description VARCHAR(255)
);

CREATE TABLE claims (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    appeal_id INTEGER REFERENCES appeals(id) ON DELETE CASCADE ON UPDATE CASCADE,
    start_date DATETIME,
    end_date DATETIME,
    status_id INTEGER REFERENCES statuses(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE contracts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    employee_id REFERENCES employees(id) ON DELETE CASCADE ON UPDATE CASCADE,
    claim_id REFERENCES claims(id) ON DELETE CASCADE ON UPDATE CASCADE,
    description_work_done VARCHAR(255),
    cost DECIMAL(10, 2)
);

CREATE TABLE types_users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255)
);

CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(255),
    password VARCHAR(255),
    type_id REFERENCES types_users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE components (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255)
);

CREATE TABLE components_used (
    contract_id INTEGER REFERENCES contracts(id) ON DELETE CASCADE ON UPDATE CASCADE,
    component_id INTEGER REFERENCES components(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TRIGGER IF NOT EXISTS set_start_date
    AFTER INSERT ON claims
    FOR EACH ROW
    BEGIN
        UPDATE claims
        SET start_date = datetime('now')
        WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_end_date
    AFTER UPDATE OF status_id ON claims
    WHEN NEW.status_id = (SELECT id FROM statuses WHERE name = 'Выполнено')
    BEGIN
        UPDATE claims
        SET end_date = datetime('now')
        WHERE id = NEW.id;
    END;

CREATE TRIGGER set_default_status_on_insert
    AFTER INSERT ON claims
    FOR EACH ROW
    BEGIN
        UPDATE claims
        SET status_id = (SELECT id FROM statuses WHERE name = 'В ожидании')
        WHERE id = NEW.id;
    END;