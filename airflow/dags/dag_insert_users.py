from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from faker import Faker
from datetime import datetime
from pendulum import timezone
import random
import uuid

fake = Faker("id_ID")

domain_email = ["gmail.com", "yahoo.com", "outlook.com"]


# inisiasi untuk buat user baru
def buat_user():
    nama = fake.name()
    username = nama.lower().replace(" ", ".") + str(random.randint(1, 999))
    email = f"{username}@{random.choice(domain_email)}"

    return {
        "user_id": str(uuid.uuid4())[:8],
        "name": nama,
        "email": email,
        "phone_number": fake.phone_number(),
        "address": fake.street_address(),
        "city": fake.city(),
        "is_active": random.choices([True, False], weights=[90, 10])[0],
        "created_date": datetime.now(),
    }


# masukan data yang dibuat kedalam database
def insert_users():
    pg = PostgresHook(postgres_conn_id="postgres_ecommerce")
    conn = pg.get_conn()
    cursor = conn.cursor()

    jumlah = random.randint(10, 50)
    data_users = [buat_user() for _ in range(jumlah)]

    for user in data_users:
        cursor.execute(
            """
            INSERT INTO users (user_id, name, email, phone_number, address, city, is_active, created_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
        """,
            (
                user["user_id"],
                user["name"],
                user["email"],
                user["phone_number"],
                user["address"],
                user["city"],
                user["is_active"],
                user["created_date"],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{jumlah} users berhasil dimasukkan")


with DAG(
    dag_id="dag_insert_users",
    start_date=datetime(2026, 4, 1, tzinfo=timezone("Asia/Jakarta")),
    schedule_interval="@hourly",
    catchup=False,
    tags=["batch", "users"],
) as dag:

    task_insert_users = PythonOperator(
        task_id="insert_users", python_callable=insert_users
    )
