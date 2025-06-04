import pandas as pd
from faker import Faker
import random
import string
from google.cloud import storage
import os
import csv

# Initialize Faker
fake = Faker()

# Generate random password (8-12 chars, mixed case + digits + symbols)
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    length = random.randint(8, 12)
    return ''.join(random.choice(chars) for _ in range(length))

# Clean text by removing commas and newlines
def clean_text(text):
    return text.replace("\n", " ").replace(",", "").strip()

# Generate employee data
def generate_employee_data(num_records=100):
    employees = []
    for _ in range(num_records):
        employee = {
            "employee_id": fake.unique.random_number(digits=6),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": clean_text(fake.address()),  # cleaned address
            "job_title": clean_text(fake.job()),     # cleaned job title
            "department": fake.random_element(elements=("HR", "Engineering", "Finance", "Marketing", "Sales")),
            "salary": round(random.uniform(40000, 120000), 2),
            "ssn": fake.ssn(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d'),
            "password": generate_password()
        }
        employees.append(employee)
    return pd.DataFrame(employees)

# Save to CSV (you can still quote all to be safe)
def save_to_csv(df, filename="employee_data.csv"):
    df.to_csv(filename, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"✅ Data saved to {filename}")
    return filename

# Upload to GCS
def upload_to_gcs(bucket_name, source_filename, destination_filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_filename)
    blob.upload_from_filename(source_filename)
    print(f"✅ Uploaded {source_filename} to GCS bucket: gs://{bucket_name}/{destination_filename}")

# Main Execution
if __name__ == "__main__":
    # Generate data
    df = generate_employee_data(100)

    # Save to CSV
    csv_file = save_to_csv(df)

    # Upload to GCS
    gcs_bucket = "dl-agent"  # change this to your GCS bucket name
    gcs_destination = "employee_data.csv"

    upload_to_gcs(gcs_bucket, csv_file, gcs_destination)
