import logging
import re
from typing import Tuple

import requests
from bs4 import BeautifulSoup


def scraper_html(url: str) -> Tuple[str, str]:
    """
    Scrapes the HTML content of a given URL and extracts the title, lead text (if available), and main body text.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        Tuple[str, str]: A tuple containing the extracted title and the concatenated lead text and main body text.
    """

    logger = logging.getLogger(__name__)
    logger.info("Getting article text from URL")

    # Get html from url
    response = requests.get(url)
    html_content = response.content

    # Init scraper
    soup = BeautifulSoup(html_content, "html.parser")

    # Get article title
    title_element = soup.title
    title = title_element.get_text()

    class_types = {
        "cnn_portugal": "article-conteudo",
        "sic_noticias_lead": "g-article-lead lead",
        "sic_noticias": "full-article-fragment full-article-body first full-article-body-legacy",
        "observador": "article-body-content",
        "noticias_ao_minuto": "news-main-text content",
        "publico_lead": "story__blurb lead",
        "publico": "story__body",
        "dn": "t-af1-content-1",
        "dinheiro_vivo": "t-article-body-1",
        "dineheiro_vivo_lead": "t-ah-desc",
        "jn": "t-article-content-inner",
        "dnoticias": "article--body",
        "dnoticias_lead": "article--header",
        "rr": "slab-400",
        "rr_lead": "rr-lead",
        "jornalnegocios": "texto paywall",
        "sapo_24": "content",
        "tsf_lead": "t-ah-desc",
    }
    # Exclude classes that are in the article but are not relevant to article body
    excluding_classes = [
        "relacionados-no-texto",
        "t-content-responsive-1",
        "article--footer",
        "relatedLink",
        "related-article",
        "t-a-subscribe-1 js-contentcollapse-root",
        "t-grp-title-5",
        "t-a-info-share",
        "t-abc-footer",
        "t-a-multimedia-1",
        "t-a-info-authoring",
        "t-a-info-share-comment",
        "t-a-audioplayer-1",
        "t-af-share-2",
        "t-af-comments-1",
        "t-af-callout-5 js-contentcollapse-root newslettercapping",
        "t-af-multimedia-1",
        "t-af1-c1-sb js-a-content-sb-elm-ref",
    ]

    # Get lead text if it exists
    try:
        lead_paragraph = soup.find("p", class_=class_types.values())
        news_lead = ""
        for element in lead_paragraph:
            news_lead += element.get_text()
    except BaseException:
        pass

    # Find and remove the <div class="unwanted_classes"> elements
    related_link_divs = soup.find_all(
        ["div", "aside", "footer"], class_=excluding_classes
    )
    for div in related_link_divs:
        div.decompose()

    # Get main body text:
    news_elements = soup.find_all("div", class_=class_types.values())

    news_text = ""
    for element in news_elements:
        news_text += element.get_text().strip()

    news_body = news_lead + news_text
    # Add space between period and capital letters of next sentence if it doesnt exist
    news_body = re.sub(r"\.(?=[A-Z\"])", ". ", news_body).strip()
    return title, news_body


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    url = "https://www.tsf.pt/portugal/politica/psd-vai-pedir-ao-ministerio-publico-que-avalie-se-houve-falsas-declaracoes-de-galamba-na-cpi-a-tap-16490844.html"
    title, body = scraper_html(url)
    print(">>> Title: ", title, "\n\n>>> Article Text: ", body)
