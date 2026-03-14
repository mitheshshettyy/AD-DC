@echo off
setlocal

echo [1/6] Creating Buckets...
aws s3 mb s3://source-bucket --endpoint-url=http://localhost.localstack.cloud:4566
aws s3 mb s3://destination-bucket --endpoint-url=http://localhost.localstack.cloud:4566

echo [2/6] Packaging Lambda...
powershell -Command "Compress-Archive -Path lambda_function.py -DestinationPath function.zip -Force"

echo [3/6] Creating Lambda Function...
aws lambda create-function ^
    --function-name S3SyncFunction ^
    --runtime python3.9 ^
    --handler lambda_function.lambda_handler ^
    --zip-file fileb://function.zip ^
    --role arn:aws:iam::000000000000:role/lambda-role ^
    --endpoint-url=http://localhost.localstack.cloud:4566

echo [4/6] Creating EventBridge Rule...
aws events put-rule ^
    --name every-minute ^
    --schedule-expression "rate(1 minute)" ^
    --endpoint-url=http://localhost.localstack.cloud:4566

echo [5/6] Adding Lambda as Target...
aws events put-targets ^
    --rule every-minute ^
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:000000000000:function:S3SyncFunction" ^
    --endpoint-url=http://localhost.localstack.cloud:4566

echo [6/6] Granting Permission...
aws lambda add-permission ^
    --function-name S3SyncFunction ^
    --statement-id AllowScheduledEvents ^
    --action lambda:InvokeFunction ^
    --principal events.amazonaws.com ^
    --source-arn arn:aws:events:us-east-1:000000000000:rule/every-minute ^
    --endpoint-url=http://localhost.localstack.cloud:4566

echo Done!
pause