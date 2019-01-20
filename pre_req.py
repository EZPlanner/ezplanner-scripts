import os
import boto3
from uwaterloo import *
from random import randint
from multiprocessing.dummy import Pool as ThreadPool

THREAD_COUNT = 20
DYNAMODB_ENDPOINT = 'http://localhost:8000'

def create_or_get_pre_req_table():
    try:
        return db_client.create_table(
            TableName='pre_req',
            KeySchema=[
                {
                    'AttributeName': 'course_key',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'course_key',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except db_client.exceptions.ResourceInUseException:
        return db_res.Table('pre_req')

def gen_api_key():
    a = 0
    while True:
        if a == 22:
            a = 0
        yield os.environ['UW_API_KEY{}'.format(a)]
        a += 1

uw = UWaterloo(os.environ['UW_API_KEY0'])

db_client = boto3.client('dynamodb', endpoint_url=DYNAMODB_ENDPOINT)
db_res = boto3.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT)

table = create_or_get_pre_req_table()

pool = ThreadPool(THREAD_COUNT)

courses = uw.get_courses()

args = []

api_key = gen_api_key()

for course in courses:
    args.append({
        'api_key': next(api_key),
        'course': course
    })

prereq_data = pool.map(uw.get_prereqs, args)

for prereqs in prereq_data:
    table.put_item(
        Item={
            'course_key': prereqs['course'],
            'prereqs': prereqs['prereqs']
        }
    )
