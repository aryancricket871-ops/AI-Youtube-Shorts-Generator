import os
import json
import re
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gemini-3.5-flash"

# Gemini returns these when it is overloaded or rate-limiting rather than when
# the request itself is wrong, so they are worth waiting out.
RETRYABLE_STATUSES = (429, 500, 502, 503, 504)

# Longest a single retry will sleep. A daily-quota 429 reports delays far past
# anything worth blocking a run on.
MAX_RETRY_WAIT = 90

# Extra writing rules used only for Hindi scripts, so the narration sounds like
# a real Indian YouTuber speaking rather than a textbook being read aloud.
HINDI_STYLE_RULES = """
    - **Hindi style:** Write natural, spoken Hindi in Devanagari script, the way a popular Indian facts YouTuber talks to viewers. Use easy everyday words, NOT bookish or Sanskritized Hindi.
    - Everyday English words that Indians commonly use may be written in Devanagari (for example: साइंटिस्ट, इंटरनेट, प्लैनेट, स्पेस).
