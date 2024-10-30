import json

import psycopg2
import uvicorn
from fastapi import FastAPI, File
import fasttext

from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")

app = FastAPI()

@app.post('/detect_language')
def detect_inference(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))

    output = model.predict(inp['text'])

    output = {inp['text'][i]: output[0][i][0].split('__')[-1] for i in range(len(output[0]))}

    for key, value in output.items():

        cursor.execute("INSERT INTO main (request_id, task, input_text, detect_language) VALUES (%s, %s, %s, %s)",
                       ('request_id', 'detect_language', key, value))
    conn.commit()

    return output

if __name__ == '__main__':

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    model = fasttext.load_model(model_path)
    uvicorn.run(app, host='0.0.0.0', port=2222)