import json

import psycopg2
from transformers import pipeline
import uvicorn
from fastapi import FastAPI, File

app = FastAPI()

@app.post('/emotions')
def sentiment_inference(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))

    output = model.predict(inp['text'])

    output = {inp['text'][i]: output[i]['label'] for i in range(len(output))}

    for key, value in output.items():
        cursor.execute("INSERT INTO main (request_id, task, input_text, emotion) VALUES (%s, %s, %s, %s)",
                       ('request_id', 'emotion', key, value))
    conn.commit()

    return output


if __name__ == '__main__':

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    model = pipeline('text-classification', model='seara/rubert-base-cased-ru-go-emotions', device='cuda:0')

    uvicorn.run(app, host='0.0.0.0', port=3333)
