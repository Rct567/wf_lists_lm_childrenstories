from collections import Counter
import csv
import os
import re
from statistics import fmean
from lib.language_data import LANGUAGE_CODES_WITH_NAMES
from lib.misc import STORIES_DIR, WF_LISTS_DIR
from lib.text_processing import TextProcessing

def create_wf_list(lang_story_dir: str) -> None:

    assert len(lang_story_dir) == 2
    lang_id = lang_story_dir
    word_counter: Counter[str] = Counter()
    word_counter_per_story: Counter[str]  = Counter()
    num_stories = 0

    for story_file in os.listdir(os.path.join(STORIES_DIR, lang_story_dir)):

        story_file_path = os.path.join(STORIES_DIR, lang_story_dir, story_file)
        num_stories += 1

        if not os.path.isfile(story_file_path):
            print("File '{}' is not a file.".format(story_file_path))
            continue
        if not story_file.endswith(".txt"):
            print("File '{}' is not a text file.".format(story_file_path))
            continue

        content_of_file = open(story_file_path, "r", encoding="utf-8").read()

        if not "<title>" in content_of_file:
            print("No <title> tag found in file '{}'.".format(story_file_path))
            continue

        # start content from last <title> tag
        content = content_of_file[content_of_file.rfind("<title>"):].strip()

        match = re.search(r"<title>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
        if not match:
            print("No <title> tag found in file '{}'.".format(story_file_path))
            continue
        title_content = match.group(1).strip()

        if not "<body>" in content:
            print("No <body> tag found in file '{}'.".format(story_file_path))
            continue

        body_content = content[content.rfind("<body>")+len("<body>"):].strip().replace("</body>", "")
        text = TextProcessing.get_plain_text(title_content+" "+body_content)
        tokens = TextProcessing.get_word_tokens_from_text(text, lang_id, filter_words=True)
        if not tokens and body_content:
            print("No tokens produced for file '{}'.".format(story_file_path))

        word_counter.update(tokens)
        word_counter_per_story.update(set(tokens))

    if num_stories < 10:
        print("Not enough stories for language '{}'.".format(lang_id))
        return
    if not word_counter:
        print("No words found for language '{}'.".format(lang_id))
        return

    wf_file = os.path.join(WF_LISTS_DIR, "wf_list_{}.csv".format(lang_id))

    entries = [(word, count, word_counter_per_story[word]) for word, count in word_counter.items()]
    max_count = max([entry[1] for entry in entries])
    max_story_count = max([entry[2] for entry in entries])
    sorted_entries = sorted(entries, key=lambda x: fmean([x[1]/max_count,x[2]/max_story_count]), reverse=True)

    with open(wf_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word", "count", "doc_count"])
        for word, count, story_count in sorted_entries:
            if story_count == 1:
                continue
            writer.writerow([word, count, story_count])

    print("Created word frequency list for language '{}' ({}) based on {} stories.".format(lang_id, LANGUAGE_CODES_WITH_NAMES[lang_id], num_stories))


if not os.path.exists(WF_LISTS_DIR):
    os.makedirs(WF_LISTS_DIR)

for lang_story_dir in os.listdir(STORIES_DIR):
    create_wf_list(lang_story_dir)
