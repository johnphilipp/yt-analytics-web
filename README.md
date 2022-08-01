# What Does Youtube Think (WDYT)?

What?

- Tool to analyze the sentiment of comments for any given YouTube video

Why?

- Automotive stakeholders (PMs, Engineers, Designers, Sales, etc.) must be aware of feedback/critique from consumers and media

How?

- Downloading comments and replies of a YouTube video via YouTube API
- Cleaning comments (e.g., removing name mentions, urls, and in some cases stopwords)
- Calculating sentiment (from 1 (negative) to 5 (positive)) via Hugging Face's "nlptown/bert-base-multilingual-uncased-sentiment" model finetuned for sentiment analysis on product reviews in six languages
- Grouping the sentiment for each car/video by its features
- Displaying a radar chart using streamlit and plotly

<img src="https://p-john.com/wp-content/uploads/2022/07/Screen-Shot-2022-07-06-at-11.18.54-AM.png">
<img src="https://p-john.com/wp-content/uploads/2022/07/Screen-Shot-2022-07-06-at-11.19.11-AM.png">
