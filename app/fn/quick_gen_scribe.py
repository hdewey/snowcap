import os
import time
import json

from bson.objectid import ObjectId

import openai

from lib.db_ops import DBOperations
from lib.audio_ops import AudioOperations
from lib.openai_ops import OpenAIOperations

def quick_gen_scribe(filepath: str, property_id: str):
    audio_ops = AudioOperations()
    
    if filepath is None:
        return None

    key = os.getenv('OPENAI_SECRET')
    openai.api_key = key
    model = 'whisper-1'
    
    with open(filepath, 'rb') as audio_file:
        result = openai.Audio.translate(model, audio_file) # use translate to force english

    audio_ops.remove_file(filepath)

    description = result["text"]

    if description is None:
        return ''

    db_ops = DBOperations()
 
    openai_ops = OpenAIOperations()
    prompt = openai_ops.MAIN_PROMPTS.get('fabricate', '')
    format_prompt = openai_ops.MAIN_PROMPTS.get('fabrication_format', '')
    full_prompt = f"{prompt} {format_prompt} Property Details: {description}"

    fabricate_result = openai_ops.gpt4_query(full_prompt)

    data = {
        "property_id": property_id,
        "upload_time": int(time.time()), 
        "descriptions": fabricate_result,
        "property_details": description, 
    }

    data_copy = data.copy()
    data_copy['property_id'] = ObjectId(property_id)

    db_ops.insert_one("descriptions", data_copy)
    return data