import requests

url = 'http://localhost:2222/detect_language'

text = ['Привет, ты хороший!',
                'Мавҷуда, Мавҷуда зиғамот дил гирам Мавҷуда, Мавҷуда зиғамот дил гирам Ноз макун, ноз макун...', ]

response = requests.post(url, json=text).json()
print(response)

