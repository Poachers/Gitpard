from celery.task import periodic_task
from celery.schedules import crontab

@periodic_task(ignore_result=True, run_every=crontab(hour=0, minute=1))
def clean_sessions():
    print 'YYYYess'