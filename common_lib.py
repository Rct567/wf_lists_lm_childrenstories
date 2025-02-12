

from functools import cache
import html
import re
import time
from typing import Callable, NewType, Optional
from openai import OpenAI

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
            print("\n====================\n"+response_content+"\n===========================\n")
            return (response_content, prompt_text, model, lang_id, time_taken)

        except Exception as error:
            print("Error while generating story: {}".format(error))
            return None

    return call_local_lm


WordToken = NewType('WordToken', str)
Tokenizer = Callable[[str], list[str]]

class TextProcessing:

    CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]{1,}', re.UNICODE)
    JAPANESE_PATTERN = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf\uf900-\ufaff\u3400-\u4dbf]{1,}', re.UNICODE)
    KOREAN_PATTERN = re.compile(r'[\uac00-\ud7a3]{1,}', re.UNICODE)
    ARABIC_PATTERN = re.compile(r'[\u0600-\u06FF]{1,}', re.UNICODE)
    ETHIOPIC_PATTERN = re.compile(r'[\u1200-\u137F]{1,}', re.UNICODE)
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
    def get_tokenizer(lang_id: str) -> Tokenizer:

        if lang_id in {'en', 'nl', 'af'}:
            return TextProcessing.default_tokenizer_removing_possessives

        return TextProcessing.default_tokenizer

    @staticmethod
    def get_word_tokens_from_text(text: str, lang_id: str, filter_words: bool) -> list[WordToken]:

        if filter_words:
            is_acceptable_word = TextProcessing.get_word_accepter(lang_id)
        else:
            is_acceptable_word: Callable[[str], bool] = lambda _: True
        tokenizer = TextProcessing.get_tokenizer(lang_id)

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

    min_title_length = 20
    prefix_length = 28

    def __init__(self, lang_id: str):
        self.file_name = "titles_{}.txt".format(lang_id)
        try:
            with open(self.file_name, 'r', encoding="utf-8") as f:
                self.titles = [line.strip() for line in f if len(line.strip()) > self.min_title_length]
                self.unique_prefixes = set(self.prefix_from_title(title) for title in self.titles)
        except FileNotFoundError:
            self.titles = []

    def prefix_from_title(self, word: str) -> str:
        return word[:self.prefix_length].lower()

    def add_title(self, title: str) -> None:
        title_prefix = title[:self.prefix_length].lower()
        if title_prefix in self.unique_prefixes:
            return
        if len(title) < self.min_title_length:
            return
        self.titles.append(title)
        self.unique_prefixes.add(self.prefix_from_title(title))
        self.save()

    def get_new_title(self) -> Optional[str]:
        if not self.titles:
            return None
        title = self.titles.pop(0)
        self.save()
        return title

    def save(self) -> None:
        with open(self.file_name, 'w', encoding="utf-8") as f:
            for t in self.titles:
                f.write(f"{t}\n")

