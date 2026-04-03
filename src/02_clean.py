import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import json
import re
from pathlib import Path

import nltk
from num2words import num2words
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# download required nltk resources
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

RAW_PATH = Path("data/reviews_raw.jsonl")
CLEAN_PATH = Path("data/reviews_clean.jsonl")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def convert_numbers_to_words(text: str) -> str:
    def repl(match):
        try:
            return " " + num2words(int(match.group())) + " "
        except:
            return " "
    return re.sub(r"\b\d+\b", repl, text)


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = convert_numbers_to_words(text)

    # remove urls
    text = re.sub(r"http\S+|www\S+", " ", text)

    # remove emojis and non-ascii-ish symbols
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # keep only letters and spaces
    text = re.sub(r"[^a-z\s]", " ", text)

    # remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # remove stopwords + lemmatize
    tokens = []
    for word in text.split():
        if word not in stop_words:
            lemma = lemmatizer.lemmatize(word)
            tokens.append(lemma)

    return " ".join(tokens)


def extract_review_text(review_obj: dict) -> str:
    # google-play-scraper usually stores the actual review in "content"
    return review_obj.get("content", "").strip()


def main():
    seen_raw = set()
    cleaned_reviews = []
    review_counter = 1

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        for line in f:
            review = json.loads(line)
            raw_text = extract_review_text(review)

            if not raw_text:
                continue

            raw_text_norm = raw_text.strip().lower()
            if raw_text_norm in seen_raw:
                continue
            seen_raw.add(raw_text_norm)

            cleaned_text = clean_text(raw_text)

            # remove empty / extremely short reviews
            if not cleaned_text:
                continue
            if len(cleaned_text.split()) < 3:
                continue

            cleaned_reviews.append({
                "review_id": review_counter,
                "source_review_id": review.get("reviewId", ""),
                "raw_text": raw_text,
                "cleaned_text": cleaned_text
            })
            review_counter += 1

    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        for item in cleaned_reviews:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Cleaned dataset saved to {CLEAN_PATH}")
    print(f"Total cleaned reviews: {len(cleaned_reviews)}")


if __name__ == "__main__":
    main()