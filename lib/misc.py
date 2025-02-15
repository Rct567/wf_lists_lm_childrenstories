
import os

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

