import boto3
import os
import json
from moto import mock_s3, mock_dynamodb2


@mock_s3
@mock_dynamodb2
def mock_aws():
    # S3
    # Create mock client
    s3 = boto3.client('s3', region_name='us-east-1')

    # Create mock Bucket
    bucketname = 'vitesco-data-ops-assignment-2021'
    response = s3.create_bucket(Bucket=bucketname)

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

    # DynamoDB
    # Create mock client
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')

    # Create DynamoDB table
    table = "vitesco-users"
    dynamodb.create_table(
        TableName=table,
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10,
        },
        KeySchema=[{
            'AttributeName': 'id',
            'KeyType': 'HASH'  # Partition key
        }],
        AttributeDefinitions=[{
            'AttributeName': 'id',
            'AttributeType': 'N'
        }])

    # Insert DynamoDB records
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
                        'S': str(user['age']),
                    },
                    'gender': {
                        'S': str(user['gender']),
                    },
                    'part_color': {
                        'S': str(user['part_color']),
                    },
                },
                TableName=table,
            )

    response = dynamodb.scan(TableName=table)
    print(response)


mock_aws()
