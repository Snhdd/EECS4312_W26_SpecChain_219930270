# EECS4312_W26_SpecChain

## Application Studied
Application: **Wysa - Mental Health Support App**

This project analyzes user reviews collected from the Google Play Store for the Wysa application.  
The objective is to build and compare **manual**, **automated**, and **hybrid requirements engineering pipelines** for persona generation, requirement specification, test generation, and metric evaluation.

---

## Data Collection Method
Reviews were collected from the **Google Play Store** using the `google-play-scraper` Python library.

Collection settings:
- Language: English
- Country: Canada
- Sort order: Newest
- Initial collection size: **1000 reviews**

---

## Dataset
- `data/reviews_raw.jsonl` contains the originally collected raw reviews
- `data/reviews_clean.jsonl` contains the cleaned dataset
- Final cleaned dataset size: **832 reviews**

Cleaning steps included:
- duplicate removal
- empty review removal
- lowercase normalization
- punctuation and URL removal
- stopword removal
- lemmatization

---

## Repository Structure
- `data/` → datasets, raw reviews, cleaned reviews, review groups
- `personas/` → manual, automated, and hybrid persona files
- `spec/` → generated requirements specifications
- `tests/` → generated test cases
- `metrics/` → pipeline metrics and comparison summary
- `prompts/` → Groq prompt records
- `reflection/` → final reflection document
- `src/` → executable Python scripts
- `README.md` → project documentation

---

## How to Run
### Validate repository
```bash
python3.11 src/00_validate_repo.py