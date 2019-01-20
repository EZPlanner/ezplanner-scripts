import os
import boto3
from uwaterloo import *

uw = UWaterloo(os.environ['UW_API_KEY'])

db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# table = db.create_table(
#     TableName='pre_req',
#     KeySchema=[
#         {
#             'AttributeName': 'course_key'
#             'KeyType': 'HASH'
#         }
#     ],
#     AttributeDefinitions=[
#         {

#         }
#     ]
# )

courses = uw.get_courses()

prereqs = {}

for course in courses:
    prereqs['{}/{}'.format(course['subject'], course['catalog_number'])] = uw.get_prereqs(course) or []

print(prereqs)