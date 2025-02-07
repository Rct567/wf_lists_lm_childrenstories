import datetime
import os
import random
from openai import OpenAI

LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "llama-3.2-3b-instruct-uncensored"
NUMBER_OF_STORIES = 3

# Temperature and top_p can be tuned to control the randomness of the output.
LM_TEMPERATURE = 0.9
LM_TOP_P = 0.95

client = OpenAI(base_url=LM_STUDIO_API_BASE, api_key=LM_STUDIO_API_KEY)

def generate_random_story_pointer() -> str:
    genre_adjectives: list[str] = [
        "magical", "exciting", "whimsical", "enchanting", "adventurous",
        "heartwarming", "charming", "funny", "clever", "smart", "playful",
        "bright", "colorful", "joyful", "happy", "sparkly", "radiant",
        "cheerful", "merry", "bubbly", "glittering"
    ]

    genres: list[str] = [
        "fairy tale", "adventure", "mystery", "fantasy", "fable",
        "science fiction", "animal tale", "magical mystery", "storybook",
        "imaginative journey", "pirate adventure", "enchanted quest",
        "underwater adventure", "whimsical fantasy", "sunny tale"
    ]

    settings: list[str] = [
        "an forest", "outer space", "an underwater kingdom",
        "a castle", "a garden", "a tree house", "a house",
        "a park", "a kingdom", "an office",
        "a playground", "a farm", "a library", "a kitchen",
        "a village", "a jungle",
        "a spaceship", "a space station", "a submarine",
        "a cave", "a mountain", "a ship", "a field",
        "a school", "a museum", "a shop",
        "an island", "a camp", "a store"
    ]

    protagonists_adjectives: list[str] = [
        "brave", "curious", "clever", "smart", "friendly", "kind",
        "playful", "happy", "joyful", "adventurous", "gentle", "loving",
        "cheerful", "optimistic", "sparkling", "graceful", "energetic",
        "bubbly", "smiling", "wise", "everyday", ""
    ]

    protagonists: list[str] = [
        "girl", "boy", "talking animal", "fairy", "wizard", "child",
        "princess", "prince", "mermaid", "elf", "dwarf", "genie", "knight",
        "dragon", "unicorn", "puppy", "kitten", "teddy bear", "superhero",
        "sailor", "pirate", "robot"
    ]

    twists: list[str] = [
        "that teaches the value of friendship",
        "filled with unexpected adventures",
        "where magic happens around every corner",
        "that brings joy and laughter",
        "with a delightful surprise",
        "that makes you laugh out loud",
        "that shows the power of kindness",
        "with a happy ending",
        "that sparks imagination",
        "where dreams come true",
        "where every moment is a giggle",
        "that celebrates the joy of discovery",
    ]

    genre_adjective = random.choice(genre_adjectives)
    genre = random.choice(genres)
    setting = random.choice(settings)
    protagonist_adjective = random.choice(protagonists_adjectives)
    protagonist = random.choice(protagonists)
    twist = random.choice(twists)

    pointer: str = "A {genre_adjective} {genre} story {twist}, set in {setting}, featuring a '{protagonist_adjective} {protagonist}'.".format(
        genre_adjective=genre_adjective,
        genre=genre,
        setting=setting,
        protagonist_adjective=protagonist_adjective,
        protagonist=protagonist,
        twist=twist
    )
    return pointer

def build_story_prompt() -> str:
    selected_pointer = generate_random_story_pointer()
    print("Pointer selected: {}".format(selected_pointer))
    prompt = (
        "Please write a creative and original Dutch children's story that is at least 1000 words long. Completely written in Dutch (NL)."
        "The story should be based on the theme: {pointer}. "
        "Ensure that the title of the story is enclosed in <title> tags and the body of the story is enclosed in <body> tags. "
        "Do not include any extra commentary or explanation; output only the story in the specified format."
    ).format(pointer=selected_pointer)
    return prompt

def call_local_lm(prompt_text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a creative children's story writer."},
        {"role": "user", "content": prompt_text}
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=LM_TEMPERATURE,
            top_p=LM_TOP_P
        )
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
