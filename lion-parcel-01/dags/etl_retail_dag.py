from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import logging

SOURCE_CONN_ID = 'SOURCE_DB'
DW_CONN_ID = 'DATA_WAREHOUSE'

default_args = {
    'owner': 'lion_parcel',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def get_watermark():
    dw_hook = PostgresHook(postgres_conn_id=DW_CONN_ID)
    sql = "SELECT MAX(updated_at) FROM retail_transactions;"
    conn = dw_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    if result:
        return result
    return datetime(1970, 1, 1)

def run_etl(**context):
    source_hook = PostgresHook(postgres_conn_id=SOURCE_CONN_ID)
    dw_hook = PostgresHook(postgres_conn_id=DW_CONN_ID)
    
    watermark = get_watermark()
    logging.info(f"Starting ETL with Watermark: {watermark}")
    

    extract_sql = """
        SELECT id, customer_id, last_status, pos_origin, pos_destination, created_at, updated_at, deleted_at
        FROM retail_transactions
        WHERE updated_at > %s
    """
    source_conn = source_hook.get_conn()
    source_cursor = source_conn.cursor()
    source_cursor.execute(extract_sql, (watermark,))
    rows = source_cursor.fetchall()
    
    if not rows:
        logging.info("No new data to sync.")
        return

    logging.info(f"Extracted {len(rows)} rows to sync.")


    upsert_sql = """
        INSERT INTO retail_transactions (id, customer_id, last_status, pos_origin, pos_destination, created_at, updated_at, deleted_at, etl_loaded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (id) DO UPDATE SET
            last_status = EXCLUDED.last_status,
            updated_at = EXCLUDED.updated_at,
            deleted_at = EXCLUDED.deleted_at,
            etl_loaded_at = NOW();
    """
    
    dw_conn = dw_hook.get_conn()
    dw_cursor = dw_conn.cursor()
    
    try:
        dw_cursor.executemany(upsert_sql, rows)
        dw_conn.commit()
        logging.info("Data synced successfully.")
    except Exception as e:
        dw_conn.rollback()
        logging.error(f"Error during loading: {e}")
        raise
    finally:
        source_cursor.close()
        source_conn.close()
        dw_cursor.close()
        dw_conn.close()

with DAG(
    '02_retail_etl_hourly',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 * * * *',
    catchup=False
) as dag:
    
    etl_task = PythonOperator(
        task_id='sync_transactions',
        python_callable=run_etl,
        provide_context=True
    )