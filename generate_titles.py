import datetime
import os
import re
from statistics import fmean
import time
from typing import Optional
from openai import OpenAI

from common_lib import LmResponse, get_lm_caller

LM_STUDIO_API_BASE = "http://127.0.0.1:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
MODEL = "meta-llama-3.1-8b-instruct (Q4_K_M)"

NUMBER_OF_STORIES = 3
STORIES_DIR = "stories"
LANG_ID = "nl"

# Temperature and top_p can be tuned to control the randomness of the output.
LM_TEMPERATURE = 0.9
LM_TOP_P = 0.95

call_local_lm = get_lm_caller(LM_STUDIO_API_BASE, LM_STUDIO_API_KEY, MODEL, LM_TEMPERATURE, LM_TOP_P)

class LmTitlesResponse(LmResponse):
    pass

def build_titles_prompt(lang_id: str) -> str:
    prompt = {}
    prompt['nl'] = (
        "Maak je lijstje met 30 titels voor nieuwe (niet bestaande) Nederlandse kinderverhalen. \n"
        "Wees creatief! Geef alleen de titels in <title> tags. De titels moeten minimaal 6 woorden lang zijn. \n"
    )
    prompt['en'] = (
        "Make a list of 30 titles for new (not existing) English children's stories. \n"
        "Be creative! Give the titles only in <title> tags. The titles must be at least 6 words long. \n"
    )
    return prompt[lang_id]

def get_titles_response_from_lm(prompt_text: str, lang_id: str) -> Optional[LmTitlesResponse]:
    response_data = call_local_lm(prompt_text, lang_id)
    if not response_data:
        return None
    (response_content, prompt_text, model, lang_id, time_taken) = response_data
    return LmTitlesResponse(response_content, prompt_text, model, lang_id, time_taken)