import requests

url = 'http://localhost:9696/sentiment'

text = ['Привет, ты хороший!', 'Привет, ты плохой!', 'Привет, ты нейтральный!']

response = requests.post(url, json=text).json()
print(response)