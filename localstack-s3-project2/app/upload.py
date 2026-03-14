import boto3
from botocore.exceptions import ClientError
import os

def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT", "http://localhost:4566"),
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"✅ Uploaded {file_name} to {bucket}/{object_name}")
    except ClientError as e:
        print(f"❌ Upload failed: {e}")


if __name__ == "__main__":
    bucket_name = "bucket1"

    s3 = boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT", "http://localhost:4566"),
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

    # Create bucket if not exists
    try:
        s3.create_bucket(Bucket=bucket_name)
        print("Bucket created.")
    except Exception:
        print("Bucket already exists.")

    upload_to_s3("test_file.txt", bucket_name)