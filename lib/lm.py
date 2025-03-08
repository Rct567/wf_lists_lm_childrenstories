from dataclasses import dataclass
from functools import cache
import os
import re
import sys
import time
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

from lib.text_processing import TextProcessing, WordToken


lm_caller_num_calls = 0
lm_caller_num_errors = 0


@dataclass
class LM():
    model: str
    api_base: str
    api_key: str
    temperature: float
    frequency_penalty: float
    presence_penalty: float

    def __post_init__(self):
        assert self.temperature >= 0 and self.temperature <= 2
        assert self.frequency_penalty >= -2 and self.frequency_penalty <= 2
        assert self.presence_penalty >= -2 and self.presence_penalty <= 2


# named tuple for LM


load_dotenv()

def get_defined_lms() -> list[LM]:

    # read .env file and create list of LMs
    lms = []
    current_index = 0
    num_not_found = 0

    while True:
        try:

            temperature = os.getenv("LM{}_TEMPERATURE".format(current_index))
            if temperature:
                temperature = float(temperature)
            else:
                temperature = 1.5

            current_lm = LM(
                model=os.environ["LM{}_MODEL".format(current_index)],
                api_base=os.environ["LM{}_OPENAI_API_BASE".format(current_index)],
                api_key=os.environ["LM{}_OPENAI_API_KEY".format(current_index)],
                temperature=temperature,
                frequency_penalty=0.01,
                presence_penalty=0.01
            )

            lms.append(current_lm)
        except KeyError:
            num_not_found += 1
            if num_not_found > 10:
                break
            else:
                continue
        finally:
            current_index += 1

    return lms

def get_selected_lm() -> LM:

    available_lms = get_defined_lms()

    if not available_lms:
        raise Exception("No LMs defined in .env file.")

    print("Available LMs:")
    for index, lm in enumerate(available_lms):
        print(" {}: {} ({})".format(index, lm.model, lm.api_base.split("://")[1]))
    while True:
        try:
            selected_lm_index = int(input("Select a LM: "))
            if selected_lm_index < 0 or selected_lm_index >= len(available_lms):
                print("Invalid index.")
                continue
            selected_lm = available_lms[selected_lm_index]
            break
        except ValueError:
            print("Invalid index.")
            continue

    print("Selected LM: {} ({})".format(selected_lm.model, selected_lm.api_base.split("://")[1]))
    print("Temperature: {}".format(selected_lm.temperature))

    return selected_lm

def get_lm_caller(lm: LM):

    client = OpenAI(base_url=lm.api_base, api_key=lm.api_key)

    if "Mistral" in lm.model:
        model_role = "assistant"
    else:
        model_role = "system"

    def call_lm(prompt_text: str, lang_id: str) -> Optional[LmResponse]:
        global lm_caller_num_calls, lm_caller_num_errors

        if lm_caller_num_errors > 3:
            print("Too many errors for {} ({}). Exiting.".format(lm.model, lm.api_base.split("://")[1]))
            sys.exit(1)

        messages = [
            {"role": model_role, "content": "You are a creative children's story writer."},
            {"role": "user", "content": prompt_text}
        ]

        lm_caller_num_calls += 1
        start_time = time.perf_counter()
        response = client.chat.completions.create(
            model=lm.model,
            messages=messages, # type: ignore
            temperature=lm.temperature,
            #frequency_penalty=frequency_penalty,
            #presence_penalty=lm.presence_penalty
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
        return LmResponse(response_content, prompt_text, lm.model, lang_id, time_taken)

    return call_lm

class LmResponse:
    def __init__(self, response_content: str, prompt: str, model: str, lang_id: str, time_taken: float):
        self.response_content = response_content.strip()
        self.prompt = prompt
        self.model = model
        self.lang_id = lang_id
        self.time_taken = time_taken

    @staticmethod
    def __remove_think_content(content: str) -> str:
        if "<think>" in content and "</think>" in content:
            content = content[content.index("</think>")+len("</think>"):].strip()
        return content

    def content_from_tag(self, tag_name: str) -> Optional[str]:
        tag_name = tag_name.strip('<>/')
        content = self.__remove_think_content(self.response_content)
        if tag_name == "body" and "<body>" in content and not "</body>" in content:
            content = content + "</body>"
        match = re.search(r"<{}>(.*?)</{}>".format(tag_name, tag_name), content, re.DOTALL | re.IGNORECASE)
        if not match:
            return None
        return match.group(1).strip()

    def content_from_tags(self, tag_name: str) -> Optional[list[str]]:
        tag_name = tag_name.strip('<>/')
        content = self.__remove_think_content(self.response_content)
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