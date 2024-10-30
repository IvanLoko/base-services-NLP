import requests

url = 'http://localhost:9696/polyglot'

text = ['Привет, ты хороший!',
                'Мавҷуда, Мавҷуда зиғамот дил гирам Мавҷуда, Мавҷуда зиғамот дил гирам Ноз макун, ноз макун...', ]



response = requests.post(url, json=text).json()
print(response)