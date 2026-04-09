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


INSERT INTO products (product_id, product_name, category, brand, price, stock, is_available, created_date) VALUES

-- Skincare
('SKC-001', 'Hydrating Serum 30ml', 'Skincare', 'Somethinc', 189000, 80, TRUE, NOW()),
('SKC-002', 'Niacinamide Serum 20ml', 'Skincare', 'Somethinc', 159000, 500, TRUE, NOW()),
('SKC-003', 'Moisture Bomb Toner', 'Skincare', 'Skintific', 135000, 300, TRUE, NOW()),
('SKC-004', '5X Ceramide Serum', 'Skincare', 'Skintific', 179000, 250, TRUE, NOW()),
('SKC-005', 'AHA BHA Peeling Solution', 'Skincare', 'The Ordinary', 245000, 150, TRUE, NOW()),
('SKC-006', 'Retinol 0.5% Serum', 'Skincare', 'The Ordinary', 220000, 100, TRUE, NOW()),
('SKC-007', 'Facial Treatment Essence', 'Skincare', 'SK-II', 1500000, 60, TRUE, NOW()),
('SKC-008', 'Genoptics Aura Essence', 'Skincare', 'SK-II', 2000000, 50, TRUE, NOW()),
('SKC-009', 'Creme de la Mer Moisturizer', 'Skincare', 'La Mer', 3000000, 30, TRUE, NOW()),
('SKC-010', 'Regenerating Serum', 'Skincare', 'La Mer', 5000000, 20, TRUE, NOW()),
('SKC-011', 'White Glow Serum', 'Skincare', 'Wardah', 89000, 600, TRUE, NOW()),
('SKC-012', 'Acne Sunscreen SPF50', 'Skincare', 'Emina', 55000, 700, TRUE, NOW()),
('SKC-013', 'Brightening Moisturizer', 'Skincare', 'Scarlett', 75000, 550, TRUE, NOW()),
('SKC-014', 'Sunscreen Matte SPF45', 'Skincare', 'Scarlett', 85000, 450, TRUE, NOW()),
('SKC-015', 'First Essence Treatment', 'Skincare', 'Sulwhasoo', 750000, 40, TRUE, NOW()),

-- Lipstik & Lip Care
('LIP-001', 'Exclusive Lip Color', 'Lipstik', 'Wardah', 45000, 800, TRUE, NOW()),
('LIP-002', 'Matte Lip Cream', 'Lipstik', 'Emina', 40000, 750, TRUE, NOW()),
('LIP-003', 'Soft Matte Lip Cream', 'Lipstik', 'NYX', 120000, 400, TRUE, NOW()),
('LIP-004', 'Powder Kiss Lipstick', 'Lipstik', 'MAC', 350000, 200, TRUE, NOW()),
('LIP-005', 'Rouge Allure Velvet', 'Lipstik', 'Chanel', 650000, 70, TRUE, NOW()),
('LIP-006', 'Lip Sleeping Mask', 'Lip Care', 'Laneige', 250000, 300, TRUE, NOW()),
('LIP-007', 'Lip Gloss Plumping', 'Lip Care', 'Emina', 35000, 600, TRUE, NOW()),

-- Makeup
('MKP-001', 'Two Way Cake', 'Makeup', 'Wardah', 65000, 500, TRUE, NOW()),
('MKP-002', 'BB Cream SPF30', 'Makeup', 'Emina', 50000, 600, TRUE, NOW()),
('MKP-003', 'Fit Me Foundation', 'Makeup', 'Maybelline', 145000, 350, TRUE, NOW()),
('MKP-004', 'Stay Matte Foundation', 'Makeup', 'NYX', 180000, 250, TRUE, NOW()),
('MKP-005', 'Pro Filtir Foundation', 'Makeup', 'Fenty Beauty', 650000, 90, TRUE, NOW()),
('MKP-006', 'Lasting Perfection Concealer', 'Makeup', 'Collection', 120000, 300, TRUE, NOW()),
('MKP-007', 'Naked Eyeshadow Palette', 'Makeup', 'Urban Decay', 850000, 55, TRUE, NOW()),

-- Haircare
('HRC-001', 'Hair Serum Anti Frizz', 'Haircare', 'Wardah', 55000, 500, TRUE, NOW()),
('HRC-002', 'Hijab Fresh Shampoo', 'Haircare', 'Wardah', 35000, 700, TRUE, NOW()),
('HRC-003', 'Total Repair Shampoo', 'Haircare', 'Loreal', 75000, 600, TRUE, NOW()),
('HRC-004', 'Extraordinary Oil Serum', 'Haircare', 'Loreal', 150000, 350, TRUE, NOW()),
('HRC-005', 'Scalp Treatment Tonic', 'Haircare', 'Sulwhasoo', 500000, 80, TRUE, NOW()),

-- Parfum
('PRF-001', 'Eau de Parfum Rose', 'Parfum', 'Scarlett', 150000, 200, TRUE, NOW()),
('PRF-002', 'Body Mist Fresh', 'Parfum', 'Emina', 55000, 500, TRUE, NOW()),
('PRF-003', 'Chance Eau Tendre', 'Parfum', 'Chanel', 2500000, 25, TRUE, NOW()),
('PRF-004', 'Black Opium EDP', 'Parfum', 'YSL', 2000000, 30, TRUE, NOW())

ON CONFLICT (product_id) DO NOTHING;