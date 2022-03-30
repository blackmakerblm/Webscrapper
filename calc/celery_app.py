from celery import Celery
import time
import os
import sys
#fpath = os.path.join(os.path.dirname(__file__), 'calc')
#sys.path.append(fpath)
print(__name__)
appli = Celery('celery_app',broker="redis://localhost:6379",backend="redis://localhost:6379",include=['calc.tache'])

appli.conf.timezone = 'UTC'
@appli.task
def d():
    return 1
 

appli.conf.beat_schedule = {
    'add-every-3-seconds': {
        'task': 'celery_app.d',
        'schedule': 3.0,
    },
}
