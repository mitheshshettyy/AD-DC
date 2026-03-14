import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_localstack(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Pointing to LocalStack endpoint
    s3_client = boto3.client(
        's3',
        endpoint_url='http://localhost:4566',  # Default LocalStack port
        aws_access_key_id='test',              # LocalStack accepts 'test' keys
        aws_secret_access_key='test',
        region_name='us-east-1'
    )

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage

upload_to_localstack('sample.txt', 'bucket1')