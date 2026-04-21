from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from faker import Faker
from datetime import datetime, timedelta
from pendulum import timezone
import pendulum
import random
import uuid
import requests
import os

fake = Faker("id_ID")
domain_email = ["gmail.com", "yahoo.com", "outlook.com"]


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
    exec_dt = context["execution_date"]
    pesan = (
        f"❌ DAG Gagal!\n"
        f"DAG     : {dag_id}\n"
        f"Task    : {task_id}\n"
        f"Tanggal : {exec_dt}\n"
    )
    kirim_notif_telegram(pesan)


def buat_user():
    nama = fake.name()
    username = nama.lower().replace(" ", "")[:10] + str(random.randint(1, 999))
    email = f"{username}@{random.choice(domain_email)}"
    gender = random.choices(["Perempuan", "Laki-laki"], weights=[70, 30])[0]

    return {
        "user_id": str(uuid.uuid4()).replace("-", "")[:16],
        "name": nama,
        "email": email,
        "phone_number": fake.phone_number(),
        "address": fake.street_address(),
        "city": fake.city(),
        "age": random.randint(15, 45),
        "gender": gender,
        "is_active": random.choices([True, False], weights=[90, 10])[0],
        "created_date": pendulum.now("Asia/Jakarta"),
    }


def insert_users():
    pg = PostgresHook(postgres_conn_id="postgres_salah")
    conn = pg.get_conn()
    cursor = conn.cursor()

    jumlah = random.randint(10, 50)
    data_users = [buat_user() for _ in range(jumlah)]

    values = [
        (
            u["user_id"],
            u["name"],
            u["email"],
            u["phone_number"],
            u["address"],
            u["city"],
            u["age"],
            u["gender"],
            u["is_active"],
            u["created_date"],
        )
        for u in data_users
    ]

    sql = """
        INSERT INTO users (
            user_id, name, email, phone_number, address,
            city, age, gender, is_active, created_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (email) DO NOTHING
    """

    try:
        cursor.executemany(sql, values)
        conn.commit()
        print(f"Berhasil insert {len(values)} users.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


default_args = {
    "on_failure_callback": on_failure,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="dag_insert_users",
    start_date=datetime(2026, 4, 1, tzinfo=timezone("Asia/Jakarta")),
    schedule_interval="@hourly",
    catchup=False,
    tags=["batch", "users"],
) as dag:

    task_insert_users = PythonOperator(
        task_id="insert_users",
        python_callable=insert_users,
        on_failure_callback=on_failure,
    )
