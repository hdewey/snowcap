import json
import openai
import os
import time
from bson.objectid import ObjectId

from lib.audio_ops import AudioOperations
from lib.db_ops import DBOperations

def scribe(filepath: str, property_id):
    audio_ops = AudioOperations()

    if filepath is None:
        return None

    key = os.getenv('OPENAI_SECRET')
    openai.api_key = key
    model = 'whisper-1'

    with open(filepath, 'rb') as audio_file:
        result = openai.Audio.translate(model, audio_file) # use translate to force english

    audio_ops.remove_file(filepath)

    transcription = result["text"]

    if transcription:
        db_ops = DBOperations()
        
        data = {
            'property_id': property_id,
            'transcription': transcription,
            'upload_time': int(time.time()),
        }

        data_copy = data.copy()
        data_copy['property_id'] = ObjectId(property_id)

        db_ops.insert_one('transcripts', data_copy)

        response = data
    else:
        response = {"error": "transcription_failed"}

    return response
