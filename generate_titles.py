import os

from common_lib import LANGUAGE_CODES_WITH_NAMES, TITLES_DIR, LmResponse, StoryTitles, TextProcessing, get_lm_caller, num_lines_in_file

MODEL = "meta-llama-3.1-8b-instruct@Q4_K_M"

NUMBER_OF_RUNS = 1
LANG_ID = "en"
MAX_TITLES_PER_LANG = 1000

LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"

LM_TEMPERATURE = 1
LM_FREQUENCY_PENALTY = 0
LM_PRESENCE_PENALTY = 0

call_local_lm = get_lm_caller(LM_STUDIO_API_BASE, LM_STUDIO_API_KEY, MODEL, LM_TEMPERATURE, LM_FREQUENCY_PENALTY, LM_PRESENCE_PENALTY)

class LmTitlesResponse(LmResponse):
    pass

def build_titles_prompt(lang_id: str) -> str:
    num_words = 6
    pre_made_prompts = {}
    pre_made_prompts['nl'] = (
        "Maak je lijstje met 20 titels voor nieuwe (niet bestaande) Nederlandse kinderverhalen. \n"
        "De titels moeten volledig in correct Nederlands (NL) geschreven zijn.\n"
        "Wees creatief! Wees origineel! \n"
        "Geef de titels in <title> tags. De titels moeten minimaal {num_words} woorden lang zijn. \n"
        "Voeg geen extra commentaar of uitleg toe; geef alleen de titles in <title> tags. \n"

    )
    english_prompt_template = (
        "Make a list of 20 titles for new (not existing) {language_name} children's stories. \n"
        "The titles must be completely written in proper {language_name} ({language_code}).\n"
        "Be creative! Be original! \n"
        "Give the titles in <title> tags. The titles must be at least {num_words} words long. \n"
        "Do not add any additional comments or explanations; only provide the titles in <title> tags."
    )

    if lang_id in pre_made_prompts:
        prompt = pre_made_prompts[lang_id].format(num_words=num_words)
    else:
        language_name = LANGUAGE_CODES_WITH_NAMES[lang_id]
        prompt = english_prompt_template.format(num_words=num_words, language_name=language_name, language_code=lang_id.upper())

    return prompt

def generate_titles(lang_id: str, titles_dir: str, run_num: int) -> None:

    print("Generating titles for '{}' (batch {} of {})...".format(lang_id, run_num + 1, NUMBER_OF_RUNS))

    prompt_text = build_titles_prompt(lang_id)
    response_data = call_local_lm(prompt_text, lang_id)
    if not response_data:
        return
    (response_content, prompt_text, model, lang_id, time_taken) = response_data
    lm_response = LmTitlesResponse(response_content, prompt_text, model, lang_id, time_taken)

    titles_from_content = lm_response.content_from_tags("title")

    if not titles_from_content:
        print("No titles found in response.")
        print(lm_response.response_content)
        return

    story_titles = StoryTitles(lang_id, titles_dir)
    titles_prefixes = set()
    titles_from_content = [TextProcessing.get_plain_text(title).strip('"’”“') for title in titles_from_content]

    num_titles_added = 0
    for title in titles_from_content:
        prefix = title[0:10]
        if prefix not in titles_prefixes:
            titles_prefixes.add(prefix)
            story_titles.titles.append(title)
            num_titles_added += 1

    story_titles.save()

    if num_titles_added == 0:
        print("No new titles added to titles file!")

    file_size_in_mb = os.path.getsize(story_titles.file_path) / 1024 / 1024
    if file_size_in_mb > 1:
        raise Exception("Titles file is too large ({:.2f} MB).".format(file_size_in_mb))



def main(lang_id: str) -> None:

    assert lang_id == "*" or lang_id in LANGUAGE_CODES_WITH_NAMES

    num_runs = 0

    if lang_id != "*":
        for _ in range(NUMBER_OF_RUNS):
            generate_titles(lang_id, TITLES_DIR, num_runs)
            num_runs += 1
    else:
        for lang_id in LANGUAGE_CODES_WITH_NAMES:
            lang_title_file = os.path.join(TITLES_DIR, "titles_{}.txt".format(lang_id))
            if num_lines_in_file(lang_title_file) > MAX_TITLES_PER_LANG:
                print("Skipping '{}' because it already has {} titles.".format(lang_id, MAX_TITLES_PER_LANG))
                continue
            for _ in range(NUMBER_OF_RUNS):
                generate_titles(lang_id, TITLES_DIR, num_runs)
                num_runs += 1
                if num_runs >= NUMBER_OF_RUNS:
                    break
            if num_runs >= NUMBER_OF_RUNS:
                break

if __name__ == "__main__":
    main(LANG_ID)
