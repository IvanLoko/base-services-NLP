import requests

url = 'http://localhost:9696/zero-shot'

text = {'text': ['Какая гадость эта ваша заливная рыба!',
                 'Украинский коптер атаковал машину в Курской области, погибли два человека'],
        'candidate_labels': ''}

response = requests.post(url, json=text).json()
print(response)