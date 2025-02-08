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
    def __init__(self, content: str, prompt: str, model: str):
        self.content = content.strip()
        self.prompt = prompt
        self.model = model

    def is_valid(self) -> bool:
        return all(x in self.content for x in {"<title>", "<body>"})

    @staticmethod
    def content_from_tag(content: str, tag: str) -> Optional[str]:
        content_match = re.search(r"<{}>(.*?)</{}>".format(tag, tag), content, re.DOTALL | re.IGNORECASE)
        if not content_match:
            return None
        return content_match.group(1).strip()

    def get_title(self) -> str:
        title = self.content_from_tag(self.content, "title")
        if not title:
            return ""
        return title

    def save_to_file(self, filename: str) -> None:
        if not self.is_valid():
            print(self.content)
            print("Skipping invalid story.")
            return
        with open(filename, "w", encoding="utf-8") as file_handle:
            file_handle.write("<prompt>\n{}</prompt>\n\n".format(self.prompt))
            file_handle.write("<model>{}</model>\n\n".format(self.model))
            file_handle.write(self.content)
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

def call_local_lm(prompt_text: str) -> Optional[LmResponse]:
    messages = [
        {"role": "system", "content": "You are a creative children's story writer."},
        {"role": "user", "content": prompt_text}
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages, # type: ignore
            temperature=LM_TEMPERATURE,
            top_p=LM_TOP_P
        )
        content = response.choices[0].message.content
        if not content:
            return None
        return LmResponse(content, prompt_text, MODEL)

    except Exception as error:
        print("Error while generating story: {}".format(error))
        return None

def generate_story(lang_id: str) -> Optional[LmResponse]:
    prompt_text = build_story_prompt(lang_id)
    response = call_local_lm(prompt_text)
    return response

def save_story_to_file(story_dir: str, story: LmResponse) -> None:
    filename = os.path.join(story_dir, "{}.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")))
    try:
        story.save_to_file(filename)
    except Exception as error:
        print("Error saving the story: {}".format(error))

def generate_and_save_stories(total_stories: int, stories_dir: str, lang_id: str) -> None:
    if not os.path.exists(stories_dir):
        os.makedirs(stories_dir)
    time_per_story = []
    for index in range(total_stories):
        print("Generating story {} of {}...".format(index + 1, total_stories))
        start_time = time.perf_counter()
        lm_response = generate_story(lang_id)
        time_taken = time.perf_counter() - start_time
        if lm_response:
            time_per_story.append(time_taken)
            print("Story '{}' generated in {:.2f} seconds.".format(lm_response.get_title(), time_taken))
            save_story_to_file(stories_dir, lm_response)
        else:
            print("Skipping story {} due to an error.".format(index + 1))
    if time_per_story:
        print("{} stories generated in {:.2f} seconds ({:.2f} per story).".format(len(time_per_story), sum(time_per_story), fmean(time_per_story)))
    else:
        print("No stories generated.")

def main() -> None:
    generate_and_save_stories(NUMBER_OF_STORIES, STORIES_DIR, LANG_ID)

if __name__ == "__main__":
    main()
