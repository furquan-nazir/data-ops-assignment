import boto3
import os
import json
from moto import mock_s3, mock_dynamodb2


@mock_s3
@mock_dynamodb2
def mock_aws():
    ### S3
    # Create mock client
    s3 = boto3.client('s3', region_name='eu-central-1')

    # Create mock Bucket
    bucketname = 'vitesco'
    response = s3.create_bucket(
        Bucket=bucketname,
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-central-1',
        },
    )

    # Upload data to mock s3
    path = "data/plant"
    for root, dirs, files in os.walk(path):
        for file in files:
            s3.upload_file(os.path.join(root, file), bucketname,
                           f"{path}/{file}")

    response = s3.list_buckets()
    print([bucket["Name"] for bucket in response["Buckets"]])

    response = s3.list_objects_v2(Bucket=bucketname)
    print([object["Key"] for object in response["Contents"]])

    ### DynamoDB
    dynamodb = boto3.client('dynamodb')

    table = "users"

    dynamodb.create_table(
        TableName=table,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'age',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[{
            'AttributeName': 'id',
            'AttributeType': 'N'
        }, {
            'AttributeName': 'age',
            'AttributeType': 'N'
        }])

    with open('data/user/users.json') as json_file:
        data = json.load(json_file)
        for user in data:
            dynamodb.put_item(
                Item={
                    'id': {
                        'N': str(user['id']),
                    },
                    'first_name': {
                        'S': str(user['first_name']),
                    },
                    'email': {
                        'S': str(user['email']),
                    },
                    'city': {
                        'S': str(user['city']),
                    },
                    'age': {
                        'N': str(user['age']),
                    },
                    'gender': {
                        'S': str(user['gender']),
                    },
                    'part_color': {
                        'S': str(user['part_color']),
                    },
                },
                ReturnConsumedCapacity='TOTAL',
                TableName=table,
            )

    response = response = dynamodb.scan(TableName=table)
    print(response)


mock_aws()
