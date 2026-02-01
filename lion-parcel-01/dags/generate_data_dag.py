from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import random
import logging

default_args = {
    'owner': 'lion_parcel',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def generate_dummy_data():
    pg_hook = PostgresHook(postgres_conn_id='SOURCE_DB')
    
    rows = []
    statuses = ['PENDING', 'SHIPPED', 'IN_TRANSIT', 'DELIVERED', 'DONE']
    locations = ['CGK', 'SUB', 'DPS', 'KNO', 'UPG']
    
    for _ in range(10):
        rows.append((
            random.randint(1000, 9999),
            random.choice(statuses),
            random.choice(locations),
            random.choice(locations),
            datetime.now(),
            datetime.now()
        ))
    
    insert_query = """
    INSERT INTO retail_transactions (customer_id, last_status, pos_origin, pos_destination, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.executemany(insert_query, rows)
    conn.commit()
    logging.info("Inserted 10 dummy records.")

    soft_delete_query = """
    UPDATE retail_transactions 
    SET deleted_at = NOW(), updated_at = NOW(), last_status = 'DONE'
    WHERE id = (SELECT id FROM retail_transactions WHERE deleted_at IS NULL ORDER BY RANDOM() LIMIT 1)
    AND random() > 0.7;
    """
    cursor.execute(soft_delete_query)
    conn.commit()
    logging.info("Randomly processed soft deletes.")

with DAG(
    '01_data_generator',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='*/5 * * * *',
    catchup=False
) as dag:
    
    generate_task = PythonOperator(
        task_id='generate_transactions',
        python_callable=generate_dummy_data
    )