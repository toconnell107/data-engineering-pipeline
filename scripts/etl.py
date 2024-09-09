import psycopg2
import csv
from datetime import datetime
from minio import Minio


def extract_data():
    conn = psycopg2.connect(database="data_engineering", user="postgres", password="password", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data;")
    data = cursor.fetchall()
    conn.close()
    return data

def transform_data(data):
    transformed = []
    for row in data:
        transformed.append({
            "id": row[0],
            "sensor_id": row[1],
            "temperature_celsius": row[2],
            "humidity_percentage": row[3],
            "recorded_at": row[4].strftime("%Y-%m-%d %H:%M:%S")
        })
    return transformed


def load_data(transformed):
    filename = f"sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "sensor_id", "temperature_celsius", "humidity_percentage", "recorded_at"])
        writer.writeheader()
        for row in transformed:
            writer.writerow(row)

    minio_client = Minio(
        "localhost:9000",
        access_key="admin",
        secret_key="password",
        secure=False
    )

    minio_client.fput_object(
        "data-lake-ci-cd-test", filename, filename
    )

    return filename


if __name__ == "__main__":
    data = extract_data()
    transformed = transform_data(data)
    load_data(transformed)