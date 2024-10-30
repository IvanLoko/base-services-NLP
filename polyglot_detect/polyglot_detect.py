import json

import psycopg2
from polyglot.detect import Detector
import uvicorn
from fastapi import FastAPI, File

app = FastAPI()

@app.post('/polyglot', )
def detect_inference(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))

    output = {inp['text'][num]: Detector(i).language.name for num, i in enumerate(inp['text'])}

    for key, value in output.items():

        cursor.execute("INSERT INTO main (request_id, task, input_text, polyglot_language) VALUES (%s, %s, %s, %s)",
                       ('request_id', 'polyglot_language', key, value))
    conn.commit()

    return output

if __name__ == '__main__':

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    uvicorn.run(app, host='0.0.0.0', port=9696)

