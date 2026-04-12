from confluent_kafka import Consumer, KafkaError
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
import json
import os

load_dotenv()

# koneksi kafka
kafka_config = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    "group.id": "ecommerce-consumer-group",
    "auto.offset.reset": "earliest",
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


# cek fraud berdasarkan rules
def cek_fraud(order):
    jam = datetime.fromisoformat(order["created_date"]).hour
    jam_rawan = 0 <= jam < 4

    # rule 1: transaksi bukan dari indonesia
    if order["country"] != "ID":
        return "frauds"

    # rule 2: quantity > 100 di jam rawan
    if order["quantity"] > 100 and jam_rawan:
        return "frauds"

    # rule 3: amount > 100 juta di jam rawan
    if order["amount"] > 100_000_000 and jam_rawan:
        return "frauds"

    return "genuine"


# kurangi stok produk
def kurangi_stok(cursor, product_id, quantity):
    cursor.execute(
        "SELECT stock FROM products WHERE product_id = %s FOR UPDATE", (product_id,)
    )
    hasil = cursor.fetchone()

    if not hasil:
        print(f"⚠️ Produk {product_id} tidak ditemukan.")
        return False

    stok_sekarang = hasil[0]

    if stok_sekarang <= 0:
        print(f"⚠️ Stok produk {product_id} habis! Order di-skip.")
        return False

    if stok_sekarang < quantity:
        print(
            f"⚠️ Stok {product_id} tidak cukup. Stok: {stok_sekarang}, diminta: {quantity}. Order di-skip."
        )
        return False

    stok_baru = stok_sekarang - quantity
    cursor.execute(
        """
        UPDATE products
        SET stock = %s,
            is_available = %s
        WHERE product_id = %s
        """,
        (stok_baru, stok_baru > 0, product_id),
    )
    return True


# insert order ke postgres
def insert_order(conn, order):
    cursor = conn.cursor()

    try:
        stok_ok = kurangi_stok(cursor, order["product_id"], order["quantity"])
        if not stok_ok:
            conn.rollback()
            return

        status = cek_fraud(order)

        cursor.execute(
            """
            INSERT INTO orders (
                order_id, user_id, product_id, quantity, amount,
                country, city, payment_method, device, created_date, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING
            """,
            (
                order["order_id"],
                order["user_id"],
                order["product_id"],
                order["quantity"],
                order["amount"],
                order["country"],
                order["city"],
                order["payment_method"],
                order["device"],
                order["created_date"],
                status,
            ),
        )

        conn.commit()
        print(f"✅ Order {order['order_id']} berhasil disimpan | status: {status}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error insert order: {e}")
    finally:
        cursor.close()


# reconnect kalau koneksi putus
def pastikan_koneksi(conn):
    try:
        conn.cursor().execute("SELECT 1")
        return conn
    except Exception:
        print("🔄 Koneksi PostgreSQL terputus, mencoba reconnect...")
        return ambil_koneksi_db()


def jalankan_consumer():
    consumer = Consumer(kafka_config)
    consumer.subscribe([TOPIC])
    print(f"🚀 Consumer berjalan, mendengarkan topic '{TOPIC}'...")

    # buka koneksi sekali di awal
    conn = ambil_koneksi_db()

    try:
        while True:
            pesan = consumer.poll(timeout=1.0)

            if pesan is None:
                continue

            if pesan.error():
                if pesan.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f"❌ Kafka error: {pesan.error()}")
                continue

            try:
                order = json.loads(pesan.value().decode("utf-8"))
                print(f"📦 Order diterima: {order['order_id']}")

                # pastiin koneksi masih hidup sebelum insert
                conn = pastikan_koneksi(conn)
                insert_order(conn, order)

            except Exception as e:
                print(f"❌ Error proses pesan: {e}")

    except KeyboardInterrupt:
        print("🛑 Consumer dihentikan.")
    finally:
        conn.close()
        consumer.close()


if __name__ == "__main__":
    jalankan_consumer()
