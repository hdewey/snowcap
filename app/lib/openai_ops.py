import os
import json

import openai

import time

MAX_RETRIES = 3
RETRY_DELAY = 2 

class OpenAIOperations:
    def __init__(self):
        self.key = os.getenv('OPENAI_SECRET')
        self.MAIN_PROMPTS = {}
        self.WRITING_INSTRUCTIONS = {}

        try:
            with open(os.path.join(os.path.dirname(__file__), "../prompts/main_prompts.json"), 'r') as f:
                self.MAIN_PROMPTS = json.load(f)
        except:
            print('Error: Could not open/find prompts/main_prompts.json file')
        
        try:
            with open(os.path.join(os.path.dirname(__file__), "../prompts/writing_instructions.json"), 'r') as f:
                self.WRITING_INSTRUCTIONS = json.load(f)
        except:
            print('Error: Could not open/find prompts/writing_instructions.json file')

    def gpt4_query(self, query):
        openai.api_key = self.key

        for attempt in range(MAX_RETRIES):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a real estate administrator, expert writer, amazing at sales."},
                        {"role": "user", "content": query}
                    ]
                )
                return response.choices[0].message['content']
            except openai.error.OpenAIError as e:
                if attempt < MAX_RETRIES - 1: 
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    raise e

        return response.choices[0].message['content']