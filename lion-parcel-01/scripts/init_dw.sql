CREATE TABLE IF NOT EXISTS retail_transactions (
    id INT PRIMARY KEY,
    customer_id INT,
    last_status VARCHAR(50),
    pos_origin VARCHAR(10),
    pos_destination VARCHAR(10),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    etl_loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);