import json

import psycopg2
import uvicorn
from fastapi import FastAPI, File
import fasttext
from typing import List
from huggingface_hub import hf_hub_download

from datetime import datetime


app = FastAPI()

@app.post('/detect_language')
def detect_inference(file: List[str]):

    inp = file

    output = model.predict(inp)
    output = [(inp[i], output[0][i][0].split('__')[-1]) for i in range(len(output[0]))]


    #Task.current_task().upload_artifact(
    #    name=f'temp {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}',
    #    artifact_object=[output],
    #)

    return output

if __name__ == '__main__':

    model_path = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")
    model = fasttext.load_model(model_path)

    uvicorn.run(app, host='0.0.0.0', port=2222)
