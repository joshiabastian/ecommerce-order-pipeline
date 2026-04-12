from confluent_kafka import Producer
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import random
import json
import time
import os

load_dotenv()

# koneksi kafka
kafka_config = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
}
TOPIC = os.getenv("KAFKA_TOPIC", "orders")


# koneksi postgres
def ambil_koneksi_db():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        dbname=os.getenv("POSTGRES_DB", "ecommerce_db"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


# ambil user & produk yang tersedia dari db
def ambil_data_aktif():
    conn = ambil_koneksi_db()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE is_active = TRUE")
    users = [r[0] for r in cursor.fetchall()]

    cursor.execute(
        "SELECT product_id, price FROM products WHERE is_available = TRUE AND stock > 0"
    )
    products = cursor.fetchall()

    cursor.close()
    conn.close()
    return users, products


# hitung diskon berdasarkan quantity
def hitung_diskon(quantity):
    if quantity > 100:
        return 0.30
    elif quantity > 50:
        return 0.20
    elif quantity > 10:
        return 0.10
    return 0.0


# pilih payment method berdasarkan quantity
def pilih_payment(quantity):
    if quantity > 15:
        return random.choice(
            ["Transfer Bank", "Kartu Kredit", "GoPay", "OVO", "Dana", "ShopeePay"]
        )
    return random.choice(
        ["Transfer Bank", "Kartu Kredit", "COD", "GoPay", "OVO", "Dana", "ShopeePay"]
    )


# generate order
def buat_order(users, products):
    if not users or not products:
        print("⚠️ Tidak ada user atau produk tersedia.")
        return None

    user_id = random.choice(users)

    jumlah_produk = random.randint(1, 3)
    produk_dipilih = random.sample(products, min(jumlah_produk, len(products)))

    jam_sekarang = datetime.now().hour
    jam_rawan = 0 <= jam_sekarang < 4

    # negara - 85% Indonesia, 15% luar (fraud bait)
    country = random.choices(
        ["ID", "US", "SG", "MY", "AU", "GB"], weights=[85, 5, 4, 3, 2, 1]
    )[0]

    orders = []
    for product_id, price in produk_dipilih:
        if jam_rawan:
            quantity = random.choices(
                [random.randint(1, 15), random.randint(50, 200)], weights=[80, 20]
            )[0]
        else:
            quantity = random.randint(1, 15)

        diskon = hitung_diskon(quantity)
        amount = round(price * quantity * (1 - diskon), 2)

        orders.append(
            {
                "order_id": f"ORD-{int(time.time() * 1000)}-{random.randint(100, 999)}",
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity,
                "amount": amount,
                "country": country,
                "city": random.choice(
                    [
                        "Jakarta",
                        "Bandung",
                        "Surabaya",
                        "Medan",
                        "Makassar",
                        "Semarang",
                        "Palembang",
                        "Tangerang",
                        "Depok",
                        "Bogor",
                    ]
                ),
                "payment_method": pilih_payment(quantity),
                "device": random.choice(["mobile", "desktop", "tablet"]),
                "created_date": datetime.now().isoformat(),
            }
        )

    return orders


def on_delivery(err, msg):
    if err:
        print(f"❌ Gagal kirim pesan: {err}")
    else:
        print(
            f"✅ Order terkirim ke topic [{msg.topic()}] partition [{msg.partition()}]"
        )


def jalankan_producer():
    producer = Producer(kafka_config)
    print(f"🚀 Producer berjalan, mengirim ke topic '{TOPIC}'...")

    while True:
        try:
            users, products = ambil_data_aktif()
            orders = buat_order(users, products)

            if orders:
                for order in orders:
                    producer.produce(
                        topic=TOPIC,
                        key=order["order_id"],
                        value=json.dumps(order),
                        callback=on_delivery,
                    )
                producer.flush()

        except Exception as e:
            print(f"❌ Error: {e}")

        jeda = random.randint(1, 5)
        time.sleep(jeda)


if __name__ == "__main__":
    jalankan_producer()
