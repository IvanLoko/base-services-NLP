from transformers import pipeline
from fastapi import FastAPI, File
import uvicorn
from typing import List
import argparse


app = FastAPI()

@app.post('/sentiment')
def sentiment_inference(file: List[str]):

    inp = file

    output = model(inp, **model_kwargs)

    for num, value in enumerate(output):
        value['text'] = inp[num]

    #Task.current_task().upload_artifact(
    #    name=f'temp {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}',
    #    artifact_object=output,
    #)

    return output


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--score', type=float, default=0.6)

    args = parser.parse_args()

    model_kwargs = {'max_length': 512, 'truncation': True}
    model = pipeline('sentiment-analysis', model='seara/rubert-base-cased-russian-sentiment', device=args.device)

    uvicorn.run(app, host='0.0.0.0', port=5555)
