import requests

url = 'http://localhost:6666/translation'

input_request = {'text': 'Атакем мен сени ойлоп сагынамын'
                         'Аска зоом сен эленго таянарым'
                         'Аттин ай бул да сенин эркин эмес'
                         'Армандуу тагдырыма таарынамын',
                 'from_lang': 'uzn_Latn',
                 'to_lang': ''}

response = requests.post(url, json=input_request).json()
print(response)

