import os
import boto3
import threading
from uwaterloo import *
from random import randint
import os

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

db_client = boto3.client('dynamodb')
db_res = boto3.resource('dynamodb')

table = create_or_get_pre_req_table()

courses = (uw.get_courses())

print(len(courses))

args = []

api_key = gen_api_key()

prereqs = []

sem = threading.Semaphore()
sem2 = threading.Semaphore()

total = len(courses)

progress = 0

def run(courses):
    prereq_array = []
    global progress
    for course in courses:
        prereq_array.append(uw.get_prereqs({'api_key': next(api_key), 'course': course}))
        sem2.acquire()
        progress += 1

        # if progress % 1 == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Progress: {0:.2f}% - {1}/{2}'.format(float(progress)/total * 100.0, progress, total))
        sem2.release()

    sem.acquire()
    prereqs.extend(prereq_array)
    sem.release()

threads = [threading.Thread(target=run, args=(courses[i:i + 1000],)) for i in range(0, len(courses), 1000)]

count = 1
for thread in threads:
    print('Starting thread #{}'.format(count))
    count += 1
    thread.start()

for thread in threads:
    thread.join()

for prereq in prereqs:
    table.put_item(
        Item={
            'course_key': prereq['course'],
            'prereqs': prereq['prereqs']
        }
    )
