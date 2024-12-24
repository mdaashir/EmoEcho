from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re


def preprocessText(text):
    # Preprocesses the input text to remove unnecessary elements such as URLs, special characters, numbers, and converts text to lowercase.
    cleaned_text = text.lower()
    cleaned_text = re.sub(r"@[A-Za-z0-9_]+", " ", cleaned_text)  # Remove mentions
    cleaned_text = re.sub(r"#[A-Za-z0-9_]+", " ", cleaned_text)  # Remove hashtags
    cleaned_text = re.sub(r"http\S+", " ", cleaned_text)  # Remove http URLs
    cleaned_text = re.sub(r"www.\S+", " ", cleaned_text)  # Remove www URLs
    cleaned_text = re.sub(r"[()!?]", " ", cleaned_text)  # Remove special characters
    cleaned_text = re.sub(r"\[.*?\]", " ", cleaned_text)  # Remove inside square brackets
    cleaned_text = re.sub(r"[^a-z0-9]", " ", cleaned_text)  # Remove anything that's not alphanumeric
    cleaned_text = re.sub(r"[0-9]+", " ", cleaned_text)  # Remove numbers
    cleaned_text = re.sub(r"\brt\b", "", cleaned_text)  # Remove retweet sign (rt)
    cleaned_text = cleaned_text.strip()  # Strip extra spaces
    return cleaned_text


def sentimentAnalysis(cleaned_text):
    # Analyzes the sentiment of the cleaned text using VADER SentimentIntensityAnalyzer.
    score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
    neg = score["neg"]
    neu = score["neu"]
    pos = score["pos"]
    com = score["compound"]
    value = round(score["compound"], 2)

    # print(f"Score: {value}")  # For Debugging

    if neg > 0:
        if value < -0.6:
            return value, "Alarming!"
        elif value < -0.5:
            return value, "Level 3 : Consultation Needed"
        elif value < -0.4:
            return value, "Level 2 : Some Help would be preferred"
        elif value < -0.3:
            return value, "Basic sadness"

    return 0, "You're Okay!"
