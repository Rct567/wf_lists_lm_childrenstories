import os

from common_lib import LmResponse, StoryTitles, TextProcessing, get_lm_caller

LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "meta-llama-3.1-8b-instruct"

STORIES_DIR = "stories"
TITLES_DIR = "titles"
LANG_ID = "nl"

# Temperature and top_p can be tuned to control the randomness of the output.
LM_TEMPERATURE = 1
LM_FREQUENCY_PENALTY = 0
LM_PRESENCE_PENALTY = 0

call_local_lm = get_lm_caller(LM_STUDIO_API_BASE, LM_STUDIO_API_KEY, MODEL, LM_TEMPERATURE, LM_FREQUENCY_PENALTY, LM_PRESENCE_PENALTY)

class LmTitlesResponse(LmResponse):
    pass

def build_titles_prompt(lang_id: str) -> str:
    prompt = {}
    prompt['nl'] = (
        "Maak je lijstje met 20 titels voor nieuwe (niet bestaande) Nederlandse kinderverhalen. \n"
        "Wees creatief! Wees origineel! \n"
        "Geef de titels in <title> tags. De titels moeten minimaal 6 woorden lang zijn. \n"
        "Voeg geen extra commentaar of uitleg toe; geef alleen de titles in <title> tags. \n"

    )
    prompt['en'] = (
        "Make a list of 40 titles for new (not existing) English children's stories. \n"
        "Be creative! Give the titles in <title> tags. The titles must be at least 6 words long. \n"
    )
    return prompt[lang_id]

def generate_titles(lang_id: str, titles_dir: str) -> None:

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

    for title in titles_from_content:
        prefix = title[0:10]
        if prefix not in titles_prefixes:
            titles_prefixes.add(prefix)
            story_titles.titles.append(title)

    story_titles.save()

    file_size_in_mb = os.path.getsize(story_titles.file_path) / 1024 / 1024
    if file_size_in_mb > 0.5:
        raise Exception("Titles file is too large ({:.2f} MB).".format(file_size_in_mb))

def main() -> None:
    while True:
        generate_titles(LANG_ID, TITLES_DIR)


if __name__ == "__main__":
    main()
