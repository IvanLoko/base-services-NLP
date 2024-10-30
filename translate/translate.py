import json

import psycopg2
import uvicorn
from fastapi import FastAPI, File
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from langdetect import detect
# from transformers.models.paligemma.convert_paligemma_weights_to_hf import device
import torch

from nllb_languages import get_language_long

app = FastAPI()

class NLLBModel:
    DEFAULT_MODEL = "facebook/nllb-200-distilled-600M"
    DEFAULT_MAX_LENGTH = 1024
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name,
                                                           token='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',
                                                            )
        self.model.to(self.device)
    @staticmethod
    def detect(text: str) -> str:
        detected_language = detect(text)
        return get_language_long(detected_language)

    def translate(self, text: str, from_lng: str,to_lng: str, max_length=DEFAULT_MAX_LENGTH) -> str:

        tokenizer = AutoTokenizer.from_pretrained(self.model_name,
                                                  token='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',
                                                  src_lang=from_lng)
        inputs = tokenizer(text, return_tensors="pt").to(self.device)
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(to_lng),
            max_length=max_length
        )
        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]



@app.post('/translation')
def sentiment_inference(file: bytes = File(...)):

    inp = json.loads(file.decode('utf-8'))

    to_lang = inp['to_lang'] if inp['to_lang'] != '' else 'rus_Cyrl'
    from_lang = nllb.detect(inp['text']) if inp['from_lang'] == '' else inp['from_lang']

    output = [nllb.translate(i, from_lng=from_lang, to_lng=to_lang) for i in inp['text']]

    output = {'input_text': inp['text'],
            'from_lang:': from_lang,
            'to_lang': to_lang,
            'output': output}

    for num, value in enumerate(output['input_text']):

        cursor.execute("INSERT INTO main (request_id, task, input_text, translated_text,"
                       " translated_from_language, translated_to_language) VALUES (%s, %s, %s, %s, %s, %s)",
                       ('request_id', 'translate', value, output['output'][num], from_lang, to_lang))
    conn.commit()

    return output



if __name__ == '__main__':

    nllb = NLLBModel()

    conn = psycopg2.connect(dbname="admindb", user="postgres", password="3115", host="127.0.0.1")
    cursor = conn.cursor()

    uvicorn.run(app, host='0.0.0.0', port=6666)



