import time
import json
from bson.objectid import ObjectId

from lib.db_ops import DBOperations
from lib.openai_ops import OpenAIOperations

from fn.glean import glean

db_ops = DBOperations()

def get_latest_data(collection, property_id):
    data_list = db_ops.find_many(collection, {"property_id":  ObjectId(property_id)}, sort=[("upload_time", -1)], limit=1)
    return data_list[0] if data_list else None

def fabricate(property_id):

    cached_property_details = get_latest_data("transcript_scan", property_id)
    last_recording = get_latest_data("recordings", property_id)

    property_details = cached_property_details or glean(property_id)

    if last_recording and (not cached_property_details or last_recording.get('upload_time', 0) > cached_property_details.get('upload_time', 0)):
        property_details = last_recording

    openai_ops = OpenAIOperations()
    prompt = openai_ops.MAIN_PROMPTS.get('fabricate', '')
    format_prompt = openai_ops.MAIN_PROMPTS.get('fabrication_format', '')
    full_prompt = f"{prompt} {format_prompt} Property Details: {json.dumps(property_details, default=lambda o: str(o) if isinstance(o, ObjectId) else o)}"

    fabricate_result = openai_ops.gpt4_query(full_prompt)

    data = {
        "property_id": property_id,
        "upload_time": int(time.time()), 
        "descriptions": fabricate_result
    }

    data_copy = data.copy()
    data_copy['property_id'] = ObjectId(property_id)

    db_ops.insert_one("descriptions", data_copy)
    return data