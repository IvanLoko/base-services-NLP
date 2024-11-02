import json

import psycopg2
from transformers import pipeline
from fastapi import FastAPI, File
import uvicorn

app = FastAPI()



@app.post('/sentiment')
def sentiment_inference(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))

    output = model.predict(inp['text'])

    for num, value in enumerate(output):
        value['text'] = inp['text'][num]

    for val in output:

        cursor.execute("INSERT INTO main (request_id, task, input_text, sentiment) VALUES (%s, %s, %s, %s)",
                       ('request_id', 'sentiment', val['text'], val['label']))
    conn.commit()

    return output

if __name__ == '__main__':
    model = pipeline('sentiment-analysis', model='seara/rubert-base-cased-russian-sentiment', device='cuda')

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    uvicorn.run(app, host='0.0.0.0', port=5555)
