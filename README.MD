# Lion Parcel

> Make sure your docker active.

## How to run this project

```bash
git clone https://github.com/kevinsutrisna/lion-parcel.git
cd lion-parcel
```

---

## Task 01

To get everything running (Airflow + Databases):

```bash
cd lion-parcel-01
docker-compose build
docker-compose up -d
```

### Airflow

- URL: http://localhost:8003
- Username: airflow
- Password: airflow
- Run the DAG to populate DB

### View DB

```bash
docker exec -it lion-parcel-01-source_db-1 psql -U user -d lion_parcel_source -c "SELECT * FROM retail_transactions;"
```

### Soft Delete

```bash
docker exec -it lion-parcel-01-source_db-1 psql -U user -d lion_parcel_source -c "UPDATE retail_transactions SET deleted_at = NOW(), updated_at = NOW() WHERE id = 1;"
```

### How it works

I set this up using Airflow to sync data every hour. It only grabs what is new or changed by looking at the updated_at timestamp.

To handle soft delete i implement if a record is "deleted" (soft delete) the source database just updates the deleted_at column. My ETL sees that update, pulls the row and uses an Upsert logic in the Data Warehouse. This keeps both sides perfectly in sync so you never lose historical data for audits but the warehouse always knows which rows are officially "done".

---

## Task 2

To get everything running:

```bash
cd lion-parcel-02
docker-compose build
docker-compose up -d
```

### Analyze single image

```bash
curl -X POST http://localhost:8000/analyze-image -H "Content-Type: application/json" -d "{\"image_url\": \"http://localhost:8000/images/Gambar1.jpg\"}"
```

### Analyze all images

```bash
curl -X POST http://localhost:8000/process-dataset
```
