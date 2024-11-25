import pandas as pd
import psycopg2
import requests
from tqdm import tqdm

pd.options.mode.chained_assignment = None


def get_requests(input_data: pd.DataFrame, cursor, conn):
    #preprocess
    url = 'http://localhost:1111/preprocess'
    preprocess_inp = input_data['text'].to_list()
    prep_response = requests.post(url, json=preprocess_inp).json()
    input_data['preprocessed_text'] = prep_response
    input_data = input_data.dropna(subset='preprocessed_text')

    if input_data.empty:
        return

    # translate
    url = 'http://localhost:6666/translation'
    translate_inp = {'text': input_data['preprocessed_text'].to_list(),
                     'from_lang': '',
                     'to_lang': 'rus_Latn'}
    translate_response = requests.post(url, json=translate_inp).json()
    input_data['translated_text'] = translate_response['output']
    input_data = input_data.dropna(subset='translated_text')
    preprocessed_text = input_data['translated_text'].to_list()

    if input_data.empty:
        return

    for _, row in input_data.iterrows():
        cursor.execute(
            'INSERT INTO posts (id, community_id_in_db, message_id, from_id, text, preprocessed_text, '
            'translated_text, views, forwards, reply_to, fwd_from, id_fwd_post, date_time, link ) VALUES '
            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (row['id'],
             row['community_id_in_db'],
             row['message_id'],
             row['from_id'],
             row['text'],
             row['preprocessed_text'],
             row['translated_text'],
             row['views'],
             row['forwards'],
             row['reply_to'],
             row['fwd_from'],
             row['id_fwd_post'],
             row['date_time'],
             row['link'])
        )

        # emotions
    url = 'http://localhost:3333/emotions'
    emotion_inp = preprocessed_text
    emotion_response = requests.post(url, json=emotion_inp).json()
    for i, (_, row) in enumerate(input_data.iterrows()):
        cursor.execute(
            'INSERT INTO emotion (post_id, input_text, emotion, score) VALUES (%s, %s, %s, %s)',
            (row['id'],
             row['text'],
             emotion_response[i][1]['label'],
             emotion_response[i][1]['score'])
        )

        # NER
        url = 'http://localhost:4444/ner'
        ner_inp = preprocessed_text
        ner_response = requests.post(url, json=ner_inp).json()
        for i, (_, row) in enumerate(input_data.iterrows()):
            for num in range(len(ner_response[i][1]['word'])):
                cursor.execute(
                    'INSERT INTO NER (post_id, input_text, ner_entity, ner_type) VALUES (%s, %s, %s, %s)',
                    (row['id'],
                     row['text'],
                     ner_response[i][1]['word'][num],
                     ner_response[i][1]['entity_group'][num])
                )

        # sentiment
        url = 'http://localhost:5555/sentiment'
        sentiment_inp = preprocessed_text
        sentiment_response = requests.post(url, json=sentiment_inp).json()
        for i, (_, row) in enumerate(input_data.iterrows()):
            cursor.execute(
                'INSERT INTO sentiment (post_id, input_text, sentiment, score) VALUES (%s, %s, %s, %s)',
                (row['id'],
                 row['text'],
                 sentiment_response[i]['label'],
                 sentiment_response[i]['score'])
            )

        # zero-shot
        url = 'http://localhost:7777/zero-shot'
        zero_shot_inp = {'text': preprocessed_text,
                         'candidate_labels': '', }
        zero_shot_response = requests.post(url, json=zero_shot_inp).json()
        for i, (_, row) in enumerate(input_data.iterrows()):
            cursor.execute(
                'INSERT INTO zeroshot (post_id, input_text, class1, class2, class3, score1, score2, score3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (row['id'],
                 row['text'],
                 zero_shot_response[i][1]['labels'][0],
                 zero_shot_response[i][1]['labels'][1],
                 zero_shot_response[i][1]['labels'][2],
                 zero_shot_response[i][1]['scores'][0],
                 zero_shot_response[i][1]['scores'][1],
                 zero_shot_response[i][1]['scores'][2],
                 )
            )

        conn.commit()


def main():
    conn = psycopg2.connect(dbname="telegram", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    BATCH_SIZE = 2

    df = pd.read_csv('Posts.csv', sep=';')

    start_row = 0
    num_steps = df.shape[0] // BATCH_SIZE + 1

    for _ in tqdm(range(num_steps)):

        _df = df.iloc[start_row:start_row + BATCH_SIZE]

        try:

            get_requests(_df, cursor, conn)
        except:
            print(_df)
        start_row += BATCH_SIZE


if __name__ == '__main__':
    main()
