import datetime
import os
import re
from statistics import fmean
import time
from typing import Optional
from openai import OpenAI

from common_lib import LmResponse, get_lm_caller


# Vulcan:
# meta-llama-3.1-8b-instruct (Q4_K_M) => 151s ps
# llama-3.2-3b-instruct (Q8_0, 3.42 GB) => 120s ps
# llama-3.2-1b-instruct (Q8_0, 1.32 GB) => 28s ps

# ROCm llama.cpp
# meta-llama-3.1-8b-instruct (Q4_K_M) => 133s ps (8 words per second)
# llama-3.2-3b-instruct (Q8_0, 3.42 GB) => 81s ps

# CPU Llama.cpp
# meta-llama-3.1-8b-instruct (Q4_K_M) => 168s ps (6 words per second)


LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "meta-llama-3.1-8b-instruct (Q4_K_M)"

NUMBER_OF_STORIES = 3
STORIES_DIR = "stories"
LANG_ID = "nl"

# Temperature and top_p can be tuned to control the randomness of the output.
LM_TEMPERATURE = 0.9
LM_TOP_P = 0.95

call_local_lm = get_lm_caller(LM_STUDIO_API_BASE, LM_STUDIO_API_KEY, MODEL, LM_TEMPERATURE, LM_TOP_P)

class LmStoryResponse(LmResponse):

    def get_title(self) -> str:
        return self.content_from_tag_or_empty("title")

    def is_valid(self) -> bool:
        for tag in {"<title>", "<body>"}:
            if self.response_content.count(tag) == 0:
                print("Tag '{}' not found.".format(tag))
                return False
            if self.response_content.count(tag) > 1:
                print("Tag '{}' appears more than once.".format(tag))
                return False
            content_in_tag = self.content_from_tag(tag)
            if not content_in_tag or len(content_in_tag) < 10:
                print("Tag '{}' not valid.".format(tag))
                return False
        return True

    def save_to_file(self, filename: str) -> None:
        if not self.is_valid():
            raise Exception("Invalid story can not be saved.")
        with open(filename, "w", encoding="utf-8") as file_handle:
            file_handle.write("<prompt>\n{}</prompt>\n\n".format(self.prompt))
            file_handle.write("<model>{}</model>\n\n".format(self.model))
            file_handle.write("<lang_id>{}</lang_id>\n\n".format(self.lang_id))
            file_handle.write(self.response_content)
        print("Saved story to '{}'.".format(filename))

def build_story_prompt(lang_id: str) -> str:
    prompt = {}
    prompt['en'] = (
        "Please write a creative and original children's story that is at least 1000 words long. \n"
        "It must be completely written in proper English. \n"
        "Ensure that the title of the story is enclosed in <title> tags and the body of the story is enclosed in <body> tags. \n"
        "Example: <title>The title of the story</title><body>The story itself</body>\n"
        "Do not include any extra commentary or explanation; output only the story in the specified format. \n"
    )
    prompt['nl'] = (
        "Schrijf een creatief en origineel Nederlands kinderverhaal van minstens 1000 woorden: \n"
        "Het moet volledig in correct Nederlands (NL) geschreven zijn. \n"
        "De titel van het verhaal moet geplaats worden in <title> tags en het verhaal zelf in <body> tags. \n"
        "Voorbeeld: <title>De title van het verhaal</title><body>Het verhaal zelf</body>\n"
        "Voeg geen extra commentaar of uitleg toe; geef alleen het verhaal in de opgegeven formaat. \n"
    )
    return prompt[lang_id]




def get_story_response_from_lm(prompt_text: str, lang_id: str) -> Optional[LmStoryResponse]:
    response_data = call_local_lm(prompt_text, lang_id)
    if not response_data:
        return None
    (response_content, prompt_text, model, lang_id, time_taken) = response_data
    return LmStoryResponse(response_content, prompt_text, model, lang_id, time_taken)

def generate_story(lang_id: str) -> Optional[LmStoryResponse]:
    prompt_text = build_story_prompt(lang_id)
    response = get_story_response_from_lm(prompt_text, lang_id)
    return response

def save_story_to_file(story_dir: str, story: LmStoryResponse) -> None:
    story_lang_dir = os.path.join(story_dir, story.lang_id)
    if not os.path.exists(story_lang_dir):
        os.makedirs(story_lang_dir)
    filename = os.path.join(story_lang_dir, "{}.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")))
    try:
        story.save_to_file(filename)
    except Exception as error:
        print("Error saving the story: {}".format(error))

def generate_and_save_stories(total_stories: int, stories_dir: str, lang_id: str) -> None:
    if not os.path.exists(stories_dir):
        os.makedirs(stories_dir)

    stories_generated = []
    for index in range(total_stories):
        print("Generating story {} of {}...".format(index + 1, total_stories))
        lm_response = generate_story(lang_id)
        if not lm_response:
            print("Skipping story {} due to an error.".format(index + 1))
            break
        stories_generated.append(lm_response)
        print("Story '{}' generated in {:.2f} seconds ({} words).".format(lm_response.get_title(), lm_response.time_taken, lm_response.num_words_in_content()))
        if lm_response.is_valid():
            save_story_to_file(stories_dir, lm_response)
        else:
            print("Invalid story not saved.")

    if stories_generated:
        time_per_story = [story.time_taken for story in stories_generated]
        print("{} stories generated in {:.2f} seconds ({:.2f}s per story).".format(len(time_per_story), sum(time_per_story), fmean(time_per_story)))
        num_words_per_second = fmean([story.get_num_words_per_second() for story in stories_generated])
        print("Rate: {:.0f} words per second.".format(num_words_per_second))
    else:
        print("No stories generated.")

def main() -> None:
    generate_and_save_stories(NUMBER_OF_STORIES, STORIES_DIR, LANG_ID)

if __name__ == "__main__":
    main()
