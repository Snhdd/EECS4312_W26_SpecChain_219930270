from google_play_scraper import reviews_all, Sort
import json

APP_ID = "bot.touchkin"

# collect all available reviews (up to store limit)
result = reviews_all(
    APP_ID,
    sleep_milliseconds=0,
    lang="en",
    country="ca",
    sort=Sort.NEWEST
)

# keep only first 1000 reviews
result = result[:1000]

with open("data/reviews_raw.jsonl", "w", encoding="utf-8") as f:
    for idx, review in enumerate(result):
        review["review_id"] = idx + 1
        f.write(json.dumps(review, ensure_ascii=False, default=str) + "\n")

print(f"Collected {len(result)} reviews successfully.")