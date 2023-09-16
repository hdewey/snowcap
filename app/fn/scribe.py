import json
import openai
import os

from lib.audio_ops import AudioOperations

def scribe(filename: str):
    audio_ops = AudioOperations()
    key = os.getenv('OPENAI_SECRET')
    openai.api_key = key

    filepath = audio_ops.load_file(filename)

    if filepath is None:
        return None

    model = 'whisper-1'

    with open(filepath, 'rb') as audio_file:
        result = openai.Audio.translate(model, audio_file) # use translate to force english

    audio_ops.remove_file(filepath)

    # if result["text"]:
        # print(result["text"])

    response = {"transcription": result["text"]}, 200
    

    return response
