import os
import time

from fn.glean import glean
from fn.scribe import scribe

from fn.fabricate import fabricate
from fn.fabricate_w_prompt import fabricate_w_prompt

from celery import Celery

celery = Celery(__name__)

celery.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
celery.conf.broker_connection_retry_on_startup = True

# Our workflows will be implemented through tasks
# they just run one or multiple named function

# sample task
@celery.task(bind=True)
def some_task(self):
    time.sleep(20)
    return True

# glean task
@celery.task(bind=True)
def glean_task(self, property_id):
    result = glean(property_id)
    return result

@celery.task(bind=True)
def scribe_task(self, filename, property_id):
    result = scribe(filename, property_id)
    return result

@celery.task(bind=True)
def fabricate_task(self, property_id):
    result = fabricate(property_id)
    return result

@celery.task(bind=True)
def fabricate_w_prompt_task(self, property_id):
    result = fabricate_w_prompt(property_id)
    return result