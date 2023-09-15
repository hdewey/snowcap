import os

from typing import Union
from celery_tasks.tasks import some_task

from fastapi import FastAPI

from celery import Celery
from celery.result import AsyncResult 

from route_handlers.glean import glean

app = FastAPI()

celery = Celery(__name__)

celery.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
celery.conf.broker_connection_retry_on_startup = True

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/glean")
def do_glean():
    result = glean()
    return result

@app.get("/start_task")
def start_task():
    task = some_task.apply_async()
    return {"message": "task queued", "type": "some_task", "task_id": task.id}

@app.get('/task/{task_id}')
# @token_required
def show_task(task_id):
    """
    View status of a celery task.
    """
    task = AsyncResult(task_id, app=celery)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is pending!'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.result
        }
    elif task.state == 'FAILURE':
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    else:
        response = {
            'state': task.state,
            'status': 'Unknown state'
        }
    return response
