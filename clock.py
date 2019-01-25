from pytz import utc
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger


sched = BlockingScheduler()
sched.configure(timezone=utc)

pre_req_trigger = IntervalTrigger(weeks=3.5)
post_req_trigger =IntervalTrigger(weeks=4)


def pre_req():
    os.system('python3 pre_req.py')
    print('Running pre_req.py.')

def post_req():
    os.system('python3 post_req.py')
    print('Running post_req.py.')

sched.add_job(pre_req, pre_req_trigger)
sched.add_job(post_req, post_req_trigger)

sched.start()
 
