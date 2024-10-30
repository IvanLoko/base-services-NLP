import json

import psycopg2
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from fastapi import FastAPI, File
import uvicorn

app = FastAPI()

@app.post('/ner')
def ner_inference(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))


    output = nlp(inp['text'])

    result = {}

    for num, text in enumerate(output):
        entity_group = []
        word = []
        for i in text:
            word.append(i['word'])
            entity_group.append(i['entity_group'])
        result[inp['text'][num]] = {'word': word, 'entity_group': entity_group}

    for key, value in result.items():

        cursor.execute("INSERT INTO ma"
                       "in (request_id, task, input_text, ner_word, ner_entity) VALUES (%s, %s, %s, %s, %s)",
                       ('request_id', 'ner', key, value['word'], value['entity_group']))
    conn.commit()

    return result

if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/wikineural-multilingual-ner")
    model = AutoModelForTokenClassification.from_pretrained("Babelscape/wikineural-multilingual-ner")

    nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True, device="cuda:0")
    # print(ner_inference(['Бурятия и Забайкальский край переданы',  'из Сибирского федерального округа ']))

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    # ner_inference()
    uvicorn.run(app, host='0.0.0.0', port=4444)