\connect lion_parcel

CREATE TABLE IF NOT EXISTS retail_transactions (
    id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    last_status VARCHAR(100) NOT NULL,
    pos_origin VARCHAR(100),
    pos_destination VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    deleted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_retail_transactions_updated_at ON retail_transactions(updated_at);
CREATE INDEX IF NOT EXISTS idx_retail_transactions_deleted_at ON retail_transactions(deleted_at);
