from dynamodb import *

db = DynamoDB(endpoint_url='http://localhost:8000') # Get local dynamodb instance

prereq_table = db.get_pre_req_table()

prereqs = db.get_all_entries(prereq_table)

print(prereqs)