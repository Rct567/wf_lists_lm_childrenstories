from functools import cache, partial
import html
import os
import re
import sys
import time
from typing import Callable, Generator, Iterable, NewType, Optional
from openai import OpenAI

from lib.text_processing import TextProcessing, WordToken


lm_caller_num_errors = 0

def get_lm_caller(api_base: str, api_key: str, model: str, temperature: float, frequency_penalty: float, presence_penalty: float):

    client = OpenAI(base_url=api_base, api_key=api_key)

    if "Mistral" in model:
        model_role = "assistant"
    else:
        model_role = "system"

    def call_local_lm(prompt_text: str, lang_id: str) -> Optional[tuple[str, str, str, str, float]]:
        messages = [
            {"role": model_role, "content": "You are a creative children's story writer."},
            {"role": "user", "content": prompt_text}
        ]
        assert temperature > 0 and temperature <= 2
        assert frequency_penalty > -2 and frequency_penalty <= 2
        assert presence_penalty > -2 and presence_penalty <= 2
        #try:
        start_time = time.perf_counter()
        response = client.chat.completions.create(
            model=model,
            messages=messages, # type: ignore
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        if not response.choices:
            print("No choices in response?")
            print(response)
            return None
        response_content = response.choices[0].message.content
        if not response_content:
            return None
        time_taken = time.perf_counter() - start_time
        #print("\n===========================\n"+response_content+"\n===========================\n")
        return (response_content, prompt_text, model, lang_id, time_taken)

        # except Exception as error:
        #     global lm_caller_num_errors
        #     lm_caller_num_errors += 1
        #     print("Error while getting response from LM: {}".format(error))
        #     if lm_caller_num_errors > 10:
        #         print("Too many errors. Exiting.")
        #         sys.exit(1)
        #     return None

    return call_local_lm

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
                print(title_tokens)
                print("Title '{}' has too few words ({}).".format(title, len(title_tokens)))
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

    @staticmethod
    def title_is_acceptable(title: str, lang_id: str) -> bool:
        if any(char in title for char in "{}[]<>@#$%^*+"):
            print("Title '{}' contains invalid characters.".format(title))
            return False
        word_accepter = TextProcessing.get_word_accepter(lang_id)
        for word in TextProcessing.get_word_tokens_from_text(title, lang_id, filter_words=False):
            if not word_accepter(word):
                print("Title '{}' contains invalid word '{}' for language '{}'.".format(title, word, lang_id))
                return False
        return True

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
                if not StoryTitles.title_is_acceptable(title, self.lang_id):
                    print("Title '{}' is not acceptable.".format(title))
                    continue
                f.write(f"{title}\n")