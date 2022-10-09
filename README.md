# Senty 📊 🚗 💬

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/johnphilipp/yt-analytics-web/0_🚗_Home.py/)

## What?

- Automotive market intelligence via social media analytics

## Why?

- Discover product insights and feedback via social media
- Separate the signal from the noise
- Benchmark products against your competition

## Implementation Features
- Downloading comments and replies of a YouTube video via YouTube API
- Cleaning comments (e.g., removing user names, urls, stopwords)
- Calculating sentiment (from 1 (neg) to 5 (pos)) via Google's BERT transformer-based NLP model + dataset from HuggingFace which is finetuned for sentiment analysis on product reviews in six languages
- Pusing data to Supabase (Postgres database provider)
- Displaying simple UI using Streamlit

## How To Run
```
streamlit run 0_🚗_Home.py
```
