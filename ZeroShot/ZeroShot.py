from transformers import pipeline
import uvicorn
from fastapi import FastAPI

import argparse
import torch

print(torch.cuda.is_available())

app = FastAPI()

CANDIDATE_LABELS = [
    'Транспорт',
    'Анимация и мультипликация',
    'Военное дело и геополитика',
    'Государственная политика и управление',
    'Дом и сад',
    'Еда и напитки',
    'Животные и растения',
    'Здоровье',
    'Игры',
    'История',
    'Кино и сериалы',
    'Красота и фитнес',
    'Культура и искусство',
    'Люди и общество',
    'Мировая политика',
    'Мода и стиль',
    'Музыка',
    'Наука',
    'Недвижимость',
    'Образование, работа',
    'Промышленность и бизнес',
    'Прочее(без класса)',
    'Психология',
    'Путешествия',
    'Религия',
    'Спорт',
    'Философия',
    'Шопинг',
    'Экономика и финансы',
    'Электроника и технологии',
    'Религиозная напряженность',
    'Национальная напряженность',
    'Политическая напряженность',
    'Социальная напряженность',
    'Общественные формации',
    'Религия',
    'ЛГБТ',
    'Патриотизм',
    'Национальная безопасность',
    'Семья и дети',
    'Катастрофы и теракты',
    'Национализм',
    'Экстремизм',
]


@app.post('/zero-shot')
def zero_shot_inference(file: dict):

    inp = file

    if inp['candidate_labels'] == '':
        candidate_labels = CANDIDATE_LABELS
    else:
        candidate_labels = inp['candidate_labels']

    output = model(inp['text'], candidate_labels, )

    output = [(output[i]['sequence'], {'labels': output[i]['labels'][:3], 'scores': output[i]['scores'][:3]}) for i
              in range(len(output))]

    return output


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--device', type=str, default='cuda:1')
    parser.add_argument('--score', type=float, default=0.6)

    args = parser.parse_args()

    model = pipeline("zero-shot-classification",
                     model="joeddav/xlm-roberta-large-xnli",
                     device='cuda',
                     multi_label=True)

    uvicorn.run(app, host='0.0.0.0', port=7777)

    # Первый массив - классы предсказанные алгоритмом
    # Воторой - 1 - выше порога .4, 0 - ниже
