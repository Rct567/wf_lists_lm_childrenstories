

from functools import cache, partial
import html
import os
import re
import sys
import time
from typing import Callable, Generator, Iterable, NewType, Optional
from openai import OpenAI

STORIES_DIR = "stories"
TITLES_DIR = "titles"
WF_LISTS_DIR = "wf_lists"


lm_caller_num_errors = 0

def get_lm_caller(api_base: str, api_key: str, model: str, temperature: float, frequency_penalty: float, presence_penalty: float):

    client = OpenAI(base_url=api_base, api_key=api_key)

    def call_local_lm(prompt_text: str, lang_id: str) -> Optional[tuple[str, str, str, str, float]]:
        messages = [
            {"role": "system", "content": "You are a creative children's story writer."},
            {"role": "user", "content": prompt_text}
        ]
        assert temperature > 0 and temperature <= 2
        assert frequency_penalty > -2 and frequency_penalty <= 2
        assert presence_penalty > -2 and presence_penalty <= 2
        try:
            start_time = time.perf_counter()
            response = client.chat.completions.create( # type: ignore
                model=model,
                messages=messages, # type: ignore
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            response_content = response.choices[0].message.content
            if not response_content:
                return None
            time_taken = time.perf_counter() - start_time
            #print("\n===========================\n"+response_content+"\n===========================\n")
            return (response_content, prompt_text, model, lang_id, time_taken)

        except Exception as error:
            global lm_caller_num_errors
            lm_caller_num_errors += 1
            print("Error while getting response from LM: {}".format(error))
            if lm_caller_num_errors > 10:
                print("Too many errors. Exiting.")
                sys.exit(1)
            return None

    return call_local_lm


import spacy
from spacy.tokens import Doc
from spacy.language import Language

loaded_spacy: dict[str, Language] = {}

def get_spacy_pipeline(lang_code: str) -> Language:

    global loaded_spacy

    if lang_code in loaded_spacy:
        return loaded_spacy[lang_code]

    model_mapping = {
        'th': "th_core_news_sm", # Thai
        'bo': "xx_ent_wiki_sm",  # Tibetan
    }

    model_name = model_mapping.get(lang_code)
    if model_name:
        return spacy.load(model_name)

    if lang_code == "zh":
        import jieba
        jieba.setLogLevel(20)
        cfg = {"segmenter": "jieba"}
        nlp = spacy.blank(lang_code).from_config(
            {"nlp": {"tokenizer": cfg}}
        )
    elif lang_code == 'ja':

        nlp = spacy.blank(lang_code)

        import MeCab

        class MecabTokenizer:
            def __init__(self, nlp: Language):
                self.mecab = MeCab.Tagger()
                self.vocab = nlp.vocab

            def __call__(self, text: str) -> Doc:
                tokens = []
                node = self.mecab.parseToNode(text)
                while node:
                    if node.surface.strip():
                        tokens.append(node.surface)
                    node = node.next
                return Doc(self.vocab, words=tokens)

        # Assign custom tokenizer
        nlp.tokenizer = MecabTokenizer(nlp)
    elif lang_code == "km":
        from khmernltk import word_tokenize as khmer_tokenizer
        def custom_khmer_tokenizer(nlp: Language, text: str) -> Doc:
            tokens: list[str] = khmer_tokenizer(text)
            return Doc(nlp.vocab, words=tokens)
        nlp = spacy.blank('xx')
        nlp.tokenizer = lambda text: custom_khmer_tokenizer(nlp, text)
    elif lang_code == "lo":
        from laonlp.tokenize import word_tokenize as lao_tokenizer
        def custom_lao_tokenizer(nlp: Language, text: str) -> Doc:
            tokens: list[str] = [str(token) for token in lao_tokenizer(text)]
            return Doc(nlp.vocab, words=tokens)
        nlp = spacy.blank('xx')
        nlp.tokenizer = lambda text: custom_lao_tokenizer(nlp, text)
    else:
        #nlp = spacy.blank(lang_code)
        raise Exception("Should Spacy be used for {}?".format(lang_code))

    loaded_spacy[lang_code] = nlp

    return nlp


WordToken = NewType('WordToken', str)
Tokenizer = Callable[[str], list[str]]

class TextProcessing:

    CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]{1,}', re.UNICODE)
    JAPANESE_PATTERN = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf\uf900-\ufaff\u3400-\u4dbf]{1,}', re.UNICODE)
    KOREAN_PATTERN = re.compile(r'[\uac00-\ud7a3]{1,}', re.UNICODE)
    ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF]{1,}', re.UNICODE)
    ETHIOPIC_PATTERN = re.compile(r'[\u1200-\u137F]{1,}', re.UNICODE)
    THAI_PATTERN = re.compile(r'[\u0e00-\u0e7f]{1,}', re.UNICODE)
    LAO_PATTERN = re.compile(r'[\u0e80-\u0eff]{1,}', re.UNICODE)
    KHMER_PATTERN = re.compile(r'[\u1780-\u17ff]{1,}', re.UNICODE)
    DEFAULT_PATTERN = re.compile(r'[^\W\d_]{2,}', re.UNICODE)

    @staticmethod
    def get_word_accepter(lang_id: Optional[str]) -> Callable[[str], bool]:

        min_length = 1
        if lang_id == 'zh':
            word_pattern = TextProcessing.CHINESE_PATTERN
        elif lang_id == 'ja':
            word_pattern = TextProcessing.JAPANESE_PATTERN
        elif lang_id == 'ko':
            word_pattern = TextProcessing.KOREAN_PATTERN
        elif lang_id == 'ar':
            word_pattern = TextProcessing.ARABIC_PATTERN
        elif lang_id is not None and str(lang_id) in {'am', 'ti', 'om', 'so', 'ha'}:
            word_pattern = TextProcessing.ETHIOPIC_PATTERN
        elif lang_id == 'th':
            word_pattern = TextProcessing.THAI_PATTERN
        elif lang_id == 'lo':
            word_pattern = TextProcessing.LAO_PATTERN
        elif lang_id == 'km':
            word_pattern = TextProcessing.KHMER_PATTERN
        else:
            word_pattern = TextProcessing.DEFAULT_PATTERN
            min_length = 2

        def is_acceptable_word_for_lang(word: str) -> bool:

            stripped_word = word.strip("!@#$%^&*()_-=+{}:\"<>?,./;' ")
            stripped_word_len = len(stripped_word)
            if stripped_word_len < min_length or stripped_word_len > 300:
                return False

            return re.search(word_pattern, stripped_word) is not None

        return is_acceptable_word_for_lang

    @staticmethod
    def get_plain_text(val: str) -> str:
        val = re.sub(r'<(style|head|script|object|noscript|embed|noembed|applet|canvas)(.*?)>(.*?)</\1>', ' ', val, flags=re.DOTALL)
        val = re.sub(r'</?(br|p|hr|div|pre|blockquote|h[1-6]|ul|ol|li|table|tr|td|th|dl|dd|dt)([^>]*)>', ' ', val, flags=re.IGNORECASE)
        val = re.sub(r'<[^>]+>', '', val)
        val = re.sub(r"\[(sound|type):[^]]+\]", " ", val)
        val = html.unescape(val)
        val = re.sub(r'[\s]+', ' ', val)
        return val.strip()

    @staticmethod
    def create_word_token(text: str, lang_id: str) -> WordToken:

        assert "\t" not in text and "\n" not in text and "\r" not in text

        token = text.strip(".,'’\"' \t\n\r!@#$%^&*()_-=+{}:\"<>?/;")

        if '’' in token and lang_id in {"en", "fr", "it", "de", "es"}:
            token = token.replace("’", "'")

        return WordToken(token.lower())

    @staticmethod
    def default_tokenizer(text: str) -> list[str]:
        text = str(text+" ").replace(". ", " ")
        # Arabic diacritical marks: u0610-\u061A\u064B-\u065F
        non_word_chars = r"[^\w\-\_\'\’\.\u0610-\u061A\u064B-\u065F]{1,}"
        return re.split(non_word_chars, text)

    @staticmethod
    def default_tokenizer_removing_possessives(text: str) -> list[str]:

        tokens = TextProcessing.default_tokenizer(text)

        for i, token in enumerate(tokens):
            if len(token) <= 3:
                continue
            if token[-1] == "s" and token[-2] in {"'", "’"}:
                tokens[i] = token[:-2]

        return tokens

    @staticmethod
    def spacy_tokenizer(lang_id: str, text: str) -> list[str]:
        nlp = get_spacy_pipeline(lang_id)
        return [token.text for token in nlp(text) if not token.is_punct]

    @staticmethod
    def __get_tokenizer(lang_id: str) -> Tokenizer:

        # Chinese (zh): Logographic script with no word boundaries.
        # Japanese (ja): Mixes kanji, hiragana, and katakana without spaces.
        # Thai/Lao/Khmer (th/lo/km): Abugida scripts with no spaces between words.
        # Burmese (my): Script runs continuously without spaces.
        # Tibetan (bo): No word separation in traditional texts.
        non_whitespace_tokenize_langs = {'zh', 'ja', 'th', 'lo', 'km', 'my', 'bo'}

        if lang_id in non_whitespace_tokenize_langs:
            return partial(TextProcessing.spacy_tokenizer, lang_id)

        if lang_id in {'en', 'nl', 'af'}:
            return TextProcessing.default_tokenizer_removing_possessives

        return TextProcessing.default_tokenizer

    @staticmethod
    def get_word_tokens_from_text(text: str, lang_id: str, filter_words: bool) -> list[WordToken]:

        if filter_words:
            is_acceptable_word = TextProcessing.get_word_accepter(lang_id)
        else:
            is_acceptable_word: Callable[[str], bool] = lambda _: True
        tokenizer = TextProcessing.__get_tokenizer(lang_id)

        word_tokens = (TextProcessing.create_word_token(token, lang_id) for token in tokenizer(text))
        accepted_word_tokens = [token for token in word_tokens if is_acceptable_word(token)]
        return accepted_word_tokens

class LmResponse:
    def __init__(self, response_content: str, prompt: str, model: str, lang_id: str, time_taken: float):
        self.response_content = response_content.strip()
        self.prompt = prompt
        self.model = model
        self.lang_id = lang_id
        self.time_taken = time_taken

    @staticmethod
    def remove_think_content(content: str) -> str:
        if "<think>" in content and "</think>" in content:
            content = content[content.index("</think>")+len("</think>"):].strip()
        return content

    def content_from_tag(self, tag_name: str) -> Optional[str]:
        tag_name = tag_name.strip('<>/')
        content = self.remove_think_content(self.response_content)
        if tag_name == "body" and "<body>" in content and not "</body>" in content:
            content = content + "</body>"
        match = re.search(r"<{}>(.*?)</{}>".format(tag_name, tag_name), content, re.DOTALL | re.IGNORECASE)
        if not match:
            return None
        return match.group(1).strip()

    def content_from_tags(self, tag_name: str) -> Optional[list[str]]:
        tag_name = tag_name.strip('<>/')
        content = self.remove_think_content(self.response_content)
        matches = re.findall(r"<{}>(.*?)</{}>".format(tag_name, tag_name), content, re.DOTALL | re.IGNORECASE)
        if not matches:
            return None
        return [match.strip() for match in matches]

    def content_from_tag_or_empty(self, tag_name: str) -> str:
        tag_content = self.content_from_tag(tag_name)
        return tag_content if tag_content else ""

    @cache
    def word_tokens_from_content(self) -> list[WordToken]:
        content = TextProcessing.get_plain_text(self.response_content)
        return TextProcessing.get_word_tokens_from_text(content, self.lang_id, filter_words=False)

    @cache
    def num_words_in_content(self) -> int:
        return len(self.word_tokens_from_content())

    def get_num_words_per_second(self) -> float:
        if self.response_content == "":
            return 0
        return self.num_words_in_content() / self.time_taken


class StoryTitles:

    min_num_words_title = 4
    max_num_words_title = 40
    max_length_title = 100
    prefix_num_words = 2

    def __init__(self, lang_id: str, titles_dir: str):
        if not os.path.exists(titles_dir):
            os.makedirs(titles_dir)
        self.file_name = "titles_{}.txt".format(lang_id)
        self.file_path = os.path.join(titles_dir, self.file_name)
        self.lang_id = lang_id
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                self.titles = [title for title in self.unique_titles(f)]

        except FileNotFoundError:
            self.titles = []

    def unique_titles(self, titles: Iterable[str]) -> Generator[str, None, None]:
        unique_prefixes = set()
        for title in titles:
            title = title.strip()
            if len(title) > self.max_length_title:
                print("Title '{}' is too long.".format(title))
                continue
            title_tokens = TextProcessing.get_word_tokens_from_text(title, self.lang_id, filter_words=False)
            if len(title_tokens) < self.min_num_words_title:
                print("Title '{}' has too few words.".format(title))
                continue
            if len(title_tokens) > self.max_num_words_title:
                print("Title '{}' has too many words.".format(title))
                continue
            title_prefix = self.prefix_from_title(title, title_tokens)
            if not title_prefix:
                print("Title '{}' has no valid prefix.".format(title))
                continue
            if title_prefix in unique_prefixes:
                print("Title '{}' has a duplicate prefix.".format(title))
                continue
            yield title
            unique_prefixes.add(title_prefix)


    def prefix_from_title(self, title: str, title_tokens: Optional[list[WordToken]] = None) -> Optional[str]:
        if title_tokens == None:
            title_tokens = TextProcessing.get_word_tokens_from_text(title, self.lang_id, filter_words=False)
        if len(title_tokens) < self.prefix_num_words:
            print("Title '{}' has too few tokens for prefix.".format(title))
            return None
        return " ".join(title_tokens[0:self.prefix_num_words])

    def get_new_title(self) -> Optional[str]:
        if not self.titles:
            return None
        title = self.titles.pop(0)
        self.save()
        return title

    def save(self) -> None:
        with open(self.file_path, 'w', encoding="utf-8") as f:
            for title in self.unique_titles(self.titles):
                f.write(f"{title}\n")

def num_text_files_in_dir(dir_path: str) -> int:
    files_in_dir = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
    text_files_in_dir = [file for file in files_in_dir if file.endswith(".txt")]
    return len(text_files_in_dir)

def num_lines_in_file(file_path: str) -> int:
    with open(file_path, 'r', encoding="utf-8") as f:
        return sum(1 for _ in f)

    "af": "Afrikaans",
    "ak": "Akan",
    "am": "Amharic",
    "an": "Aragonese",
    "ar": "Arabic",
    "as": "Assamese",
    #"av": "Avaric",
    "ay": "Aymara",
    "az": "Azerbaijani",
    "ba": "Bashkir",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bh": "Bihari",
    #"bi": "Bislama",
    "bm": "Bambara",
    "bn": "Bengali",
    "bo": "Tibetan",
    "br": "Breton",
    "bs": "Bosnian",
    "ca": "Catalan",
    "ce": "Chechen",
    "ch": "Chamorro",
    "co": "Corsican",
    "cr": "Cree",
    "cs": "Czech",
    "cu": "Old Church Slavonic",
    "cv": "Chuvash",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    #"dv": "Divehi",
    #"dz": "Dzongkha",
    "ee": "Ewe",
    "el": "Greek (Modern)",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "ff": "Fula",
    "fi": "Finnish",
    "fj": "Fijian",
    #"fo": "Faroese",
    "fr": "French",
    "fy": "Western Frisian",
    "ga": "Irish",
    "gd": "Scottish Gaelic",
    "gl": "Galician",
    "gn": "Guarani",
    "gu": "Gujarati",
    "gv": "Manx",
    "ha": "Hausa",
    "he": "Hebrew",
    "hi": "Hindi",
    #"ho": "Hiri Motu",
    "hr": "Croatian",
    "ht": "Haitian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "hz": "Herero",
    "ia": "Interlingua",
    "id": "Indonesian",
    #"ie": "Interlingue",
    "ig": "Igbo",
    "ii": "Sichuan Yi",
    "ik": "Inupiaq",
    "io": "Ido",
    "is": "Icelandic",
    "it": "Italian",
    "iu": "Inuktitut",
    "ja": "Japanese",
    "jv": "Javanese",
    "ka": "Georgian",
    "kg": "Kongo",
    "ki": "Kikuyu",
    #"kj": "Kwanyama",
    "kk": "Kazakh",
    #"kl": "Kalaallisut",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    #"kr": "Kanuri",
    "ks": "Kashmiri",
    "ku": "Kurdish",
    "kv": "Komi",
    "kw": "Cornish",
    "ky": "Kyrgyz",
    "la": "Latin",
    #"lb": "Luxembourgish",
    "lg": "Ganda",
    #"li": "Limburgish",
    #"ln": "Lingala",
    "lo": "Lao",
    "lt": "Lithuanian",
    #"lu": "Luba-Katanga",
    "lv": "Latvian",
    "mg": "Malagasy",
    "mh": "Marshallese",
    "mi": "Maori",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "mt": "Maltese",
    "my": "Burmese",
    "na": "Nauru",
    #"nb": "Norwegian Bokmål",
    #"nd": "Northern Ndebele",
    "ne": "Nepali",
    #"ng": "Ndonga",
    "nl": "Dutch",
    "nn": "Norwegian Nynorsk",
    "no": "Norwegian",
    #"nr": "Southern Ndebele",
    "nv": "Navajo",
    #"ny": "Chichewa",
    #"oc": "Occitan",
    #"oj": "Ojibwe",
    #"om": "Oromo",
    "or": "Oriya",
    #"os": "Ossetian",
    "pa": "Punjabi",
    "pi": "Pali",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "qu": "Quechua",
    "rm": "Romansh",
    #"rn": "Kirundi",
    "ro": "Romanian",
    "ru": "Russian",
    #"rw": "Kinyarwanda",
    "sa": "Sanskrit",
    "sc": "Sardinian",
    "sd": "Sindhi",
    #"se": "Northern Sami",
    #"sg": "Sango",
    #"si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sm": "Samoan",
    #"sn": "Shona",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    #"ss": "Swati",
    #"st": "Southern Sotho",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "tg": "Tajik",
    "th": "Thai",
    "ti": "Tigrinya",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tn": "Tswana",
    "to": "Tonga",
    "tr": "Turkish",
    #"ts": "Tsonga",
    "tt": "Tatar",
    "tw": "Twi",
    "ty": "Tahitian",
    "ug": "Uighur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    #"ve": "Venda",
    "vi": "Vietnamese",
    #"vo": "Volapük",
    "wa": "Walloon",
    "wo": "Wolof",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    #"za": "Zhuang",
    "zh": "Chinese",
    "zu": "Zulu"
}

