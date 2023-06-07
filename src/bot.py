import logging
from datetime import datetime

import praw
import tldextract
import yaml

from src.logs_helper import load_log, log_error, update_log
from src.scraper import scraper_html
from src.summarizer import generate_extractive_summary, get_relevant_keywords

with open("./conf/parameters.yml", "r") as stream:
    PARAMETERS = yaml.safe_load(stream)

with open("./conf/local/conf.yml", "r") as stream:
    CONF = yaml.safe_load(stream)

TEMPLATE = open("./conf/post_template.txt", "r", encoding="utf-8").read()


# Templates.
TEMPLATE = open("./conf/post_template.txt", "r", encoding="utf-8").read()


HEADERS = {"User-Agent": "Sumarizador de Notícias"}


def sum_bot_init() -> None:
    """Initializes the Summarization bot. Starts a Reddit instance using PRAW, obtains the latest posts, checking if they have already been processed. If they haven't then perform summarization and
    comment on the posts with the generated summary"""

    logger = logging.getLogger(__name__)
    logger.info("Initializing Sumarization Bot")

    reddit = praw.Reddit(
        client_id=CONF["APP_ID"],
        client_secret=CONF["APP_SECRET"],
        user_agent=CONF["USER_AGENT"],
        username=CONF["REDDIT_USERNAME"],
        password=CONF["REDDIT_PASSWORD"],
    )

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
                    try:
                        # Scrape html and get article text
                        article_title, article_body = scraper_html(clean_url)

                        # Perform summarization on article text
                        logger.info("Generating summary...")

                        summary = generate_extractive_summary(
                            article_body, PARAMETERS["num_sentences"]
                        )

                        logger.info("Extracting relevant keywords...")

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
                        logger.info("Submitting comment...")
                        reddit.submission(submission.id).reply(post_message)
                        update_log(submission.id)
                        print("Created a reply to post with id: ", submission.id)

                    except Exception as e:
                        log_error("{},{}".format(clean_url, e))
                        update_log(submission.id)
                        print("Submission Failed:", submission.id)
                        continue


if __name__ == "__main__":
    sum_bot_init()
