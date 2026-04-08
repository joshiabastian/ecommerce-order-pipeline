from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from faker import Faker
from datetime import datetime
from pendulum import timezone
import random
import uuid

fake = Faker("id_ID")

# mapping kategori → brand & nama
kategori_produk = {
    "Elektronik": ["Samsung", "Apple", "Sony", "LG", "Xiaomi", "ASUS", "Lenovo"],
    "Fashion": ["Zara", "H&M", "Uniqlo", "Erigo", "Nevada", "Lea"],
    "Makanan & Minuman": ["Indofood", "Mayora", "Unilever", "Nestlé", "Garuda Food"],
    "Kesehatan": ["Kimia Farma", "Kalbe", "Combiphar", "Konimex"],
    "Olahraga": ["Nike", "Adidas", "Specs", "League", "Puma"],
    "Rumah Tangga": ["Philips", "Panasonic", "Sharp", "Maspion", "Cosmos"],
    "Kecantikan": ["Wardah", "Emina", "Pixy", "Maybelline", "L'Oréal"],
    "Otomotif": ["Bosch", "NGK", "Federal", "Aspira", "Shell"],
}

nama_produk = {
    "Elektronik": [
        "Smartphone",
        "Laptop",
        "Tablet",
        "Headphone",
        "Smartwatch",
        "Speaker Bluetooth",
    ],
    "Fashion": [
        "Kaos Polos",
        "Kemeja Casual",
        "Celana Jeans",
        "Jaket Hoodie",
        "Dress Casual",
    ],
    "Makanan & Minuman": [
        "Mie Instan",
        "Kopi Sachet",
        "Snack Keripik",
        "Minuman Energi",
        "Teh Celup",
    ],
    "Kesehatan": [
        "Vitamin C",
        "Masker Medis",
        "Obat Flu",
        "Suplemen Imun",
        "Hand Sanitizer",
    ],
    "Olahraga": [
        "Sepatu Running",
        "Kaos Olahraga",
        "Celana Training",
        "Tas Gym",
        "Topi Sport",
    ],
    "Rumah Tangga": ["Blender", "Rice Cooker", "Setrika", "Kipas Angin", "Lampu LED"],
    "Kecantikan": ["Lipstik", "Foundation", "Serum Wajah", "Pelembab", "Sunscreen"],
    "Otomotif": ["Oli Mesin", "Busi", "Ban Dalam", "Helm Full Face", "Aki Motor"],
}

# 🎯 harga per kategori (REALISTIS)
price_range = {
    "Elektronik": (500000, 15000000),
    "Fashion": (50000, 500000),
    "Makanan & Minuman": (2000, 50000),
    "Kesehatan": (10000, 300000),
    "Olahraga": (100000, 2000000),
    "Rumah Tangga": (50000, 2000000),
    "Kecantikan": (20000, 500000),
    "Otomotif": (50000, 2000000),
}


def buat_produk():
    kategori = random.choice(list(kategori_produk.keys()))
    brand = random.choice(kategori_produk[kategori])
    nama = random.choice(nama_produk[kategori])

    # harga realistis
    min_price, max_price = price_range[kategori]
    price = random.randint(min_price, max_price)

    # bikin harga "psikologis"
    price = int(str(price)[:-2] + "99") if price > 100 else price

    stock = random.randint(0, 500)

    return {
        "product_id": str(uuid.uuid4())[:8],
        "product_name": f"{brand} {nama}",
        "category": kategori,
        "brand": brand,
        "price": price,
        "stock": stock,
        "is_available": stock > 0,
        "created_date": datetime.now(),
    }


def insert_products():
    pg = PostgresHook(postgres_conn_id="postgres_ecommerce")
    conn = pg.get_conn()
    cursor = conn.cursor()

    jumlah = random.randint(10, 50)
    data_products = [buat_produk() for _ in range(jumlah)]

    # 🚀 bulk insert (lebih proper)
    values = [
        (
            p["product_id"],
            p["product_name"],
            p["category"],
            p["brand"],
            p["price"],
            p["stock"],
            p["is_available"],
            p["created_date"],
        )
        for p in data_products
    ]

    cursor.executemany(
        """
        INSERT INTO products (
            product_id, product_name, category, brand, price, stock, is_available, created_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
        """,
        values,
    )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted {len(values)} products successfully")


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
