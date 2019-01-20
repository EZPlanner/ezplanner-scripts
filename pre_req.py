import os
import boto3
from uwaterloo import *
from random import randint
from multiprocessing.dummy import Pool as ThreadPool

uw = UWaterloo(os.environ['UW_API_KEY'])

db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

try:
    table = db.create_table(
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
except:
    # do something here as you require
    pass

pool = ThreadPool(50)

courses = uw.get_courses()

args = []

def gen_api_key():
    a = 0
    while True:
        if a == 22:
            a = 0
        yield os.environ['UW_API_KEY{}'.format(a)]
        a += 1

api_key = gen_api_key()

for course in courses[0:100]:
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