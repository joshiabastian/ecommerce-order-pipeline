from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
from pendulum import timezone
from google.cloud import bigquery
from decimal import Decimal
import requests
import os

GCP_PROJECT = os.getenv("GCP_PROJECT_ID", "jcdeah-008")
BQ_DATASET = os.getenv("GCP_DATASET", "yosia_finpro")
TG_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TABLES = ["users", "products", "orders"]


def kirim_notif_telegram(pesan):
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


def ambil_data_postgres(table, tanggal_kemarin):
    pg = PostgresHook(postgres_conn_id="postgres_ecommerce")
    conn = pg.get_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM {table} WHERE DATE(created_date) = %s", (tanggal_kemarin,)
    )
    rows = cursor.fetchall()
    kolom = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return [dict(zip(kolom, row)) for row in rows]


def load_ke_bigquery(table, data):
    if not data:
        print(f"Tidak ada data baru untuk tabel {table}.")
        return

    client = bigquery.Client(project=GCP_PROJECT)
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.{table}"

    for row in data:
        for key, val in row.items():
            if isinstance(val, datetime):
                row[key] = val.isoformat()
            elif isinstance(val, Decimal):
                row[key] = int(val)

    # load incremental
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    job = client.load_table_from_json(data, table_id, job_config=job_config)
    job.result()
    print(f"Berhasil load {len(data)} baris ke {table_id}.")


def ingest_table(table, **context):
    tanggal_kemarin = (context["execution_date"] - timedelta(days=1)).date()
    print(f"Mengambil data {table} untuk tanggal {tanggal_kemarin}...")
    data = ambil_data_postgres(table, tanggal_kemarin)
    load_ke_bigquery(table, data)


default_args = {
    "on_failure_callback": on_failure,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_postgres_to_bigquery",
    start_date=datetime(2026, 4, 1, tzinfo=timezone("Asia/Jakarta")),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["batch", "bigquery"],
) as dag:

    for tabel in TABLES:
        PythonOperator(
            task_id=f"ingest_{tabel}",
            python_callable=ingest_table,
            op_kwargs={"table": tabel},
        )
