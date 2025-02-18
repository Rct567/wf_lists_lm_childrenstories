
import os
import random
from typing import Generator, Iterable, Optional, Union

from lib.language_data import LANGUAGE_CODES_WITH_NAMES
from lib.text_processing import TextProcessing, WordToken

STORIES_DIR = "stories"
TITLES_DIR = "titles"
WF_LISTS_DIR = "wf_lists"


def num_text_files_in_dir(dir_path: str) -> int:
    if not os.path.exists(dir_path):
        return 0
    files_in_dir = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
    text_files_in_dir = [file for file in files_in_dir if file.endswith(".txt")]
    return len(text_files_in_dir)

def num_lines_in_file(file_path: str) -> int:
    if not os.path.exists(file_path):
        print("File '{}' does not exist.".format(file_path))
        return 0
    with open(file_path, 'r', encoding="utf-8") as f:
        return sum(1 for _ in f)

def get_languages_to_process(lang_ids: Union[str, list[str]]) -> list[str]:

    assert isinstance(lang_ids, list) or lang_ids == "*" or lang_ids in LANGUAGE_CODES_WITH_NAMES
    assert not isinstance(lang_ids, list) or all(item in LANGUAGE_CODES_WITH_NAMES for item in lang_ids)

    if isinstance(lang_ids, str) and lang_ids == "*":
        languages_to_process = list(LANGUAGE_CODES_WITH_NAMES.keys())
    elif isinstance(lang_ids, str) and lang_ids != "*":
        languages_to_process = [lang_ids]
    elif isinstance(lang_ids, list):
        languages_to_process: list[str] = lang_ids
    else:
        raise ValueError("lang_ids must be a string, a list of strings, or '*'.")

    return languages_to_process

def keep_looping_through_languages(languages: list[str]) -> Generator[str, None, None]:

    loops = 0

    while True:
        for lang_id in languages:
            yield lang_id
        loops += 1
        if loops >= 100_000:
            raise Exception("Too many loops.")


class StoryTitles:

    min_num_words_title = 4
    max_num_words_title = 40
    max_length_title = 100
    prefix_num_words = 2

    def __init__(self, lang_id: str, titles_dir: str):
        if not os.path.exists(titles_dir):
            os.makedirs(titles_dir)
        self.file_name = "titles_{}.txt".format(lang_id)
        self.file_path = os.path.join(titles_dir, self.file_name)
        self.lang_id = lang_id
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                self.titles = [title for title in self.unique_titles(f)]
        except FileNotFoundError:
            self.titles = []

        random.shuffle(self.titles)

        valid_titles = [title for title in self.titles if StoryTitles.title_is_acceptable(title, self.lang_id)]
        if len(valid_titles) != len(self.titles):
            self.titles = valid_titles
            print("Removed {} invalid titles from loaded titles.".format(len(self.titles) - len(valid_titles)))
            self.save()

    def unique_titles(self, titles: Iterable[str]) -> Generator[str, None, None]:
        unique_prefixes = set()
        for title in titles:
            title = title.strip()
            assert "\n" not in title and "\r" not in title
            if len(title) > self.max_length_title:
                print("Title '{}' is too long.".format(title))
                continue
            title_tokens = TextProcessing.get_word_tokens_from_text(title, self.lang_id, filter_words=False)
            if len(title_tokens) < self.min_num_words_title:
                print(title_tokens)
                print("Title '{}' has too few words ({}).".format(title, len(title_tokens)))
                continue
            if len(title_tokens) > self.max_num_words_title:
                print("Title '{}' has too many words.".format(title))
                continue
            title_prefix = self.prefix_from_title(title, title_tokens)
            if not title_prefix:
                print("Title '{}' has no valid prefix.".format(title))
                continue
            if title_prefix in unique_prefixes:
                print("Title '{}' has a duplicate prefix.".format(title))
                continue
            yield title
            unique_prefixes.add(title_prefix)

    @staticmethod
    def title_is_acceptable(title: str, lang_id: str) -> bool:
        if any(char in title for char in "{}[]<>@#$%^*+"):
            print("Title '{}' contains invalid characters.".format(title))
            return False
        word_accepter = TextProcessing.get_word_accepter(lang_id)
        for word in TextProcessing.get_word_tokens_from_text(title, lang_id, filter_words=False):
            if not word_accepter(word):
                print("Title '{}' contains invalid word '{}' for language '{}'.".format(title, word, lang_id))
                return False
        return True

    def prefix_from_title(self, title: str, title_tokens: Optional[list[WordToken]] = None) -> Optional[str]:
        if title_tokens == None:
            title_tokens = TextProcessing.get_word_tokens_from_text(title, self.lang_id, filter_words=False)
        if len(title_tokens) < self.prefix_num_words:
            print("Title '{}' has too few tokens for prefix.".format(title))
            return None
        return " ".join(title_tokens[0:self.prefix_num_words])

    def get_new_title(self) -> Optional[str]:
        if not self.titles:
            return None
        title = self.titles.pop(0)
        self.save()
        return title

    def save(self) -> int:
        num_saved = 0
        with open(self.file_path, 'w', encoding="utf-8") as f:
            for title in self.unique_titles(self.titles):
                if not StoryTitles.title_is_acceptable(title, self.lang_id):
                    print("Title '{}' is not acceptable. Title not saved.".format(title))
                    continue
                f.write(f"{title}\n")
                num_saved += 1
        return num_saved

