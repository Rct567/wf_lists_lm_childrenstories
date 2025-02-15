

from functools import partial
import html
import re
from typing import Callable, Generator, Iterable, NewType, Optional


import spacy
from spacy.tokens import Doc
from spacy.language import Language

loaded_spacy: dict[str, Language] = {}

def get_spacy_pipeline(lang_code: str) -> Language:

    global loaded_spacy

    if lang_code in loaded_spacy:
        return loaded_spacy[lang_code]

    if lang_code == "zh": # Chinese
        import jieba
        jieba.setLogLevel(20)
        cfg = {"segmenter": "jieba"}
        nlp = spacy.blank(lang_code).from_config(
            {"nlp": {"tokenizer": cfg}}
        )
    elif lang_code == 'ja': # Japanese

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
        nlp.tokenizer = MecabTokenizer(nlp)
    elif lang_code == "th": # Thai
        from pythainlp.tokenize import word_tokenize as thai_word_tokenize
        def custom_thai_tokenizer(text: str) -> Doc:
            nonlocal nlp
            tokens: list[str] = thai_word_tokenize(text)
            return Doc(nlp.vocab, words=tokens)
        nlp = spacy.blank('xx')
        nlp.tokenizer = custom_thai_tokenizer
    elif lang_code == "km": # Khmer
        from khmernltk.word_tokenize import word_tokenize as khmer_tokenizer
        def custom_khmer_tokenizer(text: str) -> Doc:
            nonlocal nlp
            tokens: list[str] = [str(token) for token in khmer_tokenizer(text)]
            return Doc(nlp.vocab, words=tokens)
        nlp = spacy.blank('xx')
        nlp.tokenizer = custom_khmer_tokenizer
    elif lang_code == "lo": # Lao
        from laonlp.tokenize import word_tokenize as lao_tokenizer
        def custom_lao_tokenizer(text: str) -> Doc:
            nonlocal nlp
            tokens: list[str] = [str(token) for token in lao_tokenizer(text)]
            return Doc(nlp.vocab, words=tokens)
        nlp = spacy.blank('xx')
        nlp.tokenizer = custom_lao_tokenizer
    elif lang_code == "bo": # Tibetan
        from botok import WordTokenizer # type: ignore
        from botok.config import Config
        from pathlib import Path
        config = Config(dialect_name="general", base_path= Path.home())
        wt = WordTokenizer(config=config)
        def custom_lao_tokenizer(text: str) -> Doc:
            nonlocal nlp, wt
            text = text.replace("\t", " ")
            try:
                tokens: list[str] = [str(token.text) for token in  wt.tokenize(text, split_affixes=False) if token.chunk_type == "TEXT"]
            except Exception as e:
                print(e)
                tokens = []
            return Doc(nlp.vocab, words=tokens)
        nlp = spacy.blank('xx')
        nlp.tokenizer = custom_lao_tokenizer
    else:
        raise Exception("Should Spacy be used for {}?".format(lang_code))
        #nlp = spacy.blank(lang_code)

    loaded_spacy[lang_code] = nlp
    return nlp


WordToken = NewType('WordToken', str)
Tokenizer = Callable[[str], list[str]]

class TextProcessing:

    CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]{1,}', re.UNICODE)
    JAPANESE_PATTERN = re.compile(
        r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf\uf900-\ufaff\u3400-\u4dbf]{1,}',
        re.UNICODE
    )
    KOREAN_PATTERN = re.compile(r'[\uac00-\ud7a3]{1,}', re.UNICODE)
    ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF]{1,}', re.UNICODE)
    ETHIOPIC_PATTERN = re.compile(r'[\u1200-\u137F]{1,}', re.UNICODE)
    THAI_PATTERN = re.compile(r'[\u0e00-\u0e7f]{1,}', re.UNICODE)
    LAO_PATTERN = re.compile(r'[\u0e80-\u0eff]{1,}', re.UNICODE)
    KHMER_PATTERN = re.compile(r'[\u1780-\u17ff]{1,}', re.UNICODE)
    CYRILLIC_PATTERN = re.compile(
        r'[\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u1C80-\u1C8F]{1,}',
        re.UNICODE
    )
    HEBREW_PATTERN = re.compile(r'[\u0590-\u05FF]{1,}', re.UNICODE)
    GREEK_PATTERN = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]{1,}', re.UNICODE)
    INDIC_PATTERN = re.compile(r'[\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF\u0B00-\u0B7F\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F]{1,}', re.UNICODE)
    MYANMAR_PATTERN = re.compile(r'[\u1000-\u109F]{1,}', re.UNICODE)
    TIBETAN_PATTERN = re.compile(r'[\u0F00-\u0FFF]{1,}', re.UNICODE)
    GEORGIAN_PATTERN = re.compile(r'[\u10A0-\u10FF\u2D00-\u2D2F]{1,}', re.UNICODE)
    ARMENIAN_PATTERN = re.compile(r'[\u0530-\u058F]{1,}', re.UNICODE)
    DEFAULT_PATTERN = re.compile(r'\S{1,}', re.UNICODE)

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
        elif lang_id is not None and lang_id in {'am', 'ti'}:
            word_pattern = TextProcessing.ETHIOPIC_PATTERN
        elif lang_id == 'th':
            word_pattern = TextProcessing.THAI_PATTERN
        elif lang_id == 'lo':
            word_pattern = TextProcessing.LAO_PATTERN
        elif lang_id == 'km':
            word_pattern = TextProcessing.KHMER_PATTERN
        elif lang_id in {'be', 'ru', 'uk', 'bg'}:
            word_pattern = TextProcessing.CYRILLIC_PATTERN
        elif lang_id in {'he', 'yi'}:
            word_pattern = TextProcessing.HEBREW_PATTERN
        elif lang_id == 'el':
            word_pattern = TextProcessing.GREEK_PATTERN
        elif lang_id in {'hi', 'mr', 'ne', 'bn', 'pa', 'gu', 'or', 'ta', 'te', 'kn', 'ml'}:
            word_pattern = TextProcessing.INDIC_PATTERN
        elif lang_id == 'my':
            word_pattern = TextProcessing.MYANMAR_PATTERN
        elif lang_id == 'bo':
            word_pattern = TextProcessing.TIBETAN_PATTERN
        elif lang_id == 'ka':
            word_pattern = TextProcessing.GEORGIAN_PATTERN
        elif lang_id == 'hy':
            word_pattern = TextProcessing.ARMENIAN_PATTERN
        else:
            word_pattern = TextProcessing.DEFAULT_PATTERN

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

        word_tokens = (TextProcessing.create_word_token(token, lang_id) for token in tokenizer(text) if token)
        accepted_word_tokens = [token for token in word_tokens if is_acceptable_word(token)]
        return accepted_word_tokens