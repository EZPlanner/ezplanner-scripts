import progressbar
from dynamodb import *

DYNAMODB_LOCAL_ENDPOINT = 'http://localhost:8000'
DYNAMODB_REMOTE_ENDPOINT = None
DB_ENDPOINT = DYNAMODB_REMOTE_ENDPOINT

db = DynamoDB(endpoint_url=DB_ENDPOINT) # Get local dynamodb instance

prereq_table = db.get_pre_req_table()

prereqs = db.get_all_entries(prereq_table)

postreq_table = db.get_post_req_table()

postreq_dict = {}

def process_item(course_name, items):
    for i in items:
        if isinstance(i, int):
            continue
        elif isinstance(i, list):
            process_item(course_name, i)
        else:
            if i not in postreq_dict:
                postreq_dict[i] = []

            postreq_dict[i].append(course_name)

for prereq in prereqs:
    process_item(''.join(prereq['course_key'].split('/')), prereq['prereqs'])

with progressbar.ProgressBar(max_value=len(postreq_dict)) as bar:
    counter = 0
    for key in postreq_dict:
        postreq_table.put_item(
            Item={
                'course_key': str(key),
                'postreqs': postreq_dict[key]
            }
        )
        counter += 1
        bar.update(counter)