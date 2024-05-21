-- Добавление типов аккаунтов
INSERT INTO types_users (name) VALUES ('Administrator');
INSERT INTO types_users (name) VALUES ('Master');
INSERT INTO types_users (name) VALUES ('Manager');
INSERT INTO types_users (name) VALUES ('Customers');

-- Добавление аккаунтов для каждого типа
INSERT INTO users (login, password, type_id) VALUES ('admin', 'admin_password', 1); -- Администратор
INSERT INTO users (login, password, type_id) VALUES ('master', 'master_password', 2); -- Мастер
INSERT INTO users (login, password, type_id) VALUES ('manager', 'manager_password', 3); -- Менеджер
INSERT INTO users (login, password, type_id) VALUES ('client', 'client_password', 4); -- Клиент

-- Добавление видов статусов
INSERT INTO statuses (name) VALUES ('В ожидании');
INSERT INTO statuses (name) VALUES ('В работе');
INSERT INTO statuses (name) VALUES ('Выполнено');

-- Добавление инструментария
INSERT INTO tools (name) VALUES ('Паяльная станция');
INSERT INTO tools (name) VALUES ('Ремонтный фен');
INSERT INTO tools (name) VALUES ('Диагностическая станция');

-- Добавление типов устройств 
INSERT INTO types_devices (name) VALUES ('Смартфон');
INSERT INTO types_devices (name) VALUES ('Стиральная машина');
INSERT INTO types_devices (name) VALUES ('Ноутбук');
INSERT INTO types_devices (name) VALUES ('Пылесос');
