
from functools import cache
import os
import random
from typing import Generator, Iterable, Optional, ParamSpec, Union, Callable, TypeVar, Any, cast
import time

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

    random.shuffle(languages_to_process)

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

        valid_titles = [title for title in self.titles if self.title_is_acceptable(title)]
        if len(valid_titles) != len(self.titles):
            num_removed = len(self.titles) - len(valid_titles)
            print("Removed {} invalid titles from loaded titles.".format(num_removed))
            self.titles = valid_titles
            self.save()

    @cache
    def tokenize_title(self, title: str) -> list[WordToken]:
        return TextProcessing.get_word_tokens_from_text(title, self.lang_id, filter_words=False)

    def unique_titles(self, titles: Iterable[str]) -> Generator[str, None, None]:
        unique_prefixes = set()
        for title in titles:
            title = title.strip()
            assert "\n" not in title and "\r" not in title
            title_prefix = self.prefix_from_title(title)
            if not title_prefix:
                print("Title '{}' has no valid prefix.".format(title))
                continue
            if title_prefix in unique_prefixes:
                print("Title '{}' has a duplicate prefix.".format(title))
                continue
            yield title
            unique_prefixes.add(title_prefix)


    def title_is_acceptable(self, title: str) -> bool:
        if any(char in title for char in "{}[]<>@#$%^*+＠_°©®™∞±√"):
            print("Title '{}' contains invalid characters.".format(title))
            return False

        if TextProcessing.has_non_letter_sequences(title, r"!@#$%^&*()_+={}\[\]:;\"'<>,.?/\\|-~`"):
            print("Title '{}' contains non-letter sequences.".format(title))
            return False

        if len(title) > self.max_length_title:
            print("Title '{}' is too long.".format(title))
            return False

        word_accepter = TextProcessing.get_word_accepter(self.lang_id)
        title_tokens = self.tokenize_title(title)

        if len(title_tokens) < self.min_num_words_title:
            print(title_tokens)
            print("Title '{}' has too few words ({}).".format(title, len(title_tokens)))
            return False

        if len(title_tokens) > self.max_num_words_title:
            print("Title '{}' has too many words.".format(title))
            return False

        if len(set(title_tokens)) < len(title_tokens)/2:
            print("Title '{}' has too many repeated words.".format(title))
            return False

        for word in title_tokens:
            if not word_accepter(word):
                print("Title '{}' contains invalid word '{}' for language '{}'.".format(title, word, self.lang_id))
                return False

        return True

    def prefix_from_title(self, title: str) -> Optional[str]:
        title_tokens = self.tokenize_title(title)
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
                if not self.title_is_acceptable(title):
                    print("Title '{}' is not acceptable. Title not saved.".format(title))
                    continue
                f.write(f"{title}\n")
                num_saved += 1
        return num_saved



P = ParamSpec("P")
R = TypeVar("R")

class _RateLimiter:
    def __init__(self, max_per_minute: int):
        self.max_per_minute = max_per_minute
        self.interval = 60.0 / max_per_minute
        self.next_call_time: float = 0.0

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            current_time = time.monotonic()
            if current_time < self.next_call_time:
                sleep_duration = self.next_call_time - current_time
                print("Sleeping for {} seconds to stay within rate limit of {} calls per minute.".format(int(sleep_duration), self.max_per_minute))
                time.sleep(sleep_duration)
                current_time = time.monotonic()  # Get fresh time after sleep

            self.next_call_time = current_time + self.interval
            return func(*args, **kwargs)
        return wrapped

def rate_limit_per_minute(max_per_minute: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator factory that enforces a maximum call rate per minute."""
    return _RateLimiter(max_per_minute)

