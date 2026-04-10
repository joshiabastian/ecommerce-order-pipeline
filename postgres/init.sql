CREATE TABLE IF NOT EXISTS users (
    user_id      VARCHAR(50) PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    address      TEXT,
    city         VARCHAR(50),
    age          INT,
    gender       VARCHAR(20),
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
    created_date TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (product_name, brand)
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



INSERT INTO products (product_id, product_name, category, brand, price, stock, is_available, created_date) VALUES

-- Skincare
('SKC-a1b2c3d4', 'Hydrating Serum 30ml', 'Skincare', 'Somethinc', 189000, 80, TRUE, NOW()),
('SKC-b2c3d4e5', 'Niacinamide Serum 20ml', 'Skincare', 'Somethinc', 159000, 500, TRUE, NOW()),
('SKC-c3d4e5f6', 'Moisture Bomb Toner', 'Skincare', 'Skintific', 135000, 300, TRUE, NOW()),
('SKC-d4e5f6a7', '5X Ceramide Serum', 'Skincare', 'Skintific', 179000, 250, TRUE, NOW()),
('SKC-e5f6a7b8', 'AHA BHA Peeling Solution', 'Skincare', 'The Ordinary', 245000, 150, TRUE, NOW()),
('SKC-f6a7b8c9', 'Retinol 0.5% Serum', 'Skincare', 'The Ordinary', 220000, 100, TRUE, NOW()),
('SKC-a7b8c9d0', 'Facial Treatment Essence', 'Skincare', 'SK-II', 1500000, 60, TRUE, NOW()),
('SKC-b8c9d0e1', 'Genoptics Aura Essence', 'Skincare', 'SK-II', 2000000, 50, TRUE, NOW()),
('SKC-c9d0e1f2', 'Creme de la Mer Moisturizer', 'Skincare', 'La Mer', 3000000, 30, TRUE, NOW()),
('SKC-d0e1f2a3', 'Regenerating Serum', 'Skincare', 'La Mer', 5000000, 20, TRUE, NOW()),
('SKC-e1f2a3b4', 'White Glow Serum', 'Skincare', 'Wardah', 89000, 600, TRUE, NOW()),
('SKC-f2a3b4c5', 'Acne Sunscreen SPF50', 'Skincare', 'Emina', 55000, 700, TRUE, NOW()),
('SKC-a3b4c5d6', 'Brightening Moisturizer', 'Skincare', 'Scarlett', 75000, 550, TRUE, NOW()),
('SKC-b4c5d6e7', 'Sunscreen Matte SPF45', 'Skincare', 'Scarlett', 85000, 450, TRUE, NOW()),
('SKC-c5d6e7f8', 'First Essence Treatment', 'Skincare', 'Sulwhasoo', 750000, 40, TRUE, NOW()),

-- Lipstik
('LIP-a1b2c3d4', 'Exclusive Lip Color', 'Lipstik', 'Wardah', 45000, 800, TRUE, NOW()),
('LIP-b2c3d4e5', 'Matte Lip Cream', 'Lipstik', 'Emina', 40000, 750, TRUE, NOW()),
('LIP-c3d4e5f6', 'Soft Matte Lip Cream', 'Lipstik', 'NYX', 120000, 400, TRUE, NOW()),
('LIP-d4e5f6a7', 'Powder Kiss Lipstick', 'Lipstik', 'MAC', 350000, 200, TRUE, NOW()),
('LIP-e5f6a7b8', 'Rouge Allure Velvet', 'Lipstik', 'Chanel', 650000, 70, TRUE, NOW()),

-- Lip Care
('LPC-a1b2c3d4', 'Lip Sleeping Mask', 'Lip Care', 'Laneige', 250000, 300, TRUE, NOW()),
('LPC-b2c3d4e5', 'Lip Gloss Plumping', 'Lip Care', 'Emina', 35000, 600, TRUE, NOW()),

-- Makeup
('MKP-a1b2c3d4', 'Two Way Cake', 'Makeup', 'Wardah', 65000, 500, TRUE, NOW()),
('MKP-b2c3d4e5', 'BB Cream SPF30', 'Makeup', 'Emina', 50000, 600, TRUE, NOW()),
('MKP-c3d4e5f6', 'Fit Me Foundation', 'Makeup', 'Maybelline', 145000, 350, TRUE, NOW()),
('MKP-d4e5f6a7', 'Stay Matte Foundation', 'Makeup', 'NYX', 180000, 250, TRUE, NOW()),
('MKP-e5f6a7b8', 'Pro Filtir Foundation', 'Makeup', 'Fenty Beauty', 650000, 90, TRUE, NOW()),
('MKP-f6a7b8c9', 'Lasting Perfection Concealer', 'Makeup', 'Collection', 120000, 300, TRUE, NOW()),
('MKP-a7b8c9d0', 'Naked Eyeshadow Palette', 'Makeup', 'Urban Decay', 850000, 55, TRUE, NOW()),

-- Haircare
('HRC-a1b2c3d4', 'Hair Serum Anti Frizz', 'Haircare', 'Wardah', 55000, 500, TRUE, NOW()),
('HRC-b2c3d4e5', 'Hijab Fresh Shampoo', 'Haircare', 'Wardah', 35000, 700, TRUE, NOW()),
('HRC-c3d4e5f6', 'Total Repair Shampoo', 'Haircare', 'Loreal', 75000, 600, TRUE, NOW()),
('HRC-d4e5f6a7', 'Extraordinary Oil Serum', 'Haircare', 'Loreal', 150000, 350, TRUE, NOW()),
('HRC-e5f6a7f8', 'Scalp Treatment Tonic', 'Haircare', 'Sulwhasoo', 500000, 80, TRUE, NOW()),

-- Parfum
('PRF-a1b2c3d4', 'Eau de Parfum Rose', 'Parfum', 'Scarlett', 150000, 200, TRUE, NOW()),
('PRF-b2c3d4e5', 'Body Mist Fresh', 'Parfum', 'Emina', 55000, 500, TRUE, NOW()),
('PRF-c3d4e5f6', 'Chance Eau Tendre', 'Parfum', 'Chanel', 2500000, 25, TRUE, NOW()),
('PRF-d4e5f6a7', 'Black Opium EDP', 'Parfum', 'YSL', 2000000, 30, TRUE, NOW())

ON CONFLICT (product_name, brand) DO NOTHING;