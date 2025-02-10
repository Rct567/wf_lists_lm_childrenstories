

import re
import time
from typing import Callable, Optional
from openai import OpenAI

def get_lm_caller(LM_STUDIO_API_BASE: str, LM_STUDIO_API_KEY: str, MODEL: str, LM_TEMPERATURE: float, LM_TOP_P: float):

    client = OpenAI(base_url=LM_STUDIO_API_BASE, api_key=LM_STUDIO_API_KEY)

    def call_local_lm(prompt_text: str, lang_id: str) -> Optional[tuple[str, str, str, str, float]]:
        messages = [
            {"role": "system", "content": "You are a creative children's story writer."},
            {"role": "user", "content": prompt_text}
        ]
        try:
            start_time = time.perf_counter()
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages, # type: ignore
                temperature=LM_TEMPERATURE,
                top_p=LM_TOP_P
            )
            response_content = response.choices[0].message.content
            if not response_content:
                return None
            time_taken = time.perf_counter() - start_time
            return (response_content, prompt_text, MODEL, lang_id, time_taken)

        except Exception as error:
            print("Error while generating story: {}".format(error))
            return None

    return call_local_lm

class LmResponse:
    def __init__(self, response_content: str, prompt: str, model: str, lang_id: str, time_taken: float):
        self.response_content = response_content.strip()
        self.prompt = prompt
        self.model = model
        self.lang_id = lang_id
        self.time_taken = time_taken

    def content_from_tag(self, tag_name: str) -> Optional[str]:
        tag_name = tag_name.strip('<>/')
        content = self.response_content
        if tag_name == "body" and "<body>" in content and not "</body>" in content:
            content = content + "</body>"
        content_match = re.search(r"<{}>(.*?)</{}>".format(tag_name, tag_name), content, re.DOTALL | re.IGNORECASE)
        if not content_match:
            return None
        return content_match.group(1).strip()

    def content_from_tags(self, tag_name: str) -> Optional[list[str]]:
        tag_name = tag_name.strip('<>/')
        matches = re.findall(r"<{}>(.*?)</{}>".format(tag_name, tag_name), self.response_content, re.DOTALL | re.IGNORECASE)
        return [match.strip() for match in matches] if matches else []


    def content_from_tag_or_empty(self, tag_name: str) -> str:
        tag_content = self.content_from_tag(tag_name)
        return tag_content if tag_content else ""

    def get_words_from_content(self) -> list[str]:
        return [word.strip() for word in self.response_content.split() if word.strip() != ""]

    def get_num_words_per_second(self) -> float:
        if self.response_content == "":
            return 0
        return len(self.get_words_from_content()) / self.time_taken

