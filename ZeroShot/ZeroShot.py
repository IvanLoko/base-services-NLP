import json

import psycopg2
from transformers import pipeline
import uvicorn
from fastapi import FastAPI, File

app = FastAPI()

CANDIDATE_LABELS = [
    'Политика',
    'Бизнес',
    'Производство',
    'Наука',
    'Еда и Напитки',
    'Здоровье',
    'Семья и дети',
    'Красота и мода',
    'Путешествия',
    'Развлечения',
    'Спорт',
    'Новости',
    'Авто',
    'Праздники',
    'Электроника',
    'Преступность',
    'Связь',
    'Выборы',
    'Религия',
    'Кино',
    'Сериалы',
    'Телевидение',
    'Шоу',
    'Компьютерные игры',
    'Язычество',
    'Война'
]


@app.post('/zero-shot')
def zero_shot_inference(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))

    if inp['candidate_labels'] == '':
        candidate_labels = CANDIDATE_LABELS
    else:
        candidate_labels = inp['candidate_labels']

    output = model(inp['text'], candidate_labels, )
    for value in output:

        threshold_zero_shot = [1 if value['scores'][i] > .4 else 0 for i in range(3)]
        print(value)

        cursor.execute("INSERT INTO main (request_id, task, input_text, zero_shot, zero_shot_threshold)"
                       " VALUES (%s, %s, %s, %s, %s)",
                           ('request_id', 'zero-shot', value['sequence'], value['labels'][:3], threshold_zero_shot))
        conn.commit()


    output = {output[i]['sequence']: {'labels': output[i]['labels'][:3], 'scores': output[i]['scores'][:3]} for i in range(len(output))}

    return output

if __name__ == '__main__':

    model = pipeline("zero-shot-classification",
                     model="joeddav/xlm-roberta-large-xnli",
                     device='cuda',
                     multi_label=True)

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    uvicorn.run(app, host='0.0.0.0', port=7777)

    # Первый массив - классы предсказанные алгоритмом
    # Воторой - 1 - выше порога .4, 0 - ниже