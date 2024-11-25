import json
from transformers import pipeline
import uvicorn
from fastapi import FastAPI
from typing import List
import argparse

app = FastAPI()


@app.post('/emotions')
def sentiment_inference(file: List[str]):
    inp = file

    output = model(inp, **model_kwargs)

    output = [(inp[i], {'label': output[i]['label'], 'score': output[i]['score']}) for i in range(len(output))]

    # Task.current_task().upload_artifact(
    #    name=f'temp {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}',
    #    artifact_object=[output],
    # )

    return output


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--score', type=float, default=0.6)

    args = parser.parse_args()

    model_kwargs = {'max_length': 512}
    model = pipeline('text-classification', model='seara/rubert-base-cased-ru-go-emotions', device=args.device)

    uvicorn.run(app, host='0.0.0.0', port=3333)
