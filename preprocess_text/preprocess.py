import json
import re

import psycopg2
from fastapi import FastAPI, File
import uvicorn

from clearml import Task

execute_task = Task(task_name='Preprocess text', task_description='prep')
app = FastAPI()

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

@app.post('/preprocess')
def preprocess_text(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))
    inp = inp['text']
    no_emoji = [remove_emoji(text) for text in inp]
    output = {inp[num]: re.sub(r"https?://[^,\s]+,?", "", text) for num, text in enumerate(no_emoji)}

    for key, value in output.items():

        cursor.execute("INSERT INTO main (request_id, task, input_text, preprocessed_text) VALUES (%s, %s, %s, %s)",
                       ('request_id', 'preprocess', key, value))
    conn.commit()
    return output

if __name__ == '__main__':

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()


    uvicorn.run(app, host='0.0.0.0', port=1111)
