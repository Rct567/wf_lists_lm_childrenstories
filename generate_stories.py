import datetime
import os
import re
from statistics import fmean
import time
from typing import Optional
from openai import OpenAI

from common_lib import LANGUAGE_CODES_WITH_NAMES, STORIES_DIR, TITLES_DIR, LmResponse, StoryTitles, get_lm_caller, num_text_files_in_dir


# Vulcan:
# meta-llama-3.1-8b-instruct (Q4_K_M) => 151s ps
# llama-3.2-3b-instruct (Q8_0, 3.42 GB) => 120s ps
# llama-3.2-1b-instruct (Q8_0, 1.32 GB) => 28s ps

# ROCm llama.cpp
# meta-llama-3.1-8b-instruct (Q4_K_M) => 133s ps (8 words per second)
# llama-3.2-3b-instruct (Q8_0, 3.42 GB) => 81s ps

# CPU Llama.cpp
# meta-llama-3.1-8b-instruct (Q4_K_M) => 168s ps (6 words per second)


MODEL = "meta-llama-3.1-8b-instruct@Q4_K_M"
#MODEL = "llama-3.2-3b-instruct@Q8_0"

NUMBER_OF_STORIES = 30
LANG_ID = "*"
MAX_STORIES_PER_LANG = 10

LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"

LM_TEMPERATURE = 0.9
LM_FREQUENCY_PENALTY = 0
LM_PRESENCE_PENALTY = 0

call_local_lm = get_lm_caller(LM_STUDIO_API_BASE, LM_STUDIO_API_KEY, MODEL, LM_TEMPERATURE, LM_FREQUENCY_PENALTY, LM_PRESENCE_PENALTY)

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
                print("Tag '{}' has no valid content.".format(tag))
                return False
        return True

    def save_to_file(self, file_path: str) -> None:
        if not self.is_valid():
            raise Exception("Invalid story can not be saved.")
        with open(file_path, "w", encoding="utf-8") as file_handle:
            file_handle.write("<prompt>\n{}</prompt>\n\n".format(self.prompt))
            file_handle.write("<model>{}</model>\n\n".format(self.model))
            file_handle.write("<lang_id>{}</lang_id>\n\n".format(self.lang_id))
            file_handle.write(self.response_content)
        print("Saved story to '{}'.".format(file_path))

def build_story_prompt(lang_id: str, story_titles: StoryTitles) -> str:

    assert lang_id == story_titles.lang_id
    num_words = 1000

    pre_made_prompts = {}
    pre_made_prompts['nl'] = (
        "Schrijf een creatief en origineel Nederlands kinderverhaal van minstens {num_words} woorden:\n"
        "Het moet volledig in correct Nederlands (NL) geschreven zijn.\n"
        "De titel van het verhaal moet geplaats worden in <title> tags en het verhaal zelf in <body> tags.\n"
        "Voorbeeld: <title>De title van het verhaal</title><body>Het verhaal zelf</body>\n"
        "Voeg geen extra commentaar of uitleg toe; geef alleen het verhaal in het opgegeven formaat.\n"
    )

    english_prompt_template = (
        "Please write a creative and original {language_name} children's story that is at least {num_words} words long.\n"
        "It must be completely written in proper {language_name} ({language_code}).\n"
        "Ensure that the title of the story is enclosed in <title> tags and the body of the story is enclosed in <body> tags.\n"
        "Example: <title>The title of the story</title><body>The story itself</body>\n"
        "Do not include any extra commentary or explanation; output only the story in the specified format.\n"
    )

    if lang_id in pre_made_prompts:
        prompt = pre_made_prompts[lang_id].format(num_words=num_words)
    else:
        language_name = LANGUAGE_CODES_WITH_NAMES[lang_id]
        prompt = english_prompt_template.format(num_words=num_words, language_name=language_name, language_code=lang_id.upper())

    # add story title

    title = story_titles.get_new_title()

    if not title:
        return prompt

    pre_made_title_prompt = {}
    pre_made_title_prompt['nl'] = "De titel van het verhaal is: '{}'."

    english_title_prompts_template = "The title of the story is: '{}'."

    if lang_id in pre_made_title_prompt:
        prompt += ""+pre_made_title_prompt[lang_id].format(title)+"\n"
    else:
        prompt += ""+english_title_prompts_template.format(title)+"\n"

    return prompt


def get_story_response_from_lm(prompt_text: str, lang_id: str) -> Optional[LmStoryResponse]:
    response_data = call_local_lm(prompt_text, lang_id)
    if not response_data:
        return None
    (response_content, prompt_text, model, lang_id, time_taken) = response_data
    return LmStoryResponse(response_content, prompt_text, model, lang_id, time_taken)

def generate_story(lang_id: str, story_titles: StoryTitles) -> Optional[LmStoryResponse]:
    prompt_text = build_story_prompt(lang_id, story_titles)
    response = get_story_response_from_lm(prompt_text, lang_id)
    return response

def save_story_to_file(story_dir: str, story: LmStoryResponse) -> None:
    story_lang_dir = os.path.join(story_dir, story.lang_id)
    if not os.path.exists(story_lang_dir):
        os.makedirs(story_lang_dir)
    file_path = os.path.join(story_lang_dir, "{}.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")))
    try:
        story.save_to_file(file_path)
    except Exception as error:
        print("Error saving the story: {}".format(error))

def generate_and_save_stories(total_stories: int, stories_dir: str, titles_dir: str, lang_id: str) -> None:
    if not os.path.exists(stories_dir):
        os.makedirs(stories_dir)

    story_titles = StoryTitles(lang_id, titles_dir)
    stories_generated = []
    for index in range(total_stories):
        print("Generating story {} of {}...".format(index + 1, total_stories))
        lm_response = generate_story(lang_id, story_titles)
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



def main(lang_id: str) -> None:

    assert lang_id == "*" or lang_id in LANGUAGE_CODES_WITH_NAMES

    if lang_id != "*":
        generate_and_save_stories(NUMBER_OF_STORIES, STORIES_DIR, TITLES_DIR, lang_id)
    else:
        for lang_id in LANGUAGE_CODES_WITH_NAMES:
            lang_story_dir = os.path.join(STORIES_DIR, lang_id)
            if os.path.exists(lang_story_dir) and num_text_files_in_dir(lang_story_dir) > MAX_STORIES_PER_LANG:
                print("Skipping '{}' because it already has {} stories.".format(lang_id, MAX_STORIES_PER_LANG))
                continue
            print("Generating stories for '{}'...".format(lang_id))
            generate_and_save_stories(NUMBER_OF_STORIES, STORIES_DIR, TITLES_DIR, lang_id)
            break

if __name__ == "__main__":
    main(LANG_ID)
