from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime
import random
import uuid

BRAND_PRODUCT_MAP = {
    "Somethinc": {
        "Skincare": [
            "Hydrating Serum",
            "Niacinamide Serum",
            "Game Changer Eye Gel",
            "Lemonade Waterless Vitamin C",
            "Bakuchiol Skinpair Oil",
            "Supple Power Essence",
            "Ceramic Saviour Moisturizer",
            "Low pH Jelly Cleanser",
        ],
        "Makeup": [
            "Copy Paste Cushion",
            "Hooman Undercontrol Powder",
            "Badass Breathable Foundation",
            "DNA Airbrush Powder Foundation",
            "Tamago Airy Blush",
            "Checkmatte Lipstick",
        ],
    },
    "Skintific": {
        "Skincare": [
            "5X Ceramide Barrier Repair",
            "Mugwort Anti Pores Mask",
            "Glycolic Acid Clarifying Toner",
            "10% Niacinamide Brightening",
            "Salicylic Acid Anti Acne",
            "Symwhite 377 Dark Spot",
            "Panthenol Gel Moisturizer",
            "Invisible Sunscreen Stick",
        ]
    },
    "The Ordinary": {
        "Skincare": [
            "AHA 30% BHA 2% Peeling",
            "Niacinamide 10% Zinc 1%",
            "Hyaluronic Acid 2% B5",
            "Caffeine Solution 5% EGCG",
            "Natural Moisturizing Factors",
            "Squalane Cleanser",
            "Glycolic Acid 7% Toning",
            "Argireline Solution 10%",
        ]
    },
    "Wardah": {
        "Skincare": [
            "White Secret Brightening Essence",
            "Crystal Secret Dark Spot",
            "Hydra Rose Serum",
            "Lightening Day Gel",
            "Renew You Anti Aging Cream",
            "C-Defense Vitamin C Serum",
        ],
        "Lipstik": [
            "Exclusive Matte Lip Cream",
            "Glasting Liquid Lip",
            "Colorfit Velvet Matte",
            "Everyday Cheek And Lip Tint",
            "Matte Foundation Lipstick",
        ],
        "Makeup": [
            "Exclusive Two Way Cake",
            "Colorfit Powder Foundation",
            "Luminous Face Powder",
            "Instaperfect Cushion",
            "Eyebrow Pencil Brown",
        ],
        "Haircare": [
            "Anti Dandruff Shampoo",
            "Hair Fall Treatment",
            "Hair Serum Anti Frizz",
            "Nutri Shine Shampoo",
            "Hijab Fresh Conditioner",
        ],
    },
    "Emina": {
        "Skincare": [
            "Bright Stuff Face Wash",
            "Ms Pimple Acne Gel",
            "Sun Battle SPF 30",
            "Skin Buddy Micellar Water",
            "Aloe Vera Gel",
            "Glossy Stain Serum",
        ],
        "Lipstik": [
            "Creamytint",
            "Magic Potion Lip Tint",
            "Poppin Matte",
            "Sugar Rush Lipstick",
            "Lip Cushion",
        ],
        "Makeup": [
            "Bare With Me Mineral Cushion",
            "City Chic CC Cake",
            "Daily Matte Powder",
            "Cheek Lit Cream Blush",
            "Squeeze Me Up Mascara",
        ],
    },
    "SK-II": {
        "Skincare": [
            "Facial Treatment Essence",
            "Genoptics Aura Essence",
            "Skinpower Cream",
            "Facial Treatment Clear Lotion",
            "RNA New Age Cream",
            "Mid-Day Miracle Essence",
        ]
    },
    "Chanel": {
        "Parfum": [
            "Chance Eau Tendre",
            "Bleu de Chanel",
            "N°5 Eau de Parfum",
            "Coco Mademoiselle",
            "Allure Homme Sport",
        ],
        "Lipstik": [
            "Rouge Allure Velvet",
            "Rouge Coco Bloom",
            "Le Rouge Duo Ultra",
            "Rouge Pur Couture",
            "Rouge Allure Ink",
        ],
    },
    "YSL": {
        "Parfum": [
            "Black Opium EDP",
            "Libre EDP",
            "Mon Paris",
            "Y Le Parfum",
            "L'Homme",
        ],
        "Lipstik": [
            "Rouge Pur Couture",
            "Vinyl Cream Lip Stain",
            "Slim Velvet Radical",
            "Tatouage Couture",
            "Candy Glaze",
        ],
    },
    "Scarlett": {
        "Skincare": [
            "Brightly Ever After Serum",
            "Acne Serum",
            "Glowtening Serum",
            "7X Ceramide Moisturizer",
            "Sunscreen Sunbright Daily",
            "Peeling So Good",
        ],
        "Parfum": [
            "Eau de Parfum Rose",
            "Dreamy EDP",
            "Sweet Memories",
            "Euphoria EDP",
            "Passion EDP",
        ],
    },
}


PRICE_RULES = {
    "SK-II": {"Skincare": (1500000, 2500000)},
    "Chanel": {"Parfum": (2000000, 5000000), "Lipstik": (600000, 800000)},
    "YSL": {"Parfum": (1500000, 3500000), "Lipstik": (500000, 800000)},
    "Wardah": {
        "Skincare": (40000, 100000),
        "Lipstik": (35000, 65000),
        "Makeup": (55000, 110000),
        "Haircare": (35000, 70000),
    },
    "Somethinc": {"Skincare": (110000, 260000), "Makeup": (130000, 260000)},
    "Skintific": {"Skincare": (125000, 250000)},
    "The Ordinary": {"Skincare": (180000, 350000)},
    "Emina": {
        "Skincare": (30000, 60000),
        "Lipstik": (30000, 55000),
        "Makeup": (35000, 65000),
    },
    "Scarlett": {"Skincare": (65000, 95000), "Parfum": (120000, 190000)},
}


PREFIX = {
    "Skincare": "SKC",
    "Lipstik": "LIP",
    "Makeup": "MKP",
    "Haircare": "HRC",
    "Parfum": "PRF",
    "Lip Care": "LPC",
}


def generate_product(existing_ids, existing_combos):
    brand = random.choice(list(BRAND_PRODUCT_MAP.keys()))
    category = random.choice(list(BRAND_PRODUCT_MAP[brand].keys()))

    pfx = PREFIX.get(category)
    if not pfx:
        return None

    base_name = random.choice(BRAND_PRODUCT_MAP[brand][category])

    size = (
        random.choice(["20ml", "30ml", "50ml", "100ml"])
        if category in ["Skincare", "Parfum", "Haircare"]
        else ""
    )
    product_name = f"{base_name} {size}".strip()

    if (product_name, brand) in existing_combos:
        return None

    # ID: PREFIX-8CHAR
    product_id = f"{pfx}-{uuid.uuid4().hex[:8].upper()}"
    if product_id in existing_ids:
        return None

    price_range = PRICE_RULES.get(brand, {}).get(category, (50000, 150000))
    price = round(random.randint(*price_range) / 5000) * 5000

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


def insert_product_job():
    hook = PostgresHook(postgres_conn_id="postgres_ecommerce")
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("UPDATE products SET is_available = FALSE WHERE stock = 0")

    cursor.execute(
        "UPDATE products SET stock = 100, is_available = TRUE WHERE stock = 0"
    )

    cursor.execute(
        """
        UPDATE products 
        SET stock = stock + CEIL(stock * 0.5), 
            is_available = TRUE 
        WHERE stock > 0 AND stock <= 50
    """
    )

    cursor.execute("SELECT product_id, product_name, brand FROM products")
    rows = cursor.fetchall()
    existing_ids = {r[0] for r in rows}
    existing_combos = {(r[1], r[2]) for r in rows}

    new_products = []
    for _ in range(random.randint(2, 5)):
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

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    dag_id="dag_insert_products",
    start_date=datetime(2026, 4, 1),
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    PythonOperator(task_id="insert_products", python_callable=insert_product_job)
