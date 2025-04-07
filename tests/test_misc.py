import os
from lib.misc import StoryTitles

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def test_story_titles_prefix_from_title():

    titles = [
        "A very long title",
        "A very loooooooooong title", # 3 first words should be used for prefix, as first word is to short
        "Super long cool title",
        "Super long cool title 2", # 2 first words should be used for prefix, so this one should be removed
    ]

    titles_dir = os.path.join(TEST_DATA_DIR, "titles")
    story_titles = StoryTitles("en", titles_dir)

    unique_titles = list(story_titles.unique_titles(titles))
    assert unique_titles == ["A very long title", "A very loooooooooong title", "Super long cool title"]