from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime
from pendulum import timezone
import random
import uuid

# (nama_produk, harga_base)
BRAND_PRODUCT_MAP = {
    "Somethinc": {
        "Skincare": [
            ("Hydrating Serum", 189000),
            ("Niacinamide Serum", 159000),
            ("Game Changer Eye Gel", 175000),
            ("Lemonade Waterless Vitamin C", 195000),
            ("Bakuchiol Skinpair Oil", 215000),
            ("Supple Power Essence", 185000),
            ("Ceramic Saviour Moisturizer", 165000),
            ("Low pH Jelly Cleanser", 145000),
        ],
        "Makeup": [
            ("Copy Paste Cushion", 235000),
            ("Hooman Undercontrol Powder", 185000),
            ("Badass Breathable Foundation", 245000),
            ("DNA Airbrush Powder Foundation", 255000),
            ("Tamago Airy Blush", 175000),
            ("Checkmatte Lipstick", 155000),
        ],
    },
    "Skintific": {
        "Skincare": [
            ("5X Ceramide Barrier Repair", 179000),
            ("Mugwort Anti Pores Mask", 155000),
            ("Glycolic Acid Clarifying Toner", 145000),
            ("10% Niacinamide Brightening", 135000),
            ("Salicylic Acid Anti Acne", 125000),
            ("Symwhite 377 Dark Spot", 165000),
            ("Panthenol Gel Moisturizer", 135000),
            ("Invisible Sunscreen Stick", 145000),
        ]
    },
    "The Ordinary": {
        "Skincare": [
            ("AHA 30% BHA 2% Peeling", 245000),
            ("Niacinamide 10% Zinc 1%", 185000),
            ("Hyaluronic Acid 2% B5", 195000),
            ("Caffeine Solution 5% EGCG", 215000),
            ("Natural Moisturizing Factors", 175000),
            ("Squalane Cleanser", 195000),
            ("Glycolic Acid 7% Toning", 185000),
            ("Argireline Solution 10%", 225000),
        ]
    },
    "Wardah": {
        "Skincare": [
            ("White Secret Brightening Essence", 89000),
            ("Crystal Secret Dark Spot", 95000),
            ("Hydra Rose Serum", 85000),
            ("Lightening Day Gel", 75000),
            ("Renew You Anti Aging Cream", 99000),
            ("C-Defense Vitamin C Serum", 92000),
        ],
        "Lipstik": [
            ("Exclusive Matte Lip Cream", 45000),
            ("Glasting Liquid Lip", 52000),
            ("Colorfit Velvet Matte", 48000),
            ("Everyday Cheek And Lip Tint", 42000),
            ("Matte Foundation Lipstick", 55000),
        ],
        "Makeup": [
            ("Exclusive Two Way Cake", 65000),
            ("Colorfit Powder Foundation", 72000),
            ("Luminous Face Powder", 68000),
            ("Instaperfect Cushion", 95000),
            ("Eyebrow Pencil Brown", 35000),
        ],
        "Haircare": [
            ("Anti Dandruff Shampoo", 35000),
            ("Hair Fall Treatment", 55000),
            ("Hair Serum Anti Frizz", 55000),
            ("Nutri Shine Shampoo", 38000),
            ("Hijab Fresh Conditioner", 42000),
        ],
    },
    "Emina": {
        "Skincare": [
            ("Bright Stuff Face Wash", 32000),
            ("Ms Pimple Acne Gel", 28000),
            ("Sun Battle SPF 30", 45000),
            ("Skin Buddy Micellar Water", 38000),
            ("Aloe Vera Gel", 25000),
            ("Glossy Stain Serum", 42000),
        ],
        "Lipstik": [
            ("Creamytint", 32000),
            ("Magic Potion Lip Tint", 28000),
            ("Poppin Matte", 35000),
            ("Sugar Rush Lipstick", 30000),
            ("Lip Cushion", 38000),
        ],
        "Makeup": [
            ("Bare With Me Mineral Cushion", 55000),
            ("City Chic CC Cake", 48000),
            ("Daily Matte Powder", 42000),
            ("Cheek Lit Cream Blush", 45000),
            ("Squeeze Me Up Mascara", 38000),
        ],
    },
    "SK-II": {
        "Skincare": [
            ("Facial Treatment Essence", 1500000),
            ("Genoptics Aura Essence", 2000000),
            ("Skinpower Cream", 1800000),
            ("Facial Treatment Clear Lotion", 1200000),
            ("RNA New Age Cream", 2200000),
            ("Mid-Day Miracle Essence", 1650000),
        ]
    },
    "Chanel": {
        "Parfum": [
            ("Chance Eau Tendre", 2500000),
            ("Bleu de Chanel", 3000000),
            ("N5 Eau de Parfum", 3500000),
            ("Coco Mademoiselle", 2800000),
            ("Allure Homme Sport", 2200000),
        ],
        "Lipstik": [
            ("Rouge Allure Velvet", 650000),
            ("Rouge Coco Bloom", 700000),
            ("Le Rouge Duo Ultra", 720000),
            ("Rouge Pur Couture", 680000),
            ("Rouge Allure Ink", 660000),
        ],
    },
    "YSL": {
        "Parfum": [
            ("Black Opium EDP", 2000000),
            ("Libre EDP", 2200000),
            ("Mon Paris", 1800000),
            ("Y Le Parfum", 2500000),
            ("L Homme", 1900000),
        ],
        "Lipstik": [
            ("Rouge Pur Couture", 550000),
            ("Vinyl Cream Lip Stain", 580000),
            ("Slim Velvet Radical", 600000),
            ("Tatouage Couture", 570000),
            ("Candy Glaze", 520000),
        ],
    },
    "Scarlett": {
        "Skincare": [
            ("Brightly Ever After Serum", 75000),
            ("Acne Serum", 65000),
            ("Glowtening Serum", 72000),
            ("7X Ceramide Moisturizer", 79000),
            ("Sunscreen Sunbright Daily", 85000),
            ("Peeling So Good", 68000),
        ],
        "Parfum": [
            ("Eau de Parfum Rose", 150000),
            ("Dreamy EDP", 155000),
            ("Sweet Memories", 145000),
            ("Euphoria EDP", 160000),
            ("Passion EDP", 158000),
        ],
    },
}

SIZE_OPTIONS = ["20ml", "30ml", "50ml", "100ml"]
SIZE_MULTIPLIER = {"20ml": 1.0, "30ml": 1.3, "50ml": 1.6, "100ml": 2.0}

WARNA_OPTIONS = ["Red", "Nude", "Pink", "Coral", "Brown", "Mauve", "Berry", "Rose"]

PREFIX = {
    "Skincare": "SKC",
    "Lipstik": "LIP",
    "Makeup": "MKP",
    "Haircare": "HRC",
    "Parfum": "PRF",
    "Lip Care": "LPC",
}


def hitung_harga(base_price, size=None):
    multiplier = SIZE_MULTIPLIER.get(size, 1.0)
    return round((base_price * multiplier) / 5000) * 5000


def generate_product(existing_ids, existing_combos):
    brand = random.choice(list(BRAND_PRODUCT_MAP.keys()))
    category = random.choice(list(BRAND_PRODUCT_MAP[brand].keys()))
    pfx = PREFIX.get(category)
    if not pfx:
        return None

    base_name, base_price = random.choice(BRAND_PRODUCT_MAP[brand][category])

    # tambah size untuk skincare, parfum, haircare
    if category in ["Skincare", "Parfum", "Haircare"]:
        size = random.choice(SIZE_OPTIONS)
        product_name = f"{base_name} {size}"
        price = hitung_harga(base_price, size)
    # tambah warna untuk lipstik & makeup
    elif category in ["Lipstik", "Makeup"]:
        warna = random.choice(WARNA_OPTIONS)
        product_name = f"{base_name} {warna}"
        price = base_price
    else:
        product_name = base_name
        price = base_price

    if (product_name, brand) in existing_combos:
        return None

    product_id = f"{pfx}-{uuid.uuid4().hex[:8].upper()}"
    if product_id in existing_ids:
        return None

    return (
        product_id,
        product_name,
        category,
        brand,
        int(price),
        random.randint(50, 200),
        True,
        datetime.now(),
    )


def insert_products():
    pg = PostgresHook(postgres_conn_id="postgres_ecommerce")
    conn = pg.get_conn()
    cursor = conn.cursor()

    # restock produk yang habis
    cursor.execute(
        """
        UPDATE products
        SET stock = 100, is_available = TRUE
        WHERE stock = 0
    """
    )

    # tambah 50% stok untuk produk yang hampir habis
    cursor.execute(
        """
        UPDATE products
        SET stock = stock + CEIL(stock * 0.5)::INT,
            is_available = TRUE
        WHERE stock > 0 AND stock <= 50
    """
    )

    # ambil data existing buat cek duplikat
    cursor.execute("SELECT product_id, product_name, brand FROM products")
    rows = cursor.fetchall()
    existing_ids = {r[0] for r in rows}
    existing_combos = {(r[1], r[2]) for r in rows}

    # generate & insert produk baru
    new_products = []
    for _ in range(random.randint(3, 5)):
        p = generate_product(existing_ids, existing_combos)
        if p:
            new_products.append(p)
            existing_ids.add(p[0])
            existing_combos.add((p[1], p[3]))

    if new_products:
        sql = """
            INSERT INTO products (product_id, product_name, category, brand, price, stock, is_available, created_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_name, brand) DO NOTHING
        """
        cursor.executemany(sql, new_products)
        print(f"Berhasil insert {len(new_products)} produk baru.")

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    dag_id="dag_insert_products",
    start_date=datetime(2026, 4, 1, tzinfo=timezone("Asia/Jakarta")),
    schedule_interval="@hourly",
    catchup=False,
    tags=["batch", "products"],
) as dag:

    task_insert_products = PythonOperator(
        task_id="insert_products",
        python_callable=insert_products,
    )
