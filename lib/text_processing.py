

from functools import partial
import html
import re
from typing import Callable, Counter, NewType, Optional, Sequence, Union


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
        import MeCab
        def custom_japanese_tokenizer(text: str) -> Doc:
            nonlocal nlp
            tagger = MeCab.Tagger("-Owakati")
            tokens = tagger.parse(text).strip().split()
            return Doc(nlp.vocab, words=tokens)
        nlp = spacy.blank('xx')
        nlp.tokenizer = custom_japanese_tokenizer
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
            text = text.replace("\t", " ")
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

    LANGUAGES_USING_APOSTROPHE = {
        'en',  # English (e.g., contractions like "don't")
        'fr',  # French (e.g., "l'heure")
        'it',  # Italian (e.g., "un'altra")
        'ga',  # Irish (Gaeilge, e.g., "O'Connell")
        'pt',  # Portuguese (e.g., poetic contractions)
        'de',  # German (e.g., genitive case in older texts)
        'nl',  # Dutch (e.g., shortened forms like "'s ochtends")
        'sv',  # Swedish (e.g., possessive forms like "Anna's")
        'fi',  # Finnish (e.g., loanwords like "taxi’t")
        'mt',  # Maltese (apostrophe in words like "qalb’i")
        'ca',  # Catalan (e.g., "l’àvia")
        'oc',  # Occitan (e.g., "l’aiga")
        'br',  # Breton
        'sw',  # Swahili (e.g., Ng'ombe)
        'tr',  # Turkish (e.g., İstanbul’a)
        'cy',  # Welsh (e.g., i’r)
        'gd',  # Scottish Gaelic (e.g., tha ’n)
        'gv',  # Manx (e.g., yn ’eddin)
        'mi',  # Māori (e.g., tā’onga)
        'nv',  # Navajo (e.g., łéʼéjí)
        'ku',  # Kurdish (e.g., k’u in Latin script)
        'az',  # Azerbaijani (e.g., Bakı’da)
        'uz',  # Uzbek (e.g., so’z)
        'ht',  # Haitian Creole (e.g., "pa'm" for "pou mwen")
        'nn',   # Norwegian Nynorsk (e.g., "kor'leis")
        'co',  # Corsican (e.g., "l'acqua")
        'gl',  # Galician (e.g., "n'a casa")
        'lb',  # Luxembourgish (e.g., "d'Stad")
        'qu',  # Quechua (e.g., "p'unchaw")
        'sc',  # Sardinian (e.g., "s'arti")
        'wa',   # Walloon (similar to French)
    }

    CHINESE_PATTERN = re.compile(r'^[\u4e00-\u9fff]+$', re.UNICODE)
    JAPANESE_PATTERN = re.compile(r'^[\u3040-\u309F\u4E00-\u9FAF\uF900-\uFAFF\u3400-\u4DBF]+$', re.UNICODE)  # Kanji + Hiragana only
    JAPANESE_ALL_PATTERN = re.compile(
        r'^[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf\uf900-\ufaff\u3400-\u4dbf]+$',
        re.UNICODE
    )  # Kanji + Hiragana + Katakana
    JAPANESE_KATAKANA_PATTERN = re.compile(r'^[\u30A0-\u30FF]+$', re.UNICODE)  # Katakana only
    KOREAN_PATTERN = re.compile(r'^[\uac00-\ud7a3]+$', re.UNICODE)
    ARABIC_PATTERN = re.compile(r'^[\u0600-\u06FF]+$', re.UNICODE)
    URDU_PATTERN = re.compile(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+$', re.UNICODE)
    SINHALA_PATTERN = re.compile(r'^[\u0D80-\u0DFF]+$', re.UNICODE)
    ETHIOPIC_PATTERN = re.compile(r'^[\u1200-\u137F]+$', re.UNICODE)
    THAI_PATTERN = re.compile(r'^[\u0e00-\u0e7f]+$', re.UNICODE)
    LAO_PATTERN = re.compile(r'^[\u0e80-\u0eff]+$', re.UNICODE)
    KHMER_PATTERN = re.compile(r'^[\u1780-\u17ff]+$', re.UNICODE)
    CYRILLIC_PATTERN = re.compile(
        r'^[\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u1C80-\u1C8F]+$',
        re.UNICODE
    )
    OLD_CHURCH_SLAVONIC_PATTERN = re.compile(r'^[\u0400-\u04FF\u0500-\u052F\u2C00-\u2C5F\uA640-\uA69F]+$', re.UNICODE)
    HEBREW_PATTERN = re.compile(r'^[\u0590-\u05FF]+$', re.UNICODE)
    GREEK_PATTERN = re.compile(r'^[\u0370-\u03FF\u1F00-\u1FFF]+$', re.UNICODE)
    INDIC_PATTERN = re.compile(
        r'^[\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF\u0B00-\u0B7F\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F]+$',
        re.UNICODE
    )
    MYANMAR_PATTERN = re.compile(r'^[\u1000-\u109F]+$', re.UNICODE)
    TIBETAN_PATTERN = re.compile(r'^[\u0F00-\u0FFF]+$', re.UNICODE)
    MONGOLIAN_PATTERN = re.compile(r'^[\u1800-\u18AF\u0400-\u04FF]+$', re.UNICODE)  # Mongolian script + Cyrillic
    GEORGIAN_PATTERN = re.compile(r'^[\u10A0-\u10FF\u2D00-\u2D2F]+$', re.UNICODE)
    ARMENIAN_PATTERN = re.compile(r'^[\u0530-\u058F]+$', re.UNICODE)
    SERBIAN_PATTERN = re.compile(r'^[\u0400-\u045F\u0490\u0491A-Za-zČĆĐŠŽčćđšž]+$', re.UNICODE)  # Serbian Cyrillic + Serbian Latin
    CROATIAN_BOSNIAN_PATTERN = re.compile(r'^[A-Za-zČĆĐŠŽčćđšž]+$', re.UNICODE)
    SLOVAK_PATTERN = re.compile(r'^[A-Za-zÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽáäčďéíĺľňóôŕšťúýž]+$', re.UNICODE)
    SLOVENIAN_PATTERN = re.compile(r'^[A-Za-zČŠŽčšž]+$', re.UNICODE)
    VIETNAMESE_PATTERN = re.compile(r'^[A-Za-z\u00C0-\u1EF9]+$', re.UNICODE)
    INDONESIAN_PATTERN = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+$', re.UNICODE)
    TURKISH_PATTERN = re.compile(r'^[A-Za-zÇĞİÖŞÜçğıöşü]+$', re.UNICODE)
    HUNGARIAN_PATTERN = re.compile(r'^[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]+$', re.UNICODE)
    POLISH_PATTERN = re.compile(r'^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+$', re.UNICODE)
    CZECH_PATTERN = re.compile(r'^[A-Za-zÁČĎÉĚÍŇÓŘŠŤÚŮÝŽáčďéěíňóřšťúůýž]+$', re.UNICODE)
    LATIN1_PATTERN = re.compile(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+$', re.UNICODE)
    LATIN_EXTENDED_PATTERN = re.compile(r'^[A-Za-z\xC0-\xFF\u0100-\u017F\u0180-\u024F]+$', re.UNICODE)
    BASIC_LATIN_PATTERN = re.compile(r'^[A-Za-z]+$', re.UNICODE)
    DEFAULT_PATTERN = re.compile(r'^\S+$', re.UNICODE)  # Any non-whitespace character

    @staticmethod
    def get_word_accepter(lang_id: Optional[str]) -> Callable[[str], bool]:
        min_length = 1
        if lang_id == 'zh':
            word_pattern = TextProcessing.CHINESE_PATTERN
        elif lang_id == 'ja':
            word_pattern = TextProcessing.JAPANESE_PATTERN
        elif lang_id == 'ja_katakana':
            word_pattern = TextProcessing.JAPANESE_KATAKANA_PATTERN
        elif lang_id == 'ja_all':
            word_pattern = TextProcessing.JAPANESE_ALL_PATTERN
        elif lang_id == 'ko':
            word_pattern = TextProcessing.KOREAN_PATTERN
        elif lang_id == 'bo':
            word_pattern = TextProcessing.TIBETAN_PATTERN
        elif lang_id == 'th':
            word_pattern = TextProcessing.THAI_PATTERN
        elif lang_id == 'lo':
            word_pattern = TextProcessing.LAO_PATTERN
        elif lang_id == 'km':
            word_pattern = TextProcessing.KHMER_PATTERN
        elif lang_id == 'vi':
            word_pattern = TextProcessing.VIETNAMESE_PATTERN
        elif lang_id == 'ar':
            word_pattern = TextProcessing.ARABIC_PATTERN
        elif lang_id in {'ur', 'fa', 'sd', 'ug'}: # Urdu, Persian, Sindhi, Uyghur
            word_pattern = TextProcessing.URDU_PATTERN # extended Arabic ranges
        elif lang_id == 'si':
            word_pattern = TextProcessing.SINHALA_PATTERN
        elif lang_id is not None and lang_id in {'am', 'ti'}: # Amharic, Tigrinya
            word_pattern = TextProcessing.ETHIOPIC_PATTERN
        elif lang_id == 'mn':
            word_pattern = TextProcessing.MONGOLIAN_PATTERN
        elif lang_id in {'be', 'ru', 'uk', 'bg', 'ce', 'mk', 'tg', 'tt'}: # Belarusian, Russian, Ukrainian, Bulgarian, Chechen, Macedonian, Tajik, Tatar
            word_pattern = TextProcessing.CYRILLIC_PATTERN
        elif lang_id in {'hi', 'mr', 'ne', 'bn', 'pa', 'gu', 'or', 'ta', 'te', 'kn', 'ml'}:
            word_pattern = TextProcessing.INDIC_PATTERN
        elif lang_id == 'cu':
            word_pattern = TextProcessing.OLD_CHURCH_SLAVONIC_PATTERN
        elif lang_id == 'my':
            word_pattern = TextProcessing.MYANMAR_PATTERN
        elif lang_id in {'he', 'yi'}:
            word_pattern = TextProcessing.HEBREW_PATTERN
        elif lang_id == 'el':
            word_pattern = TextProcessing.GREEK_PATTERN
        elif lang_id == 'ka':
            word_pattern = TextProcessing.GEORGIAN_PATTERN
        elif lang_id == 'hy':
            word_pattern = TextProcessing.ARMENIAN_PATTERN
        elif lang_id == 'sr':
            word_pattern = TextProcessing.SERBIAN_PATTERN
        elif lang_id in {'hr', 'bs', 'me'}:  # Croatian, Bosnian, Montenegrin
            word_pattern = TextProcessing.CROATIAN_BOSNIAN_PATTERN
        elif lang_id == 'sk':
            word_pattern = TextProcessing.SLOVAK_PATTERN
        elif lang_id == 'id':
            word_pattern = TextProcessing.INDONESIAN_PATTERN
        elif lang_id == 'sl':
            word_pattern = TextProcessing.SLOVENIAN_PATTERN
        elif lang_id == 'tr':
            word_pattern = TextProcessing.TURKISH_PATTERN
        elif lang_id == 'hu':
            word_pattern = TextProcessing.HUNGARIAN_PATTERN
        elif lang_id == 'pl':
            word_pattern = TextProcessing.POLISH_PATTERN
        elif lang_id == 'cs':
            word_pattern = TextProcessing.CZECH_PATTERN
        elif lang_id in {'en', 'es', 'fr', 'de', 'nl', 'fy', 'it', 'pt', 'pt_br', 'da', 'sv', 'no', 'fi', 'is', 'ca', 'af', 'gd', 'ht', 'kg', 'rm', 'sq', 'uz', 'la', 'nn', 'jv', 'tl', 'su'}:
            word_pattern = TextProcessing.LATIN1_PATTERN
        elif lang_id in {'lv', 'lt', 'ro', 'et', 'mt', 'ga', 'cy', 'eu', 'br', 'lb', 'fo', 'kl', 'eo', 'gl'}:
            word_pattern = TextProcessing.LATIN_EXTENDED_PATTERN
        elif lang_id in {'sw', 'ms', 'mg', 'so', 'zu'}:
            word_pattern = TextProcessing.BASIC_LATIN_PATTERN
        else:
            raise Exception("Language '{}' not supported.".format(lang_id))
            word_pattern = TextProcessing.DEFAULT_PATTERN

        ignore_hyphen = True
        ignore_apostrophe = lang_id in TextProcessing.LANGUAGES_USING_APOSTROPHE

        def is_acceptable_word_for_lang(word: str) -> bool:
            stripped_word = word.strip("!@#$%^&*()_-=+{}:\"<>?,./;' ")
            stripped_word_len = len(stripped_word)
            if stripped_word_len < min_length or stripped_word_len > 300:
                return False
            if ignore_hyphen:
                stripped_word = stripped_word.replace("-", "")
            if ignore_apostrophe:
                stripped_word = stripped_word.replace("'", "").replace("’", "")

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

        return WordToken(TextProcessing.lowercase_string(token, lang_id))

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
        if text.strip() == "":
            return []
        nlp = get_spacy_pipeline(lang_id)
        return [token.text.strip() for token in nlp(text) if not token.is_punct and token.text.strip() != ""]

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

        plain_text = TextProcessing.get_plain_text(text)

        if filter_words:
            is_acceptable_word = TextProcessing.get_word_accepter(lang_id)
        else:
            is_acceptable_word: Callable[[str], bool] = lambda _: True
        tokenizer = TextProcessing.__get_tokenizer(lang_id)

        word_tokens = (TextProcessing.create_word_token(token, lang_id) for token in tokenizer(plain_text) if token.strip() != "")
        accepted_word_tokens = [token for token in word_tokens if token.strip() != "" and is_acceptable_word(token)]
        return accepted_word_tokens

    @staticmethod
    def get_word_token_rejection_rate(tokens: Sequence[WordToken], lang_id: str) -> float:

        word_accepter = TextProcessing.get_word_accepter(lang_id)
        num_accepted_words = 0
        num_rejected_words = 0
        for word in tokens:
            if word_accepter(word):
                num_accepted_words += 1
            else:
                num_rejected_words += 1

        if num_rejected_words == 0:
            return 0

        return num_rejected_words / (num_accepted_words + num_rejected_words)

    @staticmethod
    def has_repetitive_sentences(text: str, max_repeat_allowed: int = 3) -> bool:
        text = text.replace("<p>", "\n<p>").replace("</p>", "</p>\n")
        sentences = [p.strip() for p in re.split(r'\n{1,}|(?<=[.!?])\s+', text) if p.strip()]
        sentences_encountered: Counter[str] = Counter()
        for sentence in sentences:
            plain_sentence = TextProcessing.get_plain_text(sentence)
            if not plain_sentence:
                continue
            segment = plain_sentence[0:min(len(plain_sentence), 80)]
            if sentences_encountered[segment] > max_repeat_allowed:
                return True
            sentences_encountered[segment] += 1
        return False

    @staticmethod
    def has_non_letter_sequences(text: str, non_letters: str, min_length: int = 3) -> bool:
        if len(text) < min_length:
            return False
        non_letters_pattern = r'[{0}]'.format(re.escape(non_letters))+"{"+str(min_length)+",}"
        match_non_letter_sequence = re.search(non_letters_pattern, text, re.UNICODE)
        return match_non_letter_sequence is not None

    @staticmethod
    def num_lines_non_letter_sequence(text: str, non_letters: str, min_length: int = 3) -> int:
        num_none_letter_sequences = 0
        for line in text.split("\n"):
            if TextProcessing.has_non_letter_sequences(TextProcessing.get_plain_text(line), non_letters, min_length):
                num_none_letter_sequences += 1

        return num_none_letter_sequences

    @staticmethod
    def has_repeating_token_in_sequence(token_sequences: Sequence[WordToken], min_length: int = 3) -> bool:
        if not token_sequences:
            return False

        current_token = token_sequences[0]
        count = 1

        for token in token_sequences[1:]:
            if token == current_token:
                count += 1
                if count >= min_length:
                    return True
            else:
                current_token = token
                count = 1

        return False

    @staticmethod
    def lowercase_string(s: str, lang_id: str) -> str:
        if lang_id == 'ce': # Chechen
            # Lowercase the entire string first
            s_lowered = s.lower()
            # Replace Cyrillic letters followed by Latin 'i' with the corresponding Cyrillic lowercase and 'ӏ'
            cyrillic_pattern = r'([\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u1C80-\u1C8F])i'
            pattern = re.compile(cyrillic_pattern, re.UNICODE)
            s_replaced = pattern.sub(r'\1ӏ', s_lowered)
            return s_replaced
        elif lang_id == 'tr': # Turkish
            return s.replace('İ', 'i').replace('I', 'ı').lower()
        else:
            return s.lower()