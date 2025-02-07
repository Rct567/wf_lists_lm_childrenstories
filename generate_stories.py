from openai import OpenAI
import datetime
import os
import time
from typing import Any

LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "llama-3.2-3b-instruct-uncensored"
NUMBER_OF_STORIES = 3

client = OpenAI(base_url=LM_STUDIO_API_BASE, api_key=LM_STUDIO_API_KEY)

def build_story_prompt() -> str:
    return ("Please write a creative and original children's story that is at least 2000 words long. "
            "Ensure that the title of the story is enclosed in <title> tags and the body of the story is enclosed in <body> tags. "
            "Do not include any extra commentary or explanation; output only the story in the specified format.")

def call_local_lm(prompt_text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a creative children's story writer."},
        {"role": "user", "content": prompt_text}
    ]
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
        return response.choices[0].message.content.strip()
    except Exception as error:
        print("Error while generating story: {}".format(error))
        return ""

def generate_story() -> str:
    prompt_text = build_story_prompt()
    response = call_local_lm(prompt_text)
    return response


def save_story_to_file(story_content: str) -> None:
    filename = "{}.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
    try:
        with open(filename, "w", encoding="utf-8") as file_handle:
            file_handle.write(story_content)
        print("Saved story to {}".format(filename))
    except Exception as error:
        print("Error saving the story: {}".format(error))

def generate_and_save_stories(total_stories: int) -> None:
    for index in range(total_stories):
        print("Generating story {} of {}...".format(index + 1, total_stories))
        story_text = generate_story()
        if story_text:
            save_story_to_file(story_text)
        else:
            print("Skipping story {} due to an error.".format(index + 1))

def main() -> None:
    generate_and_save_stories(NUMBER_OF_STORIES)

if __name__ == "__main__":
    main()
