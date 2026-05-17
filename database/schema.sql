DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS merchant;

CREATE TABLE merchant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    contact TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    original_price INTEGER,
    discount_price INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    image_url TEXT,
    pickup_time TEXT NOT NULL,
    status TEXT DEFAULT '上架',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(merchant_id) REFERENCES merchant(id) ON DELETE CASCADE
);

-- Insert dummy data for MVP testing
INSERT INTO merchant (name, address, contact) VALUES ('好呷便當', '學區勝利路 1 號', '0912345678');
INSERT INTO merchant (name, address, contact) VALUES ('天天麵包', '學區大學路 20 號', '0987654321');

INSERT INTO product (merchant_id, name, type, original_price, discount_price, quantity, image_url, pickup_time) 
VALUES (1, '排骨便當 (微冷)', '便當', 100, 50, 3, '', '17:30 - 18:30');
INSERT INTO product (merchant_id, name, type, original_price, discount_price, quantity, image_url, pickup_time) 
VALUES (2, '隔夜波蘿麵包', '麵包', 35, 15, 10, '', '15:00 - 19:00');
