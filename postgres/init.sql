-- ========================
-- TABLE DEFINITIONS
-- ========================

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

-- ========================
-- SEED PRODUCTS
-- ========================

INSERT INTO products (product_id, product_name, category, brand, price, stock, is_available, created_date) VALUES

-- Skincare - Somethinc
('SKC-A1B2C3D4', 'Hydrating Serum 30ml', 'Skincare', 'Somethinc', 189000, 80, TRUE, NOW()),
('SKC-B2C3D4E5', 'Niacinamide Serum 20ml', 'Skincare', 'Somethinc', 159000, 500, TRUE, NOW()),
('SKC-C3D4E5F6', 'Game Changer Eye Gel 20ml', 'Skincare', 'Somethinc', 175000, 150, TRUE, NOW()),
('SKC-D4E5F6A7', 'Ceramic Saviour Moisturizer 50ml', 'Skincare', 'Somethinc', 264000, 200, TRUE, NOW()),

-- Skincare - Skintific
('SKC-E5F6A7B8', '5X Ceramide Barrier Repair 30ml', 'Skincare', 'Skintific', 179000, 250, TRUE, NOW()),
('SKC-F6A7B8C9', 'Mugwort Anti Pores Mask 50ml', 'Skincare', 'Skintific', 248000, 100, TRUE, NOW()),
('SKC-A7B8C9D0', 'Salicylic Acid Anti Acne 20ml', 'Skincare', 'Skintific', 125000, 300, TRUE, NOW()),

-- Skincare - The Ordinary
('SKC-B8C9D0E1', 'AHA 30% BHA 2% Peeling 30ml', 'Skincare', 'The Ordinary', 245000, 150, TRUE, NOW()),
('SKC-C9D0E1F2', 'Niacinamide 10% Zinc 1% 30ml', 'Skincare', 'The Ordinary', 185000, 200, TRUE, NOW()),
('SKC-D0E1F2A3', 'Hyaluronic Acid 2% B5 30ml', 'Skincare', 'The Ordinary', 195000, 180, TRUE, NOW()),

-- Skincare - SK-II
('SKC-E1F2A3B4', 'Facial Treatment Essence 100ml', 'Skincare', 'SK-II', 3000000, 60, TRUE, NOW()),
('SKC-F2A3B4C5', 'Genoptics Aura Essence 50ml', 'Skincare', 'SK-II', 3200000, 50, TRUE, NOW()),
('SKC-A3B4C5D6', 'Skinpower Cream 50ml', 'Skincare', 'SK-II', 2880000, 40, TRUE, NOW()),

-- Skincare - Wardah
('SKC-B4C5D6E7', 'White Secret Brightening Essence 20ml', 'Skincare', 'Wardah', 89000, 600, TRUE, NOW()),
('SKC-C5D6E7F8', 'C-Defense Vitamin C Serum 20ml', 'Skincare', 'Wardah', 92000, 550, TRUE, NOW()),

-- Skincare - Scarlett
('SKC-D6E7F8A9', 'Brightly Ever After Serum 30ml', 'Skincare', 'Scarlett', 75000, 550, TRUE, NOW()),
('SKC-E7F8A9B0', 'Sunscreen Sunbright Daily 50ml', 'Skincare', 'Scarlett', 136000, 450, TRUE, NOW()),

-- Skincare - Emina
('SKC-F8A9B0C1', 'Sun Battle SPF 30 30ml', 'Skincare', 'Emina', 45000, 700, TRUE, NOW()),
('SKC-A9B0C1D2', 'Bright Stuff Face Wash 50ml', 'Skincare', 'Emina', 51000, 650, TRUE, NOW()),

-- Lipstik - Wardah
('LIP-A1B2C3D4', 'Exclusive Matte Lip Cream Nude', 'Lipstik', 'Wardah', 45000, 800, TRUE, NOW()),
('LIP-B2C3D4E5', 'Exclusive Matte Lip Cream Red', 'Lipstik', 'Wardah', 45000, 750, TRUE, NOW()),
('LIP-C3D4E5F6', 'Glasting Liquid Lip Pink', 'Lipstik', 'Wardah', 52000, 600, TRUE, NOW()),

-- Lipstik - Emina
('LIP-D4E5F6A7', 'Creamytint Coral', 'Lipstik', 'Emina', 32000, 750, TRUE, NOW()),
('LIP-E5F6A7B8', 'Magic Potion Lip Tint Berry', 'Lipstik', 'Emina', 28000, 700, TRUE, NOW()),

-- Lipstik - Chanel
('LIP-F6A7B8C9', 'Rouge Allure Velvet Rose', 'Lipstik', 'Chanel', 650000, 70, TRUE, NOW()),
('LIP-A7B8C9D0', 'Rouge Coco Bloom Mauve', 'Lipstik', 'Chanel', 700000, 60, TRUE, NOW()),

-- Lipstik - YSL
('LIP-B8C9D0E1', 'Rouge Pur Couture Red', 'Lipstik', 'YSL', 550000, 80, TRUE, NOW()),
('LIP-C9D0E1F2', 'Vinyl Cream Lip Stain Brown', 'Lipstik', 'YSL', 580000, 65, TRUE, NOW()),

-- Makeup - Wardah
('MKP-A1B2C3D4', 'Exclusive Two Way Cake', 'Makeup', 'Wardah', 65000, 500, TRUE, NOW()),
('MKP-B2C3D4E5', 'Instaperfect Cushion', 'Makeup', 'Wardah', 95000, 400, TRUE, NOW()),

-- Makeup - Emina
('MKP-C3D4E5F6', 'Bare With Me Mineral Cushion', 'Makeup', 'Emina', 55000, 600, TRUE, NOW()),
('MKP-D4E5F6A7', 'Cheek Lit Cream Blush Coral', 'Makeup', 'Emina', 45000, 550, TRUE, NOW()),

-- Makeup - Somethinc
('MKP-E5F6A7B8', 'Copy Paste Cushion', 'Makeup', 'Somethinc', 235000, 250, TRUE, NOW()),
('MKP-F6A7B8C9', 'Tamago Airy Blush Pink', 'Makeup', 'Somethinc', 175000, 200, TRUE, NOW()),

-- Haircare - Wardah
('HRC-A1B2C3D4', 'Hair Serum Anti Frizz 50ml', 'Haircare', 'Wardah', 55000, 500, TRUE, NOW()),
('HRC-B2C3D4E5', 'Anti Dandruff Shampoo 100ml', 'Haircare', 'Wardah', 35000, 700, TRUE, NOW()),

-- Parfum - Scarlett
('PRF-A1B2C3D4', 'Eau de Parfum Rose 50ml', 'Parfum', 'Scarlett', 150000, 200, TRUE, NOW()),
('PRF-B2C3D4E5', 'Dreamy EDP 30ml', 'Parfum', 'Scarlett', 155000, 180, TRUE, NOW()),

-- Parfum - Chanel
('PRF-C3D4E5F6', 'Chance Eau Tendre 50ml', 'Parfum', 'Chanel', 2500000, 25, TRUE, NOW()),
('PRF-D4E5F6A7', 'Bleu de Chanel 100ml', 'Parfum', 'Chanel', 6000000, 20, TRUE, NOW()),

-- Parfum - YSL
('PRF-E5F6A7B8', 'Black Opium EDP 50ml', 'Parfum', 'YSL', 2000000, 30, TRUE, NOW()),
('PRF-F6A7B8C9', 'Libre EDP 30ml', 'Parfum', 'YSL', 2860000, 25, TRUE, NOW())

ON CONFLICT (product_name, brand) DO NOTHING;