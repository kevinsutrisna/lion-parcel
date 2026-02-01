CREATE TABLE IF NOT EXISTS retail_transactions (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    last_status VARCHAR(50),
    pos_origin VARCHAR(10),
    pos_destination VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_updated_at ON retail_transactions(updated_at);