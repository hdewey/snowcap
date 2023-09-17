import json

import time
from bson.objectid import ObjectId

from lib.db_ops import DBOperations
from lib.openai_ops import OpenAIOperations

def glean(property_id):
    db_ops = DBOperations()
    recordings = db_ops.find_many("transcripts", {"property_id": ObjectId(property_id)})

    formatted_transcripts = []

    if recordings:
        for recording in recordings:
            formatted_transcripts.append("TRANSCRIPT: " + str(recording["upload_time"]) + " " + recording["transcription"])
    else:
        response = {"error": "No recordings found"}
        return response

    openai_ops = OpenAIOperations()
    prompt = openai_ops.MAIN_PROMPTS.get('glean', '')

    full_prompt = prompt + '\n'.join(formatted_transcripts)
    glean_result = openai_ops.gpt4_query(full_prompt)

    data = {
        "property_id": property_id,
        "upload_time": int(time.time()), 
        "property_details": json.loads(glean_result)
    }

    data_copy = data.copy()
    data_copy['property_id'] = ObjectId(property_id)

    db_ops.insert_one("transcript_scan", data_copy)
    return data