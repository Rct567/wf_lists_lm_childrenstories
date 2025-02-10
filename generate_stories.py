import datetime
import os
import re
from statistics import fmean
import time
from typing import Optional
from openai import OpenAI

LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "llama-3.2-3b-instruct"


NUMBER_OF_STORIES = 3
STORIES_DIR = "stories"
LANG_ID = "nl"

# Temperature and top_p can be tuned to control the randomness of the output.
LM_TEMPERATURE = 0.9
LM_TOP_P = 0.95

class LmResponse:
    def __init__(self, response_content: str, prompt: str, model: str, lang_id: str, time_taken: float):
        self.response_content = response_content.strip()
        self.prompt = prompt
        self.model = model
        self.lang_id = lang_id
        self.time_taken = time_taken

    def is_valid(self) -> bool:
        for tag in {"<title>", "<body>"}:
            if self.response_content.count(tag) == 0:
                print("Tag '{}' not found.".format(tag))
                return False
            if self.response_content.count(tag) > 1:
                print("Tag '{}' appears more than once.".format(tag))
                return False
            content_in_tag = self.content_from_tag(self.response_content, tag)
            if not content_in_tag or len(content_in_tag) < 10:
                print("Tag '{}' not valid.".format(tag))
                return False
        return True

    @staticmethod
    def content_from_tag(content: str, tag_name: str) -> Optional[str]:
        tag_name = tag_name.strip('<>/')
        if "<body>" in content and not "</body>" in content:
            content = content + "</body>"
        content_match = re.search(r"<{}>(.*?)</{}>".format(tag_name, tag_name), content, re.DOTALL | re.IGNORECASE)
        if not content_match:
            return None
        return content_match.group(1).strip()

    def get_title(self) -> str:
        title = self.content_from_tag(self.response_content, "title")
        if not title:
            return ""
        return title

    def get_words_from_content(self) -> list[str]:
        return [word.strip() for word in self.response_content.split() if word.strip() != ""]

    def get_num_words_per_second(self) -> float:
        if self.response_content == "":
            return 0
        return len(self.get_words_from_content()) / self.time_taken

    def save_to_file(self, filename: str) -> None:
        if not self.is_valid():
            raise Exception("Invalid story can not be saved.")
        with open(filename, "w", encoding="utf-8") as file_handle:
            file_handle.write("<prompt>\n{}</prompt>\n\n".format(self.prompt))
            file_handle.write("<model>{}</model>\n\n".format(self.model))
            file_handle.write("<lang_id>{}</lang_id>\n\n".format(self.lang_id))
            file_handle.write(self.response_content)
        print("Saved story to '{}'.".format(filename))

client = OpenAI(base_url=LM_STUDIO_API_BASE, api_key=LM_STUDIO_API_KEY)



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

def call_local_lm(prompt_text: str, lang_id: str) -> Optional[LmResponse]:
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
        return LmResponse(response_content, prompt_text, MODEL, lang_id, time_taken)

    except Exception as error:
        print("Error while generating story: {}".format(error))
        return None

def generate_story(lang_id: str) -> Optional[LmResponse]:
    prompt_text = build_story_prompt(lang_id)
    response = call_local_lm(prompt_text, lang_id)
    return response

def save_story_to_file(story_dir: str, story: LmResponse) -> None:
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
            continue
        stories_generated.append(lm_response)
        print("Story '{}' generated in {:.2f} seconds ({} words).".format(lm_response.get_title(), lm_response.time_taken, len(lm_response.get_words_from_content())))
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
