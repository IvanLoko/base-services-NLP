from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from fastapi import FastAPI
import uvicorn
from typing import List
import argparse


app = FastAPI()

@app.post('/ner')
def ner_inference(file: List[str]):

    inp = file

    if args.min_len:
        inp = [text for text in inp if len(text) > args.min_len]

    output = nlp(inp)

    result = []

    for num, text in enumerate(output):
        for i in text:
            result.append((inp[num], {'word': i['word'], 'entity_group': i['entity_group']}))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--min_len', type=int, default=None)

    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained("Babelscape/wikineural-multilingual-ner")
    model = AutoModelForTokenClassification.from_pretrained("Babelscape/wikineural-multilingual-ner")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True, device=args.device)

    uvicorn.run(app, host='0.0.0.0', port=4444)
