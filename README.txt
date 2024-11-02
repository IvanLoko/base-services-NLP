1. Классификация языка

    Возможные языки : af als am an ar arz as ast av az azb ba bar bcl be bg bh bn bo bpy br bs bxr ca cbk ce ceb ckb co
    cs cv cy da de diq dsb dty dv el eml en eo es et eu fa fi fr frr fy ga gd gl gn gom gu gv he hi hif hr hsb ht hu hy
    ia id ie ilo io is it ja jbo jv ka kk km kn ko krc ku kv kw ky la lb lez li lmo lo lrc lt lv mai mg mhr min mk ml
    mn mr mrj ms mt mwl my myv mzn nah nap nds ne new nl nn no oc or os pa pam pfl pl pms pnb ps pt qu rm ro ru rue
    sa sah sc scn sco sd sh si sk sl so sq sr su sv sw ta te tg th tk tl tr tt tyv ug uk ur uz vec vep vi vls vo wa
    war wuu xal xmf yi yo yue zh

    входной формат -> json-файл формата
        {"text": List[str]}
    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:2222/detect

    Результат записывается в базу данных postgres в таблицу main в колонки "request_id", "task", "input_text", "detect_language"

========================================================================================================================

2. Классификация эмоции

    входной формат -> json-файл формата
        {"text": List[str]}
    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:3333/emotions

    Результат записывается в базу данных postgres в таблицу main в колонки "request_id", "task", "input_text", "emotion"

========================================================================================================================

3. Named Entity Recognition (NER)

    входной формат -> json-файл формата
        {"text": List[str]}
    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:4444/ner

    Результат записывается в базу данных postgres в таблицу main в колонки "request_id", "task", "input_text", "ner_word", "ner_word"

========================================================================================================================

4. Классификация языка (библиотека polyglot)

    Возможные языки:

      1. Abkhazian                  2. Afar                       3. Afrikaans
      4. Akan                       5. Albanian                   6. Amharic
      7. Arabic                     8. Armenian                   9. Assamese
     10. Aymara                    11. Azerbaijani               12. Bashkir
     13. Basque                    14. Belarusian                15. Bengali
     16. Bihari                    17. Bislama                   18. Bosnian
     19. Breton                    20. Bulgarian                 21. Burmese
     22. Catalan                   23. Cebuano                   24. Cherokee
     25. Nyanja                    26. Corsican                  27. Croatian
     28. Croatian                  29. Czech                     30. Chinese
     31. Chinese                   32. Chinese                   33. Chinese
     34. Chineset                  35. Chineset                  36. Chineset
     37. Chineset                  38. Chineset                  39. Chineset
     40. Danish                    41. Dhivehi                   42. Dutch
     43. Dzongkha                  44. English                   45. Esperanto
     46. Estonian                  47. Ewe                       48. Faroese
     49. Fijian                    50. Finnish                   51. French
     52. Frisian                   53. Ga                        54. Galician
     55. Ganda                     56. Georgian                  57. German
     58. Greek                     59. Greenlandic               60. Guarani
     61. Gujarati                  62. Haitian_creole            63. Hausa
     64. Hawaiian                  65. Hebrew                    66. Hebrew
     67. Hindi                     68. Hmong                     69. Hungarian
     70. Icelandic                 71. Igbo                      72. Indonesian
     73. Interlingua               74. Interlingue               75. Inuktitut
     76. Inupiak                   77. Irish                     78. Italian
     79. Ignore                    80. Javanese                  81. Javanese
     82. Japanese                  83. Kannada                   84. Kashmiri
     85. Kazakh                    86. Khasi                     87. Khmer
     88. Kinyarwanda               89. Krio                      90. Kurdish
     91. Kyrgyz                    92. Korean                    93. Laothian
     94. Latin                     95. Latvian                   96. Limbu
     97. Limbu                     98. Limbu                     99. Lingala
    100. Lithuanian               101. Lozi                     102. Luba_lulua
    103. Luo_kenya_and_tanzania   104. Luxembourgish            105. Macedonian
    106. Malagasy                 107. Malay                    108. Malayalam
    109. Maltese                  110. Manx                     111. Maori
    112. Marathi                  113. Mauritian_creole         114. Romanian
    115. Mongolian                116. Montenegrin              117. Montenegrin
    118. Montenegrin              119. Montenegrin              120. Nauru
    121. Ndebele                  122. Nepali                   123. Newari
    124. Norwegian                125. Norwegian                126. Norwegian_n
    127. Nyanja                   128. Occitan                  129. Oriya
    130. Oromo                    131. Ossetian                 132. Pampanga
    133. Pashto                   134. Pedi                     135. Persian
    136. Polish                   137. Portuguese               138. Punjabi
    139. Quechua                  140. Rajasthani               141. Rhaeto_romance
    142. Romanian                 143. Rundi                    144. Russian
    145. Samoan                   146. Sango                    147. Sanskrit
    148. Scots                    149. Scots_gaelic             150. Serbian
    151. Serbian                  152. Seselwa                  153. Seselwa
    154. Sesotho                  155. Shona                    156. Sindhi
    157. Sinhalese                158. Siswant                  159. Slovak
    160. Slovenian                161. Somali                   162. Spanish
    163. Sundanese                164. Swahili                  165. Swedish
    166. Syriac                   167. Tagalog                  168. Tajik
    169. Tamil                    170. Tatar                    171. Telugu
    172. Thai                     173. Tibetan                  174. Tigrinya
    175. Tonga                    176. Tsonga                   177. Tswana
    178. Tumbuka                  179. Turkish                  180. Turkmen
    181. Twi                      182. Uighur                   183. Ukrainian
    184. Urdu                     185. Uzbek                    186. Venda
    187. Vietnamese               188. Volapuk                  189. Waray_philippines
    190. Welsh                    191. Wolof                    192. Xhosa
    193. Yiddish                  194. Yoruba                   195. Zhuang
    196. Zulu

    входной формат -> json-файл формата
        {"text": List[str]}
    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:9696/polyglot

    Результат записывается в базу данных postgres в таблицу main в колонки "request_id", "task", "input_text", "polyglot_language"

========================================================================================================================

5. Удаление внешних ссылок и эмоджи

    входной формат -> json-файл формата
        {"text": List[str]}
    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:1111/preprocess

    Результат записывается в базу данных postgres в таблицу main в колонки "request_id", "task", "input_text", "preprocessed_text"

========================================================================================================================

6. Классификация тональности

    входной формат -> json-файл формата
        {"text": List[str]}
    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:5555/sentiment

    Результат записывается в базу данных postgres в таблицу main  в колонки "request_id", "task", "input_text", "sentiment"

========================================================================================================================

7. Перевод текста

    Входной формат -> json-файл формата
        {"text": List[str],
        "form_lang": str= '',
        "to_lang": str = ''}

    from_lang:  язык, с которого будет выполнен перевод. Список языков в файле nllb_language -> ALL_LANGUAGES,
     если from_lang: '', язык будет выбран автоматически из nllb_languages -> LANGUAGES
    to_lang: язык на который будет выполнен перевод. Список языков в файле nllb_language -> ALL_LANGUAGES

    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:6666/translation

    Результат записывается в базу данных postgres в таблицу main в колонки "request_id", "task", "input_text","translated_text",
                       "translated_from_language", "translated_to_language"

========================================================================================================================

8. Zero-shot claassification

    Входной формат -> json-файл формата
        {"text": List[str],
        "candidate_labels": List[str] = ''}

    candidate_labels: candidate_labels = '' автоматически формируется список классов как:

                'Политика',
                'Бизнес',
                'Производство',
                'Наука',
                'Еда и Напитки',
                'Здоровье',
                'Семья и дети',
                'Красота и мода',
                'Путешествия',
                'Развлечения',
                'Спорт',
                'Новости',
                'Авто',
                'Праздники',
                'Электроника',
                'Преступность',
                'Связь',
                'Выборы',
                'Религия',
                'Кино',
                'Сериалы',
                'Телевидение',
                'Шоу',
                'Компьютерные игры',
                'Язычество',
                'Война'

    пример curl-запроса -> curl -F "file=@path/to/file.json" -X POST http://10.0.112.2:7777/zero-shot



    Результат записывается в базу данных postgres в таблицу main в колонки "request_id", "task", "input_text", "zero_shot",
                                                            "zero_shot_threshold"




