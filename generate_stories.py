import datetime
from functools import cache
import os
import random
from statistics import fmean
from typing import Optional, Union


from lib.language_data import LANGUAGE_CODES_WITH_NAMES
from lib.lm import LmResponse, get_lm_caller
from lib.misc import STORIES_DIR, TITLES_DIR, StoryTitles, get_languages_to_process, keep_looping_through_languages, num_text_files_in_dir
from lib.text_processing import TextProcessing



NUMBER_OF_RUNS = 200
LANG_ID = "*"
MAX_STORIES_PER_LANG = 100

LM_TEMPERATURE = 0.9
LM_FREQUENCY_PENALTY = 0
LM_PRESENCE_PENALTY = 0

call_local_lm = get_lm_caller(LM_STUDIO_API_BASE, LM_STUDIO_API_KEY, MODEL, LM_TEMPERATURE, LM_FREQUENCY_PENALTY, LM_PRESENCE_PENALTY)

class LmStoryResponse(LmResponse):

    def get_title(self) -> str:
        return self.content_from_tag_or_empty("title")

    @cache
    def is_valid(self) -> bool:
        for tag in {"<title>", "<body>"}:
            if self.response_content.count(tag) == 0:
                print("Tag '{}' not found.".format(tag))
                return False
            if self.response_content.count(tag) > 1:
                print("Tag '{}' appears more than once.".format(tag))
                return False
            content_in_tag = self.content_from_tag(tag)
            if not content_in_tag:
                print("Tag '{}' has no valid content.".format(tag))
                return False
            elif len(content_in_tag) < 5:
                print("Tag '{}' has too few characters ({}).".format(tag, len(content_in_tag)))
                return False

        body_content = self.content_from_tag_or_empty("body")

        if TextProcessing.has_repetitive_sentences(body_content):
            print("Response contains repetitive sentences in body.")
            return False

        token_rejection_rate = TextProcessing.get_word_token_rejection_rate(body_content, self.lang_id)
        if token_rejection_rate > 0.1:
            print("Response contains too many rejected words in body (rejection rate: {}).".format(token_rejection_rate))
            return False

        num_none_letter_sequences = TextProcessing.num_lines_non_letter_sequence(body_content, r"!@#$%^&()_+={}\[\]:;\"'<>/\\|-~")
        if num_none_letter_sequences >= 3:
            print("Response contains too many none-letter sequences.")
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
    # pre_made_prompts['nl'] = (
    #     "Schrijf een creatief en origineel Nederlands kinderverhaal van minstens {num_words} woorden:\n"
    #     "Het moet volledig in correct Nederlands (NL) geschreven zijn.\n"
    #     "De titel van het verhaal moet geplaats worden in <title> tags en het verhaal zelf in <body> tags.\n"
    #     "Voorbeeld: <title>De title van het verhaal</title><body>Het verhaal zelf</body>\n"
    #     "Voeg geen extra commentaar of uitleg toe; geef alleen het verhaal in het opgegeven formaat.\n"
    # )

    story_adjectives = ['creative and original', 'dialog-based', 'funny', 'fun and entertaining', 'educational', 'silly', 'uncomplicated',
                        'simple and easy-to-follow', 'light-hearted', 'emotional', 'timeless', 'relatable']
    random_story_adjective = random.choice(story_adjectives)

    english_prompt_template = (
        "Please write a {story_adjective} {language_name} children's story that is at least {num_words} words long.\n"
        "It must be completely written in proper {language_name} ({language_code}).\n"
        "Ensure that the title of the story is enclosed in <title> tags and the body of the story is enclosed in <body> tags.\n"
        "Example: <title>The title of the story</title><body>The story itself</body>\n"
        "Do not include any extra commentary or explanation; output only the story in the specified format.\n"
    )

    if lang_id in pre_made_prompts:
        prompt = pre_made_prompts[lang_id].format(num_words=num_words)
    else:
        language_name = LANGUAGE_CODES_WITH_NAMES[lang_id]
        prompt = english_prompt_template.format(
            num_words=num_words,
            language_name=language_name,
            language_code=lang_id.upper(),
            story_adjective=random_story_adjective,
        )

    # add story title

    title = story_titles.get_new_title()

    if not title:
        print("Prompt made without title for story!")
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

def generate_and_save_story(stories_dir: str, titles_dir: str, lang_id: str, run_num: int) -> Optional[LmStoryResponse]:

    print("Generating story for language '{}' ({}/{})...".format(LANGUAGE_CODES_WITH_NAMES[lang_id], run_num + 1, NUMBER_OF_RUNS))

    story_titles = StoryTitles(lang_id, titles_dir)

    if not os.path.exists(stories_dir):
        os.makedirs(stories_dir)

    lm_response = generate_story(lang_id, story_titles)
    if not lm_response:
        print("Skipped saving story due to an error.")
        return

    print("Story '{}' generated in {:.2f} seconds ({} words).".format(lm_response.get_title(), lm_response.time_taken, lm_response.num_words_in_content()))

    if lm_response.is_valid():
        save_story_to_file(stories_dir, lm_response)
    else:
        print("Invalid story not saved.")
        return

    return lm_response


def main(lang_ids: Union[str, list[str]]) -> None:

    stories_generated: list[LmStoryResponse] = []
    num_runs = 0
    languages_to_process = get_languages_to_process(lang_ids)
    languages_skipped = set()

    for lang_id in keep_looping_through_languages(languages_to_process):

        if num_runs >= NUMBER_OF_RUNS:
            print("Out of runs.")
            break
        if len(languages_skipped) >= len(languages_to_process):
            print("Out of languages to process.")
            break
        if lang_id in languages_skipped:
            continue

        print("Working on language '{}' ({})...".format(lang_id, LANGUAGE_CODES_WITH_NAMES[lang_id]))
        lang_story_dir = os.path.join(STORIES_DIR, lang_id)
        if num_text_files_in_dir(lang_story_dir) > MAX_STORIES_PER_LANG:
            print("Skipping '{}' because it already has {} stories.".format(lang_id, MAX_STORIES_PER_LANG))
            languages_skipped.add(lang_id)
            continue

        story = generate_and_save_story(STORIES_DIR, TITLES_DIR, lang_id, num_runs)
        if story:
            stories_generated.append(story)
        num_runs += 1

    if stories_generated:
        time_per_story = [story.time_taken for story in stories_generated]
        print("{} stories generated in {:.2f} seconds ({:.2f}s per story).".format(len(time_per_story), sum(time_per_story), fmean(time_per_story)))
        num_words_per_second = fmean([story.get_num_words_per_second() for story in stories_generated])
        print("Rate: {:.0f} words per second.".format(num_words_per_second))
    else:
        print("No stories generated.")

if __name__ == "__main__":
    main(LANG_ID)
