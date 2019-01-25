from pytz import utc, timezone
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
tz = timezone('EST')



sched = BlockingScheduler()
sched.configure(timezone=utc)
pre_req_trigger=CronTrigger(month='*', hour='0')
post_req_trigger=CronTrigger(month='*', hour='12')


def pre_req():
    os.system('python3 pre_req.py')
    print('Running pre_req.py at {}'.fromat(datetime.now(tz)))

def post_req():
    os.system('python3 post_req.py')
    print('Running post_req.py at {}'.format(datetime.now(tz)))

sched.add_job(pre_req, pre_req_trigger)
sched.add_job(post_req, post_req_trigger)

sched.start()
 
