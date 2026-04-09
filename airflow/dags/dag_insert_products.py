from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime
from pendulum import timezone
import random
import uuid


kategori_produk = {
    "Skincare": [
        ("Hydrating Essence", "Somethinc"),
        ("Brightening Serum", "Skintific"),
        ("Retinol Night Cream", "The Ordinary"),
        ("Moisturizing Gel", "Wardah"),
        ("Sunscreen SPF50", "Emina"),
    ],
    "Lipstik": [
        ("Matte Lip Cream", "Wardah"),
        ("Velvet Lip Tint", "Emina"),
        ("Soft Matte Lip Cream", "NYX"),
        ("Luxury Lipstick", "MAC"),
    ],
    "Makeup": [
        ("Cushion Foundation", "Maybelline"),
        ("BB Cream", "Wardah"),
        ("Liquid Concealer", "NYX"),
        ("Loose Powder", "Make Over"),
    ],
    "Haircare": [
        ("Hair Repair Serum", "Loreal"),
        ("Scalp Shampoo", "Wardah"),
        ("Hair Vitamin", "Ellips"),
    ],
    "Parfum": [
        ("Body Mist Floral", "Scarlett"),
        ("Luxury Eau De Parfum", "Chanel"),
        ("Fresh Daily Mist", "Emina"),
    ],
}


price_range = {
    "Skincare": (50000, 5000000),
    "Lipstik": (35000, 650000),
    "Makeup": (50000, 850000),
    "Haircare": (35000, 500000),
    "Parfum": (55000, 2500000),
}


def buat_produk_baru():
    kategori = random.choice(list(kategori_produk.keys()))
    nama, brand = random.choice(kategori_produk[kategori])

    min_price, max_price = price_range[kategori]

    return {
        "product_id": str(uuid.uuid4())[:8],
        "product_name": f"{brand} {nama}",
        "category": kategori,
        "brand": brand,
        "price": round(random.randint(min_price, max_price), -3),
        "stock": random.randint(50, 300),
        "is_available": True,
        "created_date": datetime.now(),
    }


def maintain_products():
    pg = PostgresHook(postgres_conn_id="postgres_ecommerce")
    conn = pg.get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT product_id, product_name
        FROM products
        WHERE stock = 0
        """
    )

    out_of_stock = cursor.fetchall()

    for product in out_of_stock:
        print(f"WARNING: Stock habis untuk {product[1]} ({product[0]})")

    cursor.execute(
        """
        UPDATE products
        SET stock = stock + CEIL(stock * 0.5),
            is_available = TRUE
        """
    )

    print("All products restocked by 50%")

    data_products = [buat_produk_baru() for _ in range(3)]

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
            product_id,
            product_name,
            category,
            brand,
            price,
            stock,
            is_available,
            created_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
        """,
        values,
    )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted {len(values)} new beauty products successfully")


with DAG(
    dag_id="dag_insert_products",
    start_date=datetime(2026, 4, 1, tzinfo=timezone("Asia/Jakarta")),
    schedule_interval="@hourly",
    catchup=False,
    tags=["batch", "products"],
) as dag:

    task_maintain_products = PythonOperator(
        task_id="maintain_products",
        python_callable=maintain_products,
    )
