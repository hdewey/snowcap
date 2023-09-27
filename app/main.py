import os
from functools import wraps

import jwt

from celery_tasks.tasks import some_task, scribe_task, glean_task, fabricate_task, fabricate_w_prompt_task

from fastapi import FastAPI, HTTPException, Depends, Request 

from starlette.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from celery import Celery
from celery.result import AsyncResult 

from fn.glean import glean
from fn.scribe import scribe
from models import Recording, get_recording

from lib.audio_ops import AudioOperations

async def token_required(request: Request):
    authorization: str = request.headers.get('Authorization')
    if not authorization:
        raise HTTPException(status_code=401, detail="No Authorization header")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except ( Exception):
        raise HTTPException(status_code=401, detail="Token is invalid")

app = FastAPI(client_max_size=100_000_000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

celery = Celery(__name__)

celery.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
celery.conf.broker_connection_retry_on_startup = True 

audio_ops = AudioOperations()

@app.post("/scribe")
async def do_scribe(request: Request, data: Recording = Depends(get_recording)):
    await token_required(request)
    if data.file.filename == '':
        return 'No selected file', 400

    if data.property_id == '':
        return 'No property_id', 400

    tmp_file_path = audio_ops.save_file(data.file)

    task = scribe_task.apply_async(args=[tmp_file_path, data.property_id])
    return {"message": "task queued", "type": "scribe_task", "property_id": data.property_id, "task_id": task.id}

@app.get("/glean")
async def do_glean(request: Request, property_id):
    await token_required(request)
    if property_id == '':
        return 'No property id', 400
    
    task = glean_task.apply_async(args=[property_id])
    return {"message": "task queued", "type": "glean_task", "task_id": task.id}

@app.get("/fabricate")
async def do_fabricate(request: Request, property_id):
    await token_required(request)
    if property_id == '':
        return 'No property id', 400
    
    task = fabricate_task.apply_async(args=[property_id])
    return {"message": "task queued", "type": "fabricate_task", "task_id": task.id}

@app.get("/fabricate_w_prompt")
async def do_fabricate_w_prompt(request: Request, property_id):
    await token_required(request)
    if property_id == '':
        return 'No property id', 400
    
    task = fabricate_w_prompt_task.apply_async(args=[property_id])
    return {"message": "task queued", "type": "fabricate_w_prompt_task", "task_id": task.id}

@app.get("/start_task")
async def start_task(request: Request, ):
    await token_required(request)
    task = some_task.apply_async()
    return {"message": "task queued", "type": "some_task", "task_id": task.id}

@app.get('/task/{task_id}')
# @token_required
async def show_task(request: Request, task_id):
    """
    View status of a celery task.
    """
    await token_required(request)
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
