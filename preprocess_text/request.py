import requests
from sympy import pprint

url = 'http://localhost:1111/preprocess'

text = ["не обращать вынимание это тестовый текст 😂😂😄😄😢😢😄😌😢😀😀😱😡😭😳 https://www.google.com/search?client=ubuntu-sn&channel=fs&q=print+dict+rhfcbdj+ рандомная ссылка https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304bТУТДОЛЖЕНБЫТЬТЕКСТ А ЕГО НЕТ ",
        'Просто текст? Мб для теста... ???']

response = requests.post(url, json=text).json()
print(response)