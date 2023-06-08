# Reddit News Summarization Bot

A reddit bot that can retrieve articles from portuguese news outlets to generate an **extractive summary** and perform **keyword extraction**.
The Summarization Pipeline is a process that automates the extraction of summaries from news articles and the generation of relevant keywords. It utilizes natural language processing techniques to analyze the content of articles and provide concise summaries that capture the essential information.
It leverages **BERT SentenceTransformers** to generate input sequence embeddings and uses cosine similarity to calculate the similarity between sentence embeddings which allows us to identify the most important sentences in the article's text. This approach allows for an extractive summarization technique where the summary consists of the most relevant and representative sentences from the original text.

## Overview 

The main execution pipeline consists of several steps, including data retrieval, text preprocessing, feature extraction, and summary generation. 

Additionally, it is designed to integrate with platforms like Reddit, where it can comment on posts with the generated summaries, providing users with condensed versions of news articles and facilitating efficient information consumption.

The flow of execution of the bot is represented below in diagram format, depicting the various stages and their interactions:
```mermaid
graph TD
    A[Start] --> B[Load Configuration Files]
    B --> C[Initialize Summarization Bot]
    C --> D[Authenticate with Reddit]
    D --> E[Load Processed Posts Log]
    E --> F[Retrieve Latest Submissions]
    F --> G[Check if Submission is Processed]
    G --> H[Clean URL]
    H --> I[Extract Domain]
    I --> J[Check Domain in Whitelist]
    J --> K[Scrape HTML and Get Article Text]
    K --> L[Generate Summary]
    L --> M[Extract Relevant Keywords]
    M --> N[Prepare Post Message]
    N --> O[Submit Comment on Reddit]
    O --> P[Update Processed Posts Log]
    P --> Q[Print Success Message]
    Q --> R[Continue with Next Submission]
    G --> R[Skip Processed Submission]
    R --> F
    R --> S[Finish]
```
## Sumarization pipeline
The steps of the summarization pipeline represented by the **Generate Summary** block in the previous diagram are here represented sequentially in finer detail. The pipeline starts with text preprocessing to remove unwanted words and tokenize the article text into sentences. Next, sentence embeddings are generated using a Sentence-BERT model. The similarity scores between between sentence embeddings pairs are calculated using cosine similarity. Based on the similarity scores, the top sentences are extracted. Finally, these top sentences are combined to generate the extractive summary.
```mermaid
graph LR
    C[Preprocess Text]
    C --> D[Generate Sentence Embeddings]
    D --> E[Calculate Similarity Scores]
    E --> F[Extract Top Sentences]
    F --> G[Generate Extractive Summary]
    G 
```

## Usage

To use the Summarization Bot, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/bernardopimenta21/RedditSummarizerBot.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
Create in the folder conf/local/**globals.yml**, this is where the reddit API information is store, it should follow the structure:
```yaml
REDDIT_USERNAME : ""
REDDIT_PASSWORD : ""
APP_ID : ""
APP_SECRET : ""
USER_AGENT : ""
```
Edit the file conf/**parameters.yml**:
```yaml
subreddits : [""]
whitelist : [""]
sentence_transfomer : ""
num_sentences : ''
num_posts : ''
```
 where:
- subreddits: is a list of subreddits to search for articles
- whitelist: is the list of whitelisted news websites
- sentence_transfomer: the Hugging face model to use, currently "distilbert-base-nli-stsb-mean-tokens" is employed
- num_sentences: number of sentences that the summary will have
- num_posts: number of posts of each subreddits new page to search for news articles in each run

4. Run the bot execution script:
```bash
python sum_bot.py
```
Alternatively it is possible to run each module individually, to perform summarization and keyword extraction, independently of the bot:
```bash
python scraper.py
python summarization.py
```
