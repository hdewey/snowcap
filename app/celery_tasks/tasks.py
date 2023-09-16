import os
import time

from celery import Celery

celery = Celery(__name__)

celery.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
celery.conf.broker_connection_retry_on_startup = True


# Our workflows will be implemented through tasks
# they just run multiple fns

# sample task
@celery.task(bind=True)
def some_task(self):
    time.sleep(20)
    return True

# generate task
@celery.task(bind=True)
def generate_task(self):

    # run a glean()

    # use updated property details to run fabricate()
    time.sleep(10)
    return True