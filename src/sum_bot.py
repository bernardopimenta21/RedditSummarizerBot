import logging
import os
from datetime import datetime

import praw
import tldextract
import yaml

from logs_helper import load_log, log_error, update_log
from scraper import scraper_html
from summarizer import generate_extractive_summary, get_relevant_keywords

logging.basicConfig(
    filename="status.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

with open("./conf/parameters.yml", "r") as stream:
    PARAMETERS = yaml.safe_load(stream)

try:
    with open("./conf/local/globals.yml", "r") as stream:
        globals_config = yaml.safe_load(stream)
    # Set environment variables from the globals_config dictionary
    for key, value in globals_config.items():
        os.environ[key] = value
except FileNotFoundError:
    print(
        "No globals.yml file found. Continuing without setting environment variables."
    )


TEMPLATE = open("./conf/post_template.txt", "r", encoding="utf-8").read()


# Templates.
TEMPLATE = open("./conf/post_template.txt", "r", encoding="utf-8").read()


HEADERS = {"User-Agent": "Sumarizador de Notícias"}


def sum_bot_init() -> None:
    """Initializes the Summarization bot. Starts a Reddit instance using PRAW, obtains the latest posts, checking if they have already been processed. If they haven't then perform summarization and
    comment on the posts with the generated summary"""

    logger = logging.getLogger(__name__)
    logger.info(">>> Initializing Sumarization Bot")
    try:
        reddit = praw.Reddit(
            client_id=os.environ["APP_ID"],
            client_secret=os.environ["APP_SECRET"],
            user_agent=os.environ["USER_AGENT"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
        )
    except KeyError:
        logger.error("Reddit API information is invalid or missing.")

    new_post_found = False
    processed_posts = load_log()
    for subreddit in PARAMETERS["subreddits"]:
        for submission in reddit.subreddit(subreddit).new(
            limit=PARAMETERS["num_posts"]
        ):
            if submission.id not in processed_posts:
                clean_url = submission.url.replace("amp.", "")
                ext = tldextract.extract(clean_url)
                domain = "{}.{}".format(ext.domain, ext.suffix)

                if domain in PARAMETERS["whitelist"]:
                    new_post_found = True
                    try:
                        logger.info(
                            ">> Start summarizer for post with id: {}".format(
                                submission.id
                            )
                        )
                        # Scrape html and get article text
                        article_title, article_body = scraper_html(clean_url)

                        # Perform summarization on article text
                        summary = generate_extractive_summary(
                            article_body, PARAMETERS["num_sentences"]
                        )

                        keywords = get_relevant_keywords(article_body)

                        top_words = ""
                        for index, word in enumerate(keywords):
                            top_words += "{}^{} ".format(word, index + 1)

                        post_message = TEMPLATE.format(
                            article_title,
                            clean_url,
                            datetime.now().date(),
                            top_words,
                            summary,
                        )
                        reddit.submission(submission.id).reply(post_message)
                        update_log(submission.id)
                        logger.info(
                            ">> Submitted reply to post with id: {}".format(
                                submission.id
                            )
                        )

                    except Exception as e:
                        log_error("{},{}".format(clean_url, e))
                        update_log(submission.id)
                        logger.error("Submission Failed:", submission.id)
                        continue
        if not new_post_found:
            logger.info("No new posts to process in /r/{}.".format(subreddit))


if __name__ == "__main__":
    sum_bot_init()
