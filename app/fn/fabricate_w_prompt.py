import time
import json
from bson.objectid import ObjectId

from lib.db_ops import DBOperations
from lib.openai_ops import OpenAIOperations

def deep_serialize(data):
    if isinstance(data, dict):
        return {k: deep_serialize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_serialize(i) for i in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def get_latest_data(collection, property_id):
    obj_id = ObjectId(property_id)
    db_ops = DBOperations()
    data_list = db_ops.find_many(collection, {"property_id":  obj_id}, sort=[("upload_time", -1)])
    return data_list if data_list else None

def fabricate_w_prompt(property_id):
    db_ops = DBOperations()
    openai_ops = OpenAIOperations()
    obj_id = ObjectId(property_id)

    recordings = db_ops.find_many("transcripts", {"property_id": obj_id})

    prompt_fabricate = deep_serialize(db_ops.find_one("prompts", {"name": "fabricate"}))
    prompt_format = openai_ops.MAIN_PROMPTS.get('fabrication_format', '')

    formatted_transcripts = []

    if recordings:
        for recording in recordings:
            formatted_transcripts.append("TRANSCRIPT: " + str(recording["upload_time"]) + " " + recording["transcription"])
    else:
        response = {"error": "No recordings found"}
        return response

    full_prompt = f"{prompt_fabricate.get('value')} {prompt_format} {json.dumps(formatted_transcripts, default=lambda o: str(o) if isinstance(o, ObjectId) else o)}"

    fabricate_result = openai_ops.gpt4_query(full_prompt)

    data = {
        "property_id": str(property_id),
        "upload_time": int(time.time()), 
        "descriptions": fabricate_result,
        "prompt": prompt_fabricate
    }

    data_copy = data.copy()
    data_copy['property_id'] = ObjectId(property_id)

    db_ops.insert_one("descriptions", data_copy)
    return data

