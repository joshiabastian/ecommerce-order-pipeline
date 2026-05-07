from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
from pendulum import timezone
import pendulum
import random
import uuid
import requests
import os

from product_config import (
    BRAND_PRODUCT_MAP,
    SIZE_OPTIONS,
    SIZE_MULTIPLIER,
    WARNA_OPTIONS,
    PREFIX,
)


def kirim_notif_telegram(pesan):
    TG_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        print("Telegram belum dikonfigurasi, skip notifikasi.")
        return
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TG_CHAT_ID, "text": pesan})


def on_failure(context):
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    exec_dt = context["execution_date"].in_timezone("Asia/Jakarta")
    pesan = (
        f"❌ DAG Gagal!\n"
        f"DAG     : {dag_id}\n"
        f"Task    : {task_id}\n"
        f"Tanggal : {exec_dt}\n"
    )
    kirim_notif_telegram(pesan)


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

    if category in ["Skincare", "Parfum", "Haircare"]:
        size = random.choice(SIZE_OPTIONS)
        product_name = f"{base_name} {size}"
        price = hitung_harga(base_price, size)
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
        pendulum.now("Asia/Jakarta"),
    )


def insert_products():
    pg = PostgresHook(postgres_conn_id="postgres_ecommerce")
    conn = pg.get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE products
            SET stock = 100, is_available = TRUE
            WHERE stock = 0
        """)

        cursor.execute("""
            UPDATE products
            SET stock = stock + CEIL(stock * 0.5)::INT,
                is_available = TRUE
            WHERE stock > 0 AND stock <= 50
        """)

        cursor.execute("SELECT product_id, product_name, brand FROM products")
        rows = cursor.fetchall()

        existing_ids = {r[0] for r in rows}
        existing_combos = {(r[1], r[2]) for r in rows}

        new_products = []
        for _ in range(random.randint(3, 5)):
            p = generate_product(existing_ids, existing_combos)
            if p:
                new_products.append(p)
                existing_ids.add(p[0])
                existing_combos.add((p[1], p[3]))

        if new_products:
            sql = """
                INSERT INTO products (
                    product_id, product_name, category, brand,
                    price, stock, is_available, created_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (product_name, brand) DO NOTHING
            """
            cursor.executemany(sql, new_products)
            print(f"Berhasil insert {len(new_products)} produk baru.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


default_args = {
    "on_failure_callback": on_failure,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


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
        on_failure_callback=on_failure,
    )
