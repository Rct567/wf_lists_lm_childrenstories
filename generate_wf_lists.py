from collections import Counter
from concurrent.futures import Executor, ProcessPoolExecutor
import csv
from functools import partial
import os
import re
from statistics import fmean
import time
from typing import Callable, NamedTuple, Optional, Sequence
from lib.language_data import LANGUAGE_CODES_WITH_NAMES
from lib.misc import STORIES_DIR, WF_LISTS_DIR
from lib.text_processing import TextProcessing, WordToken


def get_tokens_from_story(story_file_path: str, word_accepter: Callable[[str], bool], lang_id: str) -> Optional[Sequence[WordToken]]:

    content_of_file = open(story_file_path, "r", encoding="utf-8").read()

    if not "<title>" in content_of_file:
        print("No <title> tag found in file '{}'.".format(story_file_path))
        return None

    # start content from last <title> tag
    content = content_of_file[content_of_file.rfind("<title>"):].strip()

    match = re.search(r"<title>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
    if not match:
        print("No <title> tag found in file '{}'.".format(story_file_path))
        return None
    title_content = match.group(1).strip()

    if not "<body>" in content:
        print("No <body> tag found in file '{}'.".format(story_file_path))
        return None

    body_content = content[content.rfind("<body>")+len("<body>"):].strip().replace("</body>", "")
    body_tokens = TextProcessing.get_word_tokens_from_text(body_content, lang_id, filter_words=False)

    if not body_tokens:
        print("No word tokens found in body of file '{}'.".format(story_file_path))
        return None
    elif len(body_tokens) > 10_000:
        print("WARNING: File '{}' contains {} words in body.".format(story_file_path, len(body_tokens)))

    word_token_rejection_rate = TextProcessing.get_word_token_rejection_rate(body_tokens, lang_id)
    if word_token_rejection_rate > 0.1:
        print("File '{}' contains too many rejected words in body (rejection rate: {:.2f}).".format(story_file_path, word_token_rejection_rate))
        return None

    if TextProcessing.has_repetitive_sentences(body_content):
        print("File '{}' contains repetitive sentences in body.".format(story_file_path))
        return None

    if TextProcessing.has_repeating_token_in_sequence(body_tokens, min_repeats=10):
        print("File '{}' contains repeating tokens.".format(story_file_path))
        return None

    if len(set(body_tokens)) < len(body_tokens)/50:
        print("WARNING: File '{}' contains too many repeated words.".format(story_file_path))

    num_none_letter_sequences = TextProcessing.num_lines_non_letter_sequence(body_content, r"!@#$%^&()_+={}\[\]:;'<>/\\|-~")
    if num_none_letter_sequences >= 3:
        print("File '{}' contains too many lines with none-letter sequences.".format(story_file_path))
        return None

    title_tokens = TextProcessing.get_word_tokens_from_text(title_content, lang_id, filter_words=False)
    if not title_tokens:
        print("No word tokens found in title of file '{}'.".format(story_file_path))
        return None

    tokens = title_tokens + body_tokens
    tokens = [token for token in tokens if word_accepter(token)]

    if not tokens:
        print("No word tokens found in title + body.")
        return None

    return tokens

def count_tokens_from_story_file(lang_id: str, story_file_path: str) -> Counter[str]:

    word_accepter = TextProcessing.get_word_accepter(lang_id)
    tokens = get_tokens_from_story(story_file_path, word_accepter, lang_id)
    return Counter(tokens)


class WFListData(NamedTuple):
    lang_id: str
    word_counter: Counter[str]
    word_counter_per_story: Counter[str]
    num_stories: int
    num_words: int
    file_path: str

def create_wf_list(lang_story_dir: str, executor: Executor) -> WFListData:

    lang_id = lang_story_dir
    word_counter: Counter[str] = Counter()
    word_counter_per_story: Counter[str]  = Counter()

    if lang_id not in LANGUAGE_CODES_WITH_NAMES:
        print("Unknown language '{}'. Skipped creating word frequency list.".format(lang_id))
        return WFListData(lang_id, Counter(), Counter(), 0, 0, '')

    story_files = []

    for story_file in os.listdir(os.path.join(STORIES_DIR, lang_story_dir)):
        story_file_path = os.path.join(STORIES_DIR, lang_story_dir, story_file)
        if not os.path.isfile(story_file_path):
            print("File '{}' is not a file.".format(story_file_path))
            continue
        if not story_file_path.endswith(".txt"):
            print("File '{}' is not a text file.".format(story_file_path))
            continue
        story_files.append(story_file_path)


    if len(story_files) < 10:
        print("Not enough stories for language '{}'.".format(lang_id))
        return WFListData(lang_id, Counter(), Counter(), 0, 0, '')

    count_tokens_from_story_file_fn_for_lang = partial(count_tokens_from_story_file, lang_id)
    stories_counted_tokens = list(executor.map(count_tokens_from_story_file_fn_for_lang, story_files))

    for story_counted_tokens in stories_counted_tokens:
        word_counter.update(story_counted_tokens)
        word_counter_per_story.update(set(story_counted_tokens))

    wf_file = os.path.join(WF_LISTS_DIR, "wf_list_{}.csv".format(lang_id))

    entries = [(word, count, word_counter_per_story[word]) for word, count in word_counter.items()]
    max_count = max([entry[1] for entry in entries])
    max_story_count = max([entry[2] for entry in entries])
    sorted_entries = sorted(entries, key=lambda x: fmean([x[1]/max_count,x[2]/max_story_count]), reverse=True)

    num_stories = len(story_files)
    num_words = 0

    with open(wf_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word", "count", "doc_count"])
        for word, count, story_count in sorted_entries:
            if story_count < 2:
                continue
            writer.writerow([word, count, story_count])
            num_words += 1

    print("Created word frequency list for language '{}' ({}) based on {} stories.".format(lang_id, LANGUAGE_CODES_WITH_NAMES[lang_id], num_stories))

    return WFListData(lang_id, word_counter, word_counter_per_story, num_stories, num_words, wf_file)


def create_wf_lists() -> None:

    start_time = time.time()

    if not os.path.exists(WF_LISTS_DIR):
        os.makedirs(WF_LISTS_DIR)

    # create word frequency list files

    wf_lists_data: list[WFListData] = []

    with ProcessPoolExecutor(max_workers=6) as executor:
        for lang_story_dir in os.listdir(STORIES_DIR):
            wf_list_data = create_wf_list(lang_story_dir, executor)
            wf_lists_data.append(wf_list_data)

    print("Created word frequency lists in {:.2f} seconds.".format(time.time() - start_time))

    # create overview file

    overview_file_path = os.path.join("wf_lists_overview.md")

    wf_lists_data.sort(key=lambda x: x.num_stories, reverse=True)

    with open(overview_file_path, "w", encoding="utf-8") as file:
        file.write("# Word frequency lists overview\n\n")
        file.write("| Language | Word count | Story count |\n")
        file.write("| --- | --- | --- |\n")
        for wf_list_data in wf_lists_data:
            if not wf_list_data.lang_id in LANGUAGE_CODES_WITH_NAMES:
                continue
            language_name = LANGUAGE_CODES_WITH_NAMES[wf_list_data.lang_id]
            link_to_wf_list = "[{}]({})".format(language_name, wf_list_data.file_path.replace("\\", "/"))
            file.write("| {} | {:,} | {:,} |\n".format(link_to_wf_list, wf_list_data.num_words, wf_list_data.num_stories))
        file.write("\n")

    print("Created overview file '{}'.".format(overview_file_path))



if __name__ == "__main__":
    create_wf_lists()
