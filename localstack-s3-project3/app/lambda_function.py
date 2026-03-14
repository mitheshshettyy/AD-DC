import json
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localstack:4566"
)

SOURCE_BUCKET = "source-bucket"
DEST_BUCKET = "destination-bucket"


def lambda_handler(event, context):
    print("Event received:", event)

    response = s3.list_objects_v2(Bucket=SOURCE_BUCKET)

    if "Contents" not in response:
        print("No files found")
        return {
            "statusCode": 200,
            "body": json.dumps("No files found")
        }

    for obj in response["Contents"]:
        key = obj["Key"]
        print(f"Processing {key}")

        copy_source = {
            "Bucket": SOURCE_BUCKET,
            "Key": key
        }

        s3.copy_object(
            CopySource=copy_source,
            Bucket=DEST_BUCKET,
            Key=key
        )

        s3.delete_object(
            Bucket=SOURCE_BUCKET,
            Key=key
        )

        print(f"Moved {key} to destination bucket")

    return {
        "statusCode": 200,
        "body": json.dumps("Completed")
    }