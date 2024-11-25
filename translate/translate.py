import json

import psycopg2
import requests
import uvicorn
from fastapi import FastAPI, File
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from langdetect import detect
import torch
import argparse


app = FastAPI()

LANGUAGES = [
    {"long": "afr_Latn", "short": "af", "name": "Afrikaans"},
    {"long": "als_Latn", "short": "sq", "name": "Albanian"},
    {"long": "amh_Ethi", "short": "am", "name": "Amharic"},
    {"long": "arb_Arab", "short": "ar", "name": "Arabic"},
    {"long": "ast_Latn", "short": "ast", "name": "Asturian"},
    {"long": "azj_Latn", "short": "az", "name": "Azerbaijani"},
    {"long": "bel_Cyrl", "short": "be", "name": "Belarusian"},
    {"long": "ben_Beng", "short": "bn", "name": "Bengali"},
    {"long": "bul_Cyrl", "short": "bg", "name": "Bulgarian"},
    {"long": "cat_Latn", "short": "ca", "name": "Catalan"},
    {"long": "ceb_Latn", "short": "ceb", "name": "Cebuano"},
    {"long": "ces_Latn", "short": "cs", "name": "Czech"},
    {"long": "cym_Latn", "short": "cy", "name": "Welsh"},
    {"long": "dan_Latn", "short": "da", "name": "Danish"},
    {"long": "deu_Latn", "short": "de", "name": "German"},
    {"long": "ell_Grek", "short": "el", "name": "Greek"},
    {"long": "eng_Latn", "short": "en", "name": "English"},
    {"long": "epo_Latn", "short": "eo", "name": "Esperanto"},
    {"long": "est_Latn", "short": "et", "name": "Estonian"},
    {"long": "fin_Latn", "short": "fi", "name": "Finnish"},
    {"long": "fra_Latn", "short": "fr", "name": "French"},
    {"long": "gaz_Latn", "short": "om", "name": "Oromo"},
    {"long": "gla_Latn", "short": "gd", "name": "Scottish Gaelic"},
    {"long": "gle_Latn", "short": "ga", "name": "Irish"},
    {"long": "glg_Latn", "short": "gl", "name": "Galician"},
    {"long": "hau_Latn", "short": "ha", "name": "Hausa"},
    {"long": "heb_Hebr", "short": "he", "name": "Hebrew"},
    {"long": "hin_Deva", "short": "hi", "name": "Hindi"},
    {"long": "hrv_Latn", "short": "hr", "name": "Croatian"},
    {"long": "hun_Latn", "short": "hu", "name": "Hungarian"},
    {"long": "hye_Armn", "short": "hy", "name": "Armenian"},
    {"long": "ibo_Latn", "short": "ig", "name": "Igbo"},
    {"long": "ilo_Latn", "short": "ilo", "name": "Ilocano"},
    {"long": "ind_Latn", "short": "id", "name": "Indonesian"},
    {"long": "isl_Latn", "short": "is", "name": "Icelandic"},
    {"long": "ita_Latn", "short": "it", "name": "Italian"},
    {"long": "jav_Latn", "short": "jv", "name": "Javanese"},
    {"long": "jpn_Jpan", "short": "ja", "name": "Japanese"},
    {"long": "kat_Geor", "short": "ka", "name": "Georgian"},
    {"long": "kaz_Cyrl", "short": "kk", "name": "Kazakh"},
    {"long": "khm_Khmr", "short": "km", "name": "Khmer"},
    {"long": "kor_Hang", "short": "ko", "name": "Korean"},
    {"long": "lit_Latn", "short": "lt", "name": "Lithuanian"},
    {"long": "ltz_Latn", "short": "lb", "name": "Luxembourgish"},
    {"long": "lug_Latn", "short": "lg", "name": "Ganda"},
    {"long": "lvs_Latn", "short": "lv", "name": "Latvian"},
    {"long": "mal_Mlym", "short": "ml", "name": "Malayalam"},
    {"long": "mar_Deva", "short": "mr", "name": "Marathi"},
    {"long": "mkd_Cyrl", "short": "mk", "name": "Macedonian"},
    {"long": "mya_Mymr", "short": "my", "name": "Burmese"},
    {"long": "nld_Latn", "short": "nl", "name": "Dutch"},
    {"long": "nob_Latn", "short": "no", "name": "Norwegian Bokmål"},
    {"long": "npi_Deva", "short": "ne", "name": "Nepali"},
    {"long": "oci_Latn", "short": "oc", "name": "Occitan"},
    {"long": "ory_Orya", "short": "or", "name": "Odia"},
    {"long": "pes_Arab", "short": "fa", "name": "Persian"},
    {"long": "plt_Latn", "short": "mg", "name": "Malagasy"},
    {"long": "pol_Latn", "short": "pl", "name": "Polish"},
    {"long": "por_Latn", "short": "pt", "name": "Portuguese"},
    {"long": "ron_Latn", "short": "ro", "name": "Romanian"},
    {"long": "rus_Cyrl", "short": "ru", "name": "Russian"},
    {"long": "sin_Sinh", "short": "si", "name": "Sinhala"},
    {"long": "slk_Latn", "short": "sk", "name": "Slovak"},
    {"long": "slv_Latn", "short": "sl", "name": "Slovenian"},
    {"long": "snd_Arab", "short": "sd", "name": "Sindhi"},
    {"long": "som_Latn", "short": "so", "name": "Somali"},
    {"long": "spa_Latn", "short": "es", "name": "Spanish"},
    {"long": "srp_Cyrl", "short": "sr", "name": "Serbian"},
    {"long": "sun_Latn", "short": "su", "name": "Sundanese"},
    {"long": "swe_Latn", "short": "sv", "name": "Swedish"},
    {"long": "swh_Latn", "short": "sw", "name": "Swahili"},
    {"long": "tam_Taml", "short": "ta", "name": "Tamil"},
    {"long": "tat_Cyrl", "short": "tt", "name": "Tatar"},
    {"long": "tgl_Latn", "short": "tl", "name": "Tagalog"},
    {"long": "tur_Latn", "short": "tr", "name": "Turkish"},
    {"long": "ukr_Cyrl", "short": "uk", "name": "Ukrainian"},
    {"long": "urd_Arab", "short": "ur", "name": "Urdu"},
    {"long": "uzn_Latn", "short": "uz", "name": "Uzbek"},
    {"long": "vie_Latn", "short": "vi", "name": "Vietnamese"},
    {"long": "wol_Latn", "short": "wo", "name": "Wolof"},
    {"long": "xho_Latn", "short": "xh", "name": "Xhosa"},
    {"long": "ydd_Hebr", "short": "yi", "name": "Yiddish"},
    {"long": "yor_Latn", "short": "yo", "name": "Yoruba"},
    {"long": "zho_Hans", "short": "zh", "name": "Chinese (Simplified)"},
    {"long": "zsm_Latn", "short": "ms", "name": "Malay"},
    {"long": "zul_Latn", "short": "zu", "name": "Zulu"},
]  # Список автоматически определяесмых языков
SHORT_TO_LONG = {lang['short']: lang['long'] for lang in LANGUAGES}
LONG_TO_SHORT = {lang['long']: lang['short'] for lang in LANGUAGES}


def get_language_long(short):
    """Get a long language name by its short name"""
    return SHORT_TO_LONG[short]


def get_language_short(long):
    """Get a short language name by its long name"""
    return LONG_TO_SHORT.get(long)


ALL_LANGUAGES = {'ace_Arabnew': 'Acehnese Arabic',
                 'ace_Latnnew': 'Acehnese Latin',
                 'acm_Arabnew': 'Mesopotamian Arabic',
                 'acq_Arabnew': 'Taʽizzi-Adeni Arabic',
                 'aeb_Arabnew': 'Tunisian Arabic',
                 'afr_Latn Afrikaans': 'Latin',
                 'ajp_Arabnew South': 'Levantine',
                 'aka_Latnnew': 'Akan',
                 'amh_Ethi': 'Amharic',
                 'apc_Arabnew': 'North Levantine',
                 'arb_Arab': 'Modern Standard Arabic',
                 'arb_Latnnew': 'Modern Standard Arabic',
                 'ars_Arabnew': 'Najdi Arabic',
                 'ary_Arabnew': 'Moroccan',
                 'arz_Arabnew': 'Egyptian',
                 'asm_Beng': 'Assamese',
                 'ast_Latn': 'Asturian',
                 'awa_Devanew': 'Awadhi',
                 'ayr_Latnnew': 'Central Aymara',
                 'azj_Latn North': 'Azerbaijani',
                 'bak_Cyrlnew': 'Bashkir',
                 'bam_Latnnew': 'Bambara',
                 'ban_Latnnew': 'Balinese',
                 'bel_Cyrl': 'Belarusian',
                 'bem_Latnnew': 'Bemba',
                 'ben_Beng': 'Bengali',
                 'bho_Devanew': 'Bhojpuri',
                 'bjn_Arabnew': 'Banjar',
                 'bjn_Latnnew': 'Banjar',
                 'bod_Tibtnew': 'Standard Tibetan',
                 'bos_Latn': 'Bosnian',
                 'bug_Latnnew': 'Buginese',
                 'bul_Cyrl': 'Bulgarian',
                 'cat_Latn': 'Catalan',
                 'ceb_Latn': 'Cebuano',
                 'ces_Latn': 'Czech',
                 'cjk_Latnnew': 'Chokwe',
                 'ckb_Arab': 'Central Kurdish',
                 'crh_Latnnew': 'Crimean',
                 'cym_Latn': 'Welsh',
                 'dan_Latn': 'Danish',
                 'deu_Latn': 'German',
                 'dik_Latnnew': 'Southwestern Dinka',
                 'dyu_Latnnew': 'Dyula',
                 'dzo_Tibtnew': 'Dzongkha',
                 'ell_Grek': 'Greek',
                 'eng_Latn': 'English',
                 'epo_Latnnew': 'Esperanto',
                 'est_Latn': 'Estonian',
                 'eus_Latnnew': 'Basque',
                 'ewe_Latnnew': 'Ewe',
                 'fao_Latnnew': 'Faroese',
                 'fij_Latnnew': 'Fijian',
                 'fin_Latn': 'Finnish',
                 'fon_Latnnew': 'Fon',
                 'fra_Latn': 'French',
                 'fur_Latnnew': 'Friulian',
                 'fuv_Latn': 'Nigerian Fulfulde',
                 'gla_Latnnew': 'Scottish Gaelic',
                 'gle_Latn': 'Irish',
                 'glg_Latn': 'Galician',
                 'grn_Latnnew': 'Guarani',
                 'guj_Gujr': 'Gujarati',
                 'hat_Latnnew': 'Haitian Creole',
                 'hau_Latn': 'Hausa Latin',
                 'heb_Hebr': 'Hebrew Hebrew',
                 'hin_Deva': 'Hindi Devanagari',
                 'hne_Devanew': 'Chhattisgarhi',
                 'hrv_Latn': 'Croatian',
                 'hun_Latn': 'Hungarian',
                 'hye_Armn': 'Armenian',
                 'ibo_Latn': 'Igbo Latin',
                 'ilo_Latnnew': 'Ilocano',
                 'ind_Latn': 'Indonesian',
                 'isl_Latn': 'Icelandic',
                 'ita_Latn': 'Italian',
                 'jav_Latn': 'Javanese',
                 'jpn_Jpan': 'Japanese',
                 'kab_Latnnew': 'Kabyle',
                 'kac_Latnnew': 'Jingpho',
                 'kam_Latn': 'Kamba',
                 'kan_Knda': 'Kannada',
                 'kas_Arabnew': 'Kashmiri',
                 'kas_Devanew': 'Kashmiri',
                 'kat_Geor': 'Georgian',
                 'knc_Arabnew': 'Central Kanuri',
                 'knc_Latnnew': 'Central Kanuri',
                 'kaz_Cyrl': 'Kazakh',
                 'kbp_Latnnew': 'Kabiyè',
                 'kea_Latnnew': 'Kabuverdianu',
                 'khm_Khmr': 'Khmer',
                 'kik_Latnnew': 'Kikuyu',
                 'kin_Latnnew': 'Kinyarwanda',
                 'kir_Cyrl': 'Kyrgyz',
                 'kmb_Latnnew': 'Kimbundu',
                 'kmr_Latnnew': 'Northern Kurdish',
                 'kon_Latnnew': 'Kikongo',
                 'kor_Hang': 'Korean',
                 'lao_Laoo': 'Lao',
                 'lij_Latnnew': 'Ligurian',
                 'lim_Latnnew': 'Limburgish',
                 'lin_Latn': 'Lingala',
                 'lit_Latn': 'Lithuanian',
                 'lmo_Latnnew': 'Lombard',
                 'ltg_Latnnew': 'Latgalian',
                 'ltz_Latn': 'Luxembourgish',
                 'lua_Latnnew': 'Luba-Kasai',
                 'lug_Latn': 'Ganda',
                 'luo_Latn': 'Luo',
                 'lus_Latnnew': 'Mizo',
                 'lvs_Latn': 'Standard Latvian',
                 'mag_Devanew': 'Magahi',
                 'mai_Devanew': 'Maithili',
                 'mal_Mlym': 'Malayalam',
                 'mar_Deva': 'Marathi',
                 'min_Arabnew': 'Minangkabau',
                 'min_Latnnew': 'Minangkabau',
                 'mkd_Cyrl': 'Macedonian',
                 'plt_Latnnew': 'Plateau Malagasy',
                 'mlt_Latn': 'Maltese',
                 'mni_Bengnew': 'Meitei',
                 'khk_Cyrl Halh': 'Mongolian',
                 'mos_Latnnew': 'Mossi',
                 'mri_Latn': 'Maori',
                 'mya_Mymr': 'Burmese',
                 'nld_Latn': 'Dutch',
                 'nno_Latnnew': 'Norwegian Nynorsk',
                 'nob_Latn': 'Norwegian Bokmål',
                 'npi_Deva': 'Nepali',
                 'nso_Latn': 'Northern Sotho',
                 'nus_Latnnew': 'Nuer',
                 'nya_Latn': 'Nyanja',
                 'oci_Latn': 'Occitan',
                 'gaz_Latnnew': 'West Central Oromo',
                 'ory_Orya': 'Odia',
                 'pag_Latnnew': 'Pangasinan',
                 'pan_Guru': 'Eastern Panjabi',
                 'pap_Latnnew': 'Papiamento',
                 'pes_Arab': 'Western Persian',
                 'pol_Latn': 'Polish',
                 'por_Latn': 'Portuguese',
                 'prs_Arabnew': 'Dari',
                 'pbt_Arab': 'Southern Pashto',
                 'quy_Latnnew': 'Ayacucho Quechua',
                 'ron_Latn': 'Romanian',
                 'run_Latnnew': 'Rundi',
                 'rus_Cyrl': 'Russian',
                 'sag_Latnnew': 'Sango',
                 'san_Devanew': 'Sanskrit',
                 'sat_Olcknew': 'Santali',
                 'scn_Latnnew': 'Sicilian',
                 'shn_Mymrnew': 'Shan',
                 'sin_Sinhnew': 'Sinhala',
                 'slk_Latn': 'Slovak',
                 'slv_Latnnew': 'Slovenian',
                 'smo_Latnnew': 'Samoan',
                 'sna_Latn': 'Shona',
                 'snd_Arab': 'Sindhi A',
                 'som_Latn': 'Somali',
                 'sot_Latnnew': 'Southern Sotho',
                 'spa_Latn': 'Spanish',
                 'als_Latnnew': 'Tosk Albanian',
                 'srd_Latnnew': 'Sardinian',
                 'srp_Cyrl': 'Serbian',
                 'ssw_Latnnew': 'Swati',
                 'sun_Latnnew': 'Sundanese',
                 'swe_Latn': 'Swedish',
                 'swh_Latn': 'Swahili',
                 'szl_Latnnew': 'Silesian',
                 'tam_Taml': 'Tamil',
                 'tat_Cyrlnew': 'Tatar',
                 'tel_Telu': 'Telugu',
                 'tgk_Cyrl': 'Tajik',
                 'tgl_Latn': 'Tagalog',
                 'tha_Thai': 'Thai',
                 'tir_Ethinew': 'Tigrinya',
                 'taq_Latnnew': 'Tamasheq',
                 'taq_Tfngnew': 'Tamasheq',
                 'tpi_Latnnew': 'Tok Pisin',
                 'tsn_Latnnew': 'Tswana',
                 'tso_Latnnew': 'Tsonga',
                 'Code Language': 'Script',
                 'tuk_Latnnew': 'Turkmen',
                 'tum_Latnnew': 'Tumbuka',
                 'tur_Latn': 'Turkish',
                 'twi_Latnnew': 'Twi',
                 'tzm_Tfngnew': 'Central Atlas Tamazight',
                 'uig_Arabnew': 'Uyghur',
                 'ukr_Cyrl': 'Ukrainian',
                 'umb_Latn': 'Umbundu',
                 'urd_Arab': 'Urdu',
                 'uzn_Latn': 'Northern Uzbek',
                 'vec_Latnnew': 'Venetian',
                 'vie_Latn': 'Vietnamese',
                 'war_Latnnew': 'Waray',
                 'wol_Latn': 'Wolof',
                 'xho_Latn': 'Xhosa',
                 'ydd_Hebrnew': 'Eastern Yiddish',
                 'yor_Latn': 'Yoruba',
                 'yue_Hantnew': 'Yue Chinese',
                 'zho_Hans': 'Chinese Han (Simplified)',
                 'zho_Hant': 'Chinese Han (Traditional)',
                 'zsm_Latn': 'Standard Malay',
                 'zul_Latn': 'Zulu'}  # все языки


class NLLBModel:
    DEFAULT_MODEL = "facebook/nllb-200-distilled-600M"
    DEFAULT_MAX_LENGTH = 1024

    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name,
                                                           token='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',
                                                           )
        self.model.to(args.device)

    @staticmethod
    def detect(text: str) -> str:
        detected_language = detect(text)
        return get_language_long(detected_language)

    def translate(self, text: str, from_lng: str, to_lng: str, max_length=DEFAULT_MAX_LENGTH) -> str:
        tokenizer = AutoTokenizer.from_pretrained(self.model_name,
                                                  token='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',
                                                  src_lang=from_lng)
        inputs = tokenizer(text, return_tensors="pt").to(args.device)
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(to_lng),
            max_length=max_length
        )
        return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]


@app.post('/translation')
def sentiment_inference(file: dict):
    inp = file

    to_lang = inp['to_lang'] if inp['to_lang'] != '' else 'rus_Cyrl'

    url = 'http://localhost:2222/detect_language'
    response_langs = requests.post(url, json=inp['text']).json()


    output = [nllb.translate(text, from_lng=lang, to_lng=to_lang) if lang != 'rus_Cyrl' else text for text, lang in
              response_langs]
    output = [text if text != '' else None for text in output]

    output = {'input_text': inp['text'],
              'from_lang:': [i[1] for i in response_langs],
              'to_lang': [to_lang] * len(inp['text']),
              'output': output}

    #Task.current_task().upload_artifact(
    #    name=f'temp {datetime.now().strftime("%Y-%m-%d-%H:%M:%S")}',
    #    artifact_object=output,
    #)

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--device', type=str, default='cuda')

    args = parser.parse_args()

    nllb = NLLBModel()

    uvicorn.run(app, host='0.0.0.0', port=6666)

