import os
import threading
from uwaterloo import *
from dynamodb import *
from random import randint
import os
import progressbar

THREAD_COUNT = 20
DYNAMODB_ENDPOINT = 'http://localhost:8000' # Use this if you want to point to local db
BATCH_COUNT = 200

def run(courses, bar):
    global progress
    prereq_array = []
    for course in courses:
        prereq_array.append(uw.get_prereqs({'course': course}))

        sem2.acquire()
        progress += 1
        bar.update(progress)
        sem2.release()

    sem.acquire()
    prereqs.extend(prereq_array)
    sem.release()

uw = UWaterloo(os.environ['UW_API_KEY0'])
db = DynamoDB()
table = db.get_pre_req_table()
courses = uw.get_courses()

prereqs = []

sem = threading.Semaphore()
sem2 = threading.Semaphore()

total = len(courses)
progress = 0

with progressbar.ProgressBar(max_value=len(courses)) as p_bar1:
    threads = [threading.Thread(target=run, args=(courses[i:i + BATCH_COUNT], p_bar1)) for i in range(0, len(courses), BATCH_COUNT)]

count = 0
for thread in threads:
    count += 1
    print('Starting thread #{}'.format(count))
    thread.start()

for thread in threads:
    thread.join()
    print('Ending thread #{}'.format(count))
    count -= 1

with progressbar.ProgressBar(max_value=len(prereqs)) as p_bar2:
    count = 0
    for prereq in prereqs:
        table.put_item(
            Item={
                'course_key': prereq['course'],
                'prereqs': prereq['prereqs']
            }
        )
        count += 1
        p_bar2.update(count)
