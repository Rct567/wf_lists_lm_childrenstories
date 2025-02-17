from functools import cache
import re
import sys
import time
from typing import Optional
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
        global lm_caller_num_errors

        if lm_caller_num_errors > 5:
            print("Too many errors. Exiting.")
            sys.exit(1)

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
            #frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        if not response.choices:
            lm_caller_num_errors += 1
            print("No choices in response?")
            print(response)
            return None
        response_content = response.choices[0].message.content
        if not response_content:
            lm_caller_num_errors += 1
            print("No content in response?")
            print(response)
            return None
        time_taken = time.perf_counter() - start_time
        #print("\n===========================\n"+response_content+"\n===========================\n")
        return (response_content, prompt_text, model, lang_id, time_taken)

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