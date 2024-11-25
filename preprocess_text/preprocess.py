import re

from fastapi import FastAPI
import uvicorn
from typing import List

import argparse


app = FastAPI()


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_url(text):
    return re.sub(r"https?://[^,\s]+,?", "", text)


def remove_tags(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)", " ", text).split())


def remove_hashtags(text):
    return ' '.join(re.sub("(#[A-Za-z0-9]+)", " ", text).split())


@app.post('/preprocess')
def preprocess_text(file: List[str]):
    output = file

    if args.min_len:
        output = [text for text in output if (len(text) > args.min_len) and (len(text) < args.max_len)]

    if args.remove_emoji:
        output = [remove_emoji(text) for text in output]
    if args.remove_url:
        output = [remove_url(text) for text in output]
    if args.remove_hashtag:
        output = [remove_hashtags(text) for text in output]
    if args.remove_tag:
        output = [remove_tags(text) for text in output]

    output = [text if text != '' else None for text in output]

    return output


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--min_len', type=int, default=None)
    parser.add_argument('--max_len', type=int, default=float('inf'))
    parser.add_argument('--remove_url', type=bool, default=True)
    parser.add_argument('--remove_tag', type=bool, default=True)
    parser.add_argument('--remove_hashtag', type=bool, default=True)
    parser.add_argument('--remove_emoji', type=bool, default=True)

    args = parser.parse_args()

    uvicorn.run(app, host='0.0.0.0', port=1111)
